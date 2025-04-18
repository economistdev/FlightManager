import sqlite3
import yaml
import os

file_path = os.path.join(os.path.dirname(__file__), 'yaml')
setup_queries_path = os.path.join(file_path, "setup_queries.yaml")
config_path = os.path.join(file_path, "config.yaml")

with open(setup_queries_path, 'r') as file:
    setup_queries= yaml.safe_load(file)

with open(config_path, 'r') as file:
    config = yaml.safe_load(file)

class FlightDatabase:

    def __init__(self, conn_string: str):
        self.conn = sqlite3.connect(conn_string)
        self.cursor = self.conn.cursor()
        self.tables = setup_queries["create_tables"].keys()
        self.views = setup_queries["create_views"].keys()
        if config["first_run"]:
            self.setup_db()

    def check_table_exists(self, table):
        return table in self.tables

    def setup_db(self):
        # Create tbls
        for table, query in setup_queries["create_tables"].items():
            self.cursor.execute(f'DROP TABLE IF EXISTS {table}')
            self.cursor.execute(query)
        # Create views
        for view, query in setup_queries["create_views"].items():
            self.cursor.execute(f'DROP VIEW IF EXISTS {view}')
            self.cursor.execute(query)
        # Populate tbls
        for query in setup_queries["populate_tables"].values():
            self.cursor.execute(query)

        self.conn.commit()

        with open(config_path, 'w') as file:
            config["first_run"] = False
            yaml.safe_dump(config, file)
    
    def query(self, *args):
        self.cursor.execute(*args)

        if args[0].strip().upper().startswith("SELECT"):
            rows = self.cursor.fetchall()
            columns = [description[0] for description in self.cursor.description]
            return (rows, columns)
        else:
            return None
        