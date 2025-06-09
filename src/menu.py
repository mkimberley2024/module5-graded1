from flight_info import FlightInfo
from pilots import Pilots
from db_operations import DBOperations
from airports import Airports
from summaries import Summaries

class Menu:
    def __init__(self, db_filename):
        self.db_operations = DBOperations(db_filename)
        self.db_operations.connect()
        self.flight_info = FlightInfo(db_filename)
        self.pilots = Pilots(db_filename)
        self.airports = Airports(db_filename)
        self.summaries = Summaries(db_filename)

# Initialise Menu Items

        self.main_menu_items = [
            {"option": 1, "description": "Manage Flights", "function": self.handle_flights_menu},
            {"option": 2, "description": "Manage Pilots", "function": self.handle_pilots_menu},
            {"option": 3, "description": "Manage Airports / Destinations", "function": self.handle_airports_menu},
            {"option": 4, "description": "Show Summaries", "function": self.handle_summaries_menu},
            {"option": 10, "description": "Exit", "function": self.exit_program},
        ]

        self.flights_menu_items = [
            {"option": 1, "description": "View All Flights", "function": self.show_all_flights},
            {"option": 2, "description": "Add a new flight", "function": self.create_flight},
            {"option": 3, "description": "View Flights by Criteria", "function": self.view_flights_by_criteria},
            {"option": 4, "description": "Updte Flight Information", "function": self.update_flight_information},
            {"option": 5, "description": "Delete Flight", "function": self.delete_flight},
            {"option": 10, "description": "Back to Main Menu", "function": self.go_back_to_main_menu},
        ]

        self.pilots_menu_items = [
            {"option": 1, "description": "View All Pilots", "function": self.show_all_pilots},
            {"option": 2, "description": "View Pilots by Criteria", "function": self.view_pilots},
            {"option": 3, "description": "Add Pilot", "function": self.add_pilot},
            {"option": 4, "description": "Update Pilot Information", "function": self.update_pilot_information},
            {"option": 5, "description": "Delete Pilot", "function": self.delete_pilot},
            {"option": 6, "description": "Assign Pilot to flight", "function": self.assign_pilot_to_flight},
            {"option": 8, "description": "Remove Pilot from flight", "function": self.remove_pilot_from_flight},
            {"option": 9, "description": "Display Pilot Schedule", "function": self.get_pilot_schedule},
            {"option": 10, "description": "Back to Main Menu", "function": self.go_back_to_main_menu},
        ]

        self.airports_menu_items = [
            {"option": 1, "description": "View all Airports", "function": self.view_airports},
            {"option": 2, "description": "Add Airport", "function": self.add_airport},
            {"option": 3, "description": "Update Airport Information", "function": self.update_airport_information},
            {"option": 4, "description": "Delete Airport", "function": self.delete_airport},
            {"option": 10, "description": "Back to Main Menu", "function": self.go_back_to_main_menu},
        ]


        self.summary_menu_items = [
            {"option": 1, "description": "Show All Flights by Destination Airport", "function": self.summaries_destination_airport},
            {"option": 2, "description": "Show All Flights by Departure Airport", "function": self.summaries_departure_airport},
            {"option": 3, "description": "Show Flights by Pilot", "function": self.summaires_flights_by_pilot},
            {"option": 4, "description": "Show Pilots assigned to Flights", "function": self.summaries_pilots_assigned_to_flights},
            {"option": 5, "description": "Show all Schduled Flights", "function": self.summaries_scheduled_flights},
            {"option": 6, "description": "Show all Cancelled Flights", "function": self.summaries_cancelled_flights},
            {"option": 10, "description": "Back to Main Menu", "function": self.go_back_to_main_menu},
        ]



# Menu Input Handling

    def getInput(self, prompt):
        while True:
            try:
                value = input(prompt)
                if not value.strip():
                    raise ValueError("Input cannot be empty")
                return value
            except ValueError as e:
                print(f"Invalid input: {e}. Please try again.")

    def display_menu(self, menu_items):
        print("\nMenu:")
        print("**********")
        for item in menu_items:
            print(f" {item['option']}. {item['description']}")
        print("\n")

