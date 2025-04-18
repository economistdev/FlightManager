from FlightManager import FlightManager
from Database import FlightDatabase
from AnalyticsManager import AnalyticsManager
from utils import create_menu_options, show_menu, validate_option_input

class FlightCli:

    def __init__(self, conn_string):
        self.db = FlightDatabase(conn_string)
        self.flight_manager = FlightManager(self.db)
        self.analytics_manager = AnalyticsManager(self.db)

    def start(self):
        self.main_menu()

    def handle_options(self, options_to_show):
        options = create_menu_options(options_to_show)
        show_menu(options)
        selected = validate_option_input(1, len(options))
        return options[selected]

    def main_menu(self):
        options = {
            "View Flights": self.flight_manager.view_flights,
            "Create Flights": self.flight_manager.create_flight,
            "Modify Flights": self.flight_manager.update_flight,
            "Analytics": self.analytics_manager.analyse,
            "Exit": None
        }
        selected_option = self.handle_options(options.keys())
        if selected_option == "Exit":
            exit(0)
        return options[selected_option](self.main_menu)
    