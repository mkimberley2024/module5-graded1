from db_operations import DBOperations
from tabulate import tabulate
from common import Common
import sqlite3

class Pilots:

    def __init__(self, db_filename):
        self.db_ops = DBOperations(db_filename)
        self.db_ops.connect()

    def view_all_pilots(self):
        query = """
        SELECT 
            pilot.pilot_id,
            pilot.first_name,
            pilot.last_name,
            pilot.license_number,
            pilot.contact_info
        FROM 
            pilot;
        """
        results = self.db_ops.execute_query(query)

        if results:
            headers = ["Pilot ID", "First Name", "Last Name", "License Number", "Contact Info"]
            table = tabulate(results, headers=headers, tablefmt="grid")
            print(table)
        else:
            print("No pilots found.")

    def view_pilot(self):
        criteria_menu = [
            {"option": 1, "description": "By Pilot ID", "column": "pilot.pilot_id"},
            {"option": 2, "description": "By Pilot First Name", "column": "pilot.first_name"},
            {"option": 3, "description": "By Pilot Last Name", "column": "pilot.last_name"},
            {"option": 4, "description": "By Pilot License Number", "column": "pilot.license_number"},
        ]
        selection = Common.get_criteria_selection(criteria_menu)
        if not selection:
            return

        selected_criteria, search_value = selection
        query = f"""
        SELECT             
            pilot.pilot_id,
            pilot.first_name,
            pilot.last_name,
            pilot.license_number,
            pilot.contact_info
        FROM 
            pilot
        WHERE 
            {selected_criteria['column']} = ?;
        """

        results = self.db_ops.execute_query(query, (search_value,))  # Use DBOperations to execute query

        if results:
            headers = [
                "Pilot ID", "First Name", "Last Name", "License Number", "Contact Info"
            ]
            table = tabulate(results, headers=headers, tablefmt="grid")
            print(table)
        else:
            print("No pilots found matching the given criteria.")

    def add_pilot(self):
        print("Adding Pilot...")
        first_name = input("Enter Pilot's First Name: ")
        last_name = input("Enter Pilot's Last Name: ")
        license_number = input("Enter Pilot's License Number: ")
        contact_info = input("Enter Pilot's Contact Information: ")

        query = """
        INSERT INTO pilot (first_name, last_name, license_number, contact_info)
        VALUES (?, ?, ?, ?);
        """
        self.db_ops.execute_query(query, (first_name, last_name, license_number, contact_info))
        print("Pilot added successfully.")
    
    def delete_pilot(self):
        pilot_id = input("Enter the Pilot ID to delete: ")
 
        # check the piloit_id exists
        if not self.db_ops.check_validation("pilot", "pilot_id", pilot_id):
            print(f"Pilot with ID {pilot_id} does not exist.")
            return
        
        # Remove pilot from all flights first
        self.db_ops.execute_query(
            "DELETE FROM flight_pilot WHERE pilot_id = ?;",
            (pilot_id,)
        )
        # Now delete the pilot
        self.db_ops.execute_query(
            "DELETE FROM pilot WHERE pilot_id = ?;",
            (pilot_id,)
        )
        print("Pilot deleted successfully.")
    
    def update_pilot_information(self):
        return
    
    def assign_pilot_to_flight(self):
        flight_number = input("Enter Flight Number: ")
        pilot_id = input("Enter Pilot ID: ")

        validations = [
            {"table": "pilot", "column": "pilot_id", "value": pilot_id, "validation_type": "existing"},
            {"table": "flights", "column": "flight_number", "value": flight_number, "validation_type": "unqiue"},
        ]
        try:
            self.db_ops.validate_fields(validations)
        except Exception as e:
            print(f"Error assigning pilot to flight: {e}")
            return

        query = """
                INSERT INTO flight_pilot (flight_id, pilot_id)
                VALUES (
                    (SELECT flight_id FROM flights WHERE flight_number = ?),
                    ?
                );
                """
        try:
            self.db_ops.execute_query(query, (flight_number, pilot_id))
            print(f"Pilot with ID {pilot_id} assigned to flight {flight_number} successfully.")
        except sqlite3.IntegrityError as e:
            print(f"Error assigning pilot to flight: {e}")
        
    def remove_pilot_from_flight(self):
        flight_number = input("Enter Flight Number: ")
        pilot_id = input("Enter Pilot ID: ")

        # Validate aircraft_id and flight_number
        validations = [
            {"table": "pilot", "column": "pilot_id", "value": pilot_id, "validation_type": "existing"},
            {"table": "flights", "column": "flight_number", "value": flight_number, "validation_type": "existing"},
        ]
        self.db_ops.validate_fields(validations)


        query = """
        DELETE FROM flight_pilot
        WHERE flight_id = (SELECT flight_id FROM flights WHERE flight_number = ?) AND pilot_id = ?;
        """
        self.db_ops.execute_query(query, (flight_number, pilot_id))
        print(f"Pilot with ID {pilot_id} removed from flight {flight_number} successfully.")
    
    def get_pilot_schedule(self):
        criteria_menu = [
            {"option": 1, "description": "By Pilot ID", "column": "pilot.pilot_id"},

        ]
        selection = Common.get_criteria_selection(criteria_menu)
        if not selection:
            return

        selected_criteria, search_value = selection
        query = """
                SELECT 
                    flights.flight_id,
                    flights.flight_number,
                    departure_airport.airport_name AS departure_airport_name,
                    arrival_airport.airport_name AS arrival_airport_name,
                    flights.departure_time,
                    flights.arrival_time,
                    flights.status AS flight_status,
                    aircraft.model AS aircraft_model,
                    aircraft.registration_number AS aircraft_registration,
                    pilot.pilot_id,
                    pilot.first_name AS pilot_first_name,
                    pilot.last_name AS pilot_last_name,
                    pilot.license_number AS pilot_license_number
                FROM 
                    flight_pilot
                JOIN 
                    flights ON flight_pilot.flight_id = flights.flight_id
                JOIN 
                    airports AS departure_airport ON flights.departure_airport_id = departure_airport.airport_id
                JOIN 
                    airports AS arrival_airport ON flights.arrival_airport_id = arrival_airport.airport_id
                JOIN 
                    aircraft ON flights.aircraft_id = aircraft.aircraft_id
                JOIN 
                    pilot ON flight_pilot.pilot_id = pilot.pilot_id
                WHERE 
                    flight_pilot.pilot_id = ?;
                """

        results = self.db_ops.execute_query(query, (search_value,))  # Use DBOperations to execute query

        if results:
            headers = [
                "Flight ID", "Flight Number", "Departure Airport", "Arrival Airport",
                "Departure Time", "Arrival Time", "Flight Status", "Aircraft Model",
                "Aircraft Registration", "Pilot ID", "Pilot Name", "Pilot Surname", "License Number", "Contact Info"
            ]
            table = tabulate(results, headers=headers, tablefmt="grid")
            print(table)
        else:
            print("No pilots found matching the given criteria.")


    def update_pilot_information(self):
        try:
            pilot_id = input("Enter Pilot ID to update: ")
            
            # Check if the pilot exists
            if not self.db_ops.check_validation("pilot", "pilot_id", pilot_id):
                print(f"Pilot with ID {pilot_id} does not exist.")

                return

            fields_to_update = {
                "first_name": input("Enter new First Name (leave blank to keep current): "),
                "last_name": input("Enter new Last Name (leave blank to keep current): "),
                "license_number": input("Enter new License Number (leave blank to keep current): "),
                "contact_info": input("Enter new Contact Information (leave blank to keep current): ")
            }

            validations = []
            if fields_to_update["first_name"]:
                validations.append({"table": "pilot", "column": "first_name", "value": fields_to_update["first_name"], "validation_type": "not_empty"})
            if fields_to_update["last_name"]:
                validations.append({"table": "pilot", "column": "last_name", "value": fields_to_update["last_name"], "validation_type": "not_empty"})
            if fields_to_update["license_number"]:
                validations.append({"table": "pilot", "column": "license_number", "value": fields_to_update["license_number"], "validation_type": "unique"})
            if fields_to_update["contact_info"]:
                validations.append({"table": "pilot", "column": "contact_info", "value": fields_to_update["contact_info"], "validation_type": "not_empty"})

            self.db_ops.validate_fields(validations)

            update, params = Common.prepare_updates(fields_to_update)
            if not update:
                print("No fields to update.")
                return
            
            params.append(pilot_id)  # Append pilot_id for the WHERE clause
            update_query = f"UPDATE pilot SET {', '.join(update)} WHERE pilot_id = ?;"
            self.db_ops.execute_query(update_query, params)
            print(f"Pilot with ID {pilot_id} updated successfully.")
        except ValueError as e:
            print(f"Error updating pilot: {e}")
            raise