# Main Menu Handler

    def handle_main_menu(self):
        while True:
            self.display_menu(self.main_menu_items)
            choice = int(input("Enter your choice: "))
            for item in self.main_menu_items:
                if item["option"] == choice:
                    item["function"]()
                    break
            else:
                print("Invalid choice. Please try again.")

    def handle_flights_menu(self):
        while True:
            self.display_menu(self.flights_menu_items)
            choice = int(input("Enter your choice for Flights Menu: "))
            for item in self.flights_menu_items:
                if item["option"] == choice:
                    item["function"]()
                    break
            else:
                print("Invalid choice. Please try again.")

    def handle_airports_menu(self):
        while True:
            self.display_menu(self.airports_menu_items)
            choice = int(input("Enter your choice for Airports Menu: "))
            for item in self.airports_menu_items:
                if item["option"] == choice:
                    item["function"]()
                    break
            else:
                print("Invalid choice. Please try again.")

    def handle_pilots_menu(self):
        while True:
            self.display_menu(self.pilots_menu_items)
            choice = int(input("Enter your choice for Pilots Menu: "))
            for item in self.pilots_menu_items:
                if item["option"] == choice:
                    item["function"]()
                    break
            else:
                print("Invalid choice. Please try again.")    

    def handle_summaries_menu(self):
        while True:
            self.display_menu(self.summary_menu_items)
            choice = int(input("Enter your choice for Summaries Menu: "))
            for item in self.summary_menu_items:
                if item["option"] == choice:
                    item["function"]()
                    break
            else:
                print("Invalid choice. Please try again.")    


    def handle_schedules_menu(self):
        print("Schedules Menu is not implemented yet.")
        # Placeholder for future implementation

# Flights Menu Functions

    def view_flights_by_criteria(self):
        self.flight_info.view_flights_by_criteria()
        
    def create_flight(self):
        self.flight_info.create_flight()
    
    def update_flight_information(self):
        self.flight_info.update_flight_information()
    
    def delete_flight(self):
        self.flight_info.delete_flight()
    
    def show_all_flights(self):
        self.flight_info.view_all_flights()

# Pilots Menu Functions

    def show_all_pilots(self):
        self.pilots.view_all_pilots()

    def view_pilots(self):
        self.pilots.view_pilot()
    
    def add_pilot(self):
        self.pilots.add_pilot()
    
    def update_pilot_information(self):
        self.pilots.update_pilot_information()
    
    def delete_pilot(self):
        self.pilots.delete_pilot()

    def assign_pilot_to_flight(self):
        self.pilots.assign_pilot_to_flight()

    def remove_pilot_from_flight(self):
        self.pilots.remove_pilot_from_flight()
    
    def get_pilot_schedule(self):
        self.pilots.get_pilot_schedule()
    
# Airports Menu Functions

    def view_airports(self):
        self.airports.view_airports()
    
    def add_airport(self):
        self.airports.add_airport()

    def update_airport_information(self):
        self.airports.update_airport_information()
    
    def delete_airport(self):
        self.airports.delete_airport()

# Summaries Menu Functions
    def summaries_destination_airport(self):
        self.summaries.summaries_destination_airport()

    def summaries_departure_airport(self):
        self.summaries.summaries_departure_airport()

    def summaires_flights_by_pilot(self):
        self.summaries.summaires_flights_by_pilot()

    def summaries_scheduled_flights(self):
        self.summaries.summaries_scheduled_flights()

    def summaries_cancelled_flights(self):
        self.summaries.summaries_cancelled_flights()
    
    def summaries_pilots_assigned_to_flights(self):
        self.summaries.summaries_pilots_assigned_to_flights()

    

# Generic
  
    def go_back_to_main_menu(self):
        print("Returning to Main Menu...")
        self.handle_main_menu()

    def exit_program(self):
        print("Exiting program...")
        self.db_operations.close()
        exit()
