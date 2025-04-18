from utils import show_results, validate_y_n_input, show_menu, validate_multi_fields_input, create_menu_options, show_options, validate_option_input, validate_text_input
import os
import yaml

config_dir = os.path.join(os.path.dirname(__file__), "yaml")
fm_config_path = os.path.join(config_dir, "flight_manager_config.yaml")
config_path = os.path.join(config_dir, "config.yaml")

with open(fm_config_path, "r") as file:
    fm_config = yaml.safe_load(file)

with open(config_path, "r") as file:
    config = yaml.safe_load(file)

flight_filter_params = fm_config["flight_filter_params"]
flight_create_params = fm_config["flight_create_params"]

class FlightManager:

    def __init__(self, db):
        self.db = db

    def present_values_reference_table(self, option):
        valid_values_query = flight_filter_params["input"][option]["valid_values"]
        if valid_values_query is None:
            print(f"\n{option}")
        else:
            print(f"\n{option} Valid Values For Reference")
            show_results(*self.db.query(valid_values_query))

    def get_flight_filter_string(self, option):
        self.present_values_reference_table(option)
        filter = validate_text_input("Enter the text you would like to filter on (fuzzy matching active): ", accept_none=False)
        table = flight_filter_params["input"][option]["filter_col"]
        return f"{table} LIKE ?", f"%{filter}%"

    def view_flights(self, return_callback):

        show_results(*self.db.query(config["show_flights"]))
        choice = validate_y_n_input("Would you like to filter by fields? ")

        if choice == "y":
            while True:
                options = create_menu_options(flight_filter_params["input"].keys())
                show_menu(options)
                filter_options_ints = validate_multi_fields_input(options)

                filter_clauses = []
                filter_params = []
                for option in filter_options_ints:
                    param, val = self.get_flight_filter_string(options[option])
                    filter_clauses.append(param)
                    filter_params.append(val)
                query = flight_filter_params["filter_query"] + " " + " AND ".join(filter_clauses)
                show_results(*self.db.query(query, filter_params))
                choice = validate_y_n_input("Would you like to filter again? ")

                if choice == "n":
                    return return_callback()

        return return_callback()
    
    def communicate_requirement(self, necessary):
        if necessary:
            print("(REQUIRED)")
        else:
            print("(NOT REQUIRED - Press Enter to Skip)")
        return None

    def create_flight(self, return_callback):

        insert_values = {}

        while True:

            for insert_col in flight_create_params["input"].keys():
                
                print(f"\n{insert_col} Selection")

                params = flight_create_params["input"][insert_col]

                choice = self.choose_record_or_input(params)
                insert_values[params["insert_col"]] = choice
            
            try:
                self.db.query(flight_create_params["insert_query"], insert_values)
                row_id_inserted = self.db.cursor.lastrowid
                self.db.conn.commit()
                show_results(*self.db.query(config["show_flights_by_id"], [row_id_inserted]))

                choice = validate_y_n_input("Flight creation successful. Would you like to create another flight? ")
                if choice == "n":
                    return return_callback()
            except Exception as e:
                print(e)
                choice = validate_y_n_input("Flight creation unsuccessful. Would you like to try again? ")
                if choice == "n":
                    return return_callback()

    
    def update_flight(self, return_callback):

        while True:
            #Pick Flight to eidt
            print("Select a flight ID to edit")
            flights_params = {"options":config["show_flights"], "necessary": True}
            flight_id = self.choose_record_or_input(flights_params)

            # Get input tables
            options = create_menu_options(flight_create_params["input"].keys())
            show_menu(options)
            filter_options_ints = validate_multi_fields_input(options)
            update_cols = [col for idx, col in options.items() if idx in filter_options_ints]

            update_clauses = []

            for update_col in update_cols:
                
                print(f"\n{update_col} Selection")

                params = flight_create_params["input"][update_col]
                choice = self.choose_record_or_input(params)
                
                update_clauses.append(f"{params["insert_col"]}={choice}")
            
            update_clauses = ", ".join(update_clauses)
            query = "UPDATE flights SET " + update_clauses + " WHERE id=" + flight_id

            try:
                self.db.query(query)
                self.db.conn.commit()
                show_results(*self.db.query(config["show_flights_by_id"], [flight_id]))

                choice = validate_y_n_input("Flight update successful. Would you like to update another flight? ")
                if choice == "n":
                    return return_callback()
            except Exception as e:
                print(e)
                choice = validate_y_n_input("Flight update unsuccessful. Would you like to try again? ")
                if choice == "n":
                    return return_callback()
            

    def choose_record_or_input(self, params):
        choice = ""
        necessary = params["necessary"]

        if params["options"] is not None:
            rows, cols = self.db.query(params["options"])
            
            show_options(rows, cols)
            self.communicate_requirement(necessary)
            
            choice = str(validate_option_input(1, len(rows), accept_none=not necessary))
        else:
            self.communicate_requirement(necessary)
            choice = validate_text_input("Please enter the field: ", accept_none=not necessary)
        choice = None if choice == "" else choice

        return choice
