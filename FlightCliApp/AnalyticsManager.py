from utils import show_results, show_menu, create_menu_options, validate_option_input, press_enter
import os
import yaml

am_config_path = os.path.join(os.path.dirname(__file__), "yaml", "analytics_manager_config.yaml")

with open(am_config_path, "r") as file:
    am_config = yaml.safe_load(file)

analytics_queries = am_config["analytics_queries"]

class AnalyticsManager:
    def __init__(self, db):
        self.db = db

    def handle_options(self, options_to_show):
        options = create_menu_options(options_to_show)
        show_menu(options)
        selected = validate_option_input(1, len(options))
        return options[selected]

    def flights_by_pilot_summary(self):
        
        show_results(*self.db.query(analytics_queries["flights_by_pilot"]))
        press_enter()

        return self.analyse()
    
    def capacity_by_route_summary(self):
        
        show_results(*self.db.query(analytics_queries["capacity_by_route"]))
        press_enter()

        return self.analyse()
    
    def airports_by_country(self):
        
        show_results(*self.db.query(analytics_queries["airports_by_country"]))
        press_enter()

        return self.analyse()
    

    def analyse(self, return_callback=None):
        if return_callback is not None:
            self.return_callback = return_callback

        options = {
            "Flights By Pilot": self.flights_by_pilot_summary,
            "Capacity By Route": self.capacity_by_route_summary,
            "Airports By Country": self.airports_by_country,
            "Back": self.return_callback
        }
        selected_option = self.handle_options(options.keys())
        return options[selected_option]()
        


        
