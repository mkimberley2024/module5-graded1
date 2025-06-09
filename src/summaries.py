from db_operations import DBOperations
from tabulate import tabulate
from common import Common
import sqlite3


class Summaries:

    def __init__(self, db_filename):
        self.db_ops = DBOperations(db_filename)
        self.db_ops.connect()

    def summaries_destination_airport(self):
        criteria_menu = [
            {"option": 1, "description": "By Airport Name", "column": "airport_name"},
            {"option": 2, "description": "By Airport Code", "column": "airport_code"},
        ]
        selection = Common.get_criteria_selection(criteria_menu)
        if not selection:
            return

        selected_criteria, value = selection
        print(f"Selected criteria: {selected_criteria['column']} with value '{value}'")

        validations = []
        if selected_criteria['column'] == "airport_code":
            validations.append({"table": "airports", "column": "airport_code", "value": value, "validation_type": "existing"})
        elif selected_criteria['column'] == "airport_name":
            validations.append({"table": "airports", "column": "airport_name", "value": value, "validation_type": "existing"})

        try:
            self.db_ops.validate_fields(validations)
        except ValueError as e:
            print(f"Validation error: {e}")
            return
        
        query = f"""
        SELECT f.flight_number, f.departure_time, f.arrival_time, f.status
        FROM flights f
        JOIN airports a ON f.arrival_airport_id = a.airport_id
        WHERE a.{selected_criteria['column']} = ?
        ORDER BY f.departure_time;
        """
        result = self.db_ops.execute_query(query, (value,))
        if result:
            print(f"Flights to {value}:")    
            print(tabulate(result, headers=["Flight Number", "Departure Time", "Arrival Time", "Status"], tablefmt="grid"))
        else:
            print(f"No flights found for {selected_criteria['column']} '{value}'.")

    def summaries_departure_airport(self):
        
        criteria_menu = [
            {"option": 1, "description": "By Airport Name", "column": "airport_name"},
            {"option": 2, "description": "By Airport Code", "column": "airport_code"},
        ]
        selection = Common.get_criteria_selection(criteria_menu)
        if not selection:
            return

        selected_criteria, value = selection
        print(f"Selected criteria: {selected_criteria['column']} with value '{value}'")

        validations = []
        if selected_criteria['column'] == "airport_code":
            validations.append({"table": "airports", "column": "airport_code", "value": value, "validation_type": "existing"})
        elif selected_criteria['column'] == "airport_name":
            validations.append({"table": "airports", "column": "airport_name", "value": value, "validation_type": "existing"})

        try:
            self.db_ops.validate_fields(validations)
        except ValueError as e:
            print(f"Validation error: {e}")
            return
        
        query = f"""
        SELECT f.flight_number, f.departure_time, f.arrival_time, f.status
        FROM flights f
        JOIN airports a ON f.departure_airport_id = a.airport_id
        WHERE a.{selected_criteria['column']} = ?
        ORDER BY f.departure_time;
        """
        result = self.db_ops.execute_query(query, (value,))
        if result:
            print(f"Flights from {value}:")    
            print(tabulate(result, headers=["Flight Number", "Departure Time", "Arrival Time", "Status"], tablefmt="grid"))
        else:
            print(f"No flights found for {selected_criteria['column']} '{value}'.")
    
    def summaires_flights_by_pilot(self):
        criteria_menu = [
            {"option": 1, "description": "By Pilot ID", "column": "pilot_id"},
            {"option": 2, "description": "By Pilot License Code", "column": "license_number"},
        ]
        selection = Common.get_criteria_selection(criteria_menu)
        if not selection:
            return

        selected_criteria, value = selection
        print(f"Selected criteria: {selected_criteria['column']} with value '{value}'")

        validations = []
        if selected_criteria['column'] == "pilot_id":
            validations.append({"table": "pilot", "column": "pilot_id", "value": value, "validation_type": "existing"})
        elif selected_criteria['column'] == "license_number":
            validations.append({"table": "pilot", "column": "license_number", "value": value, "validation_type": "existing"})

        try:
            self.db_ops.validate_fields(validations)
        except ValueError as e:
            print(f"Validation error: {e}")
            return

        query = f"""
        SELECT p.pilot_id, p.first_name, p.last_name, COUNT(fp.flight_id) AS flight_count
        FROM pilot p
        JOIN flight_pilot fp ON p.pilot_id = fp.pilot_id
        JOIN flights f ON fp.flight_id = f.flight_id
        WHERE p.{selected_criteria['column']} = ?
        GROUP BY p.pilot_id, p.first_name, p.last_name
        ORDER BY flight_count DESC;
        """
        result = self.db_ops.execute_query(query, (value,))
        if result:
            print(f"Flights for pilot {value}:")    
            print(tabulate(result, headers=["Pilot ID", "First Name", "Last Name", "Flight Count"], tablefmt="grid"))
        else:
            print(f"No flights found for {selected_criteria['column']} '{value}'.")
    
    def summaries_pilots_assigned_to_flights(self):
        criteria_menu = [
            {"option": 1, "description": "By Flight Number", "column": "flight_number"},
            {"option": 2, "description": "By Flight ID", "column": "flight_id"},
        ]
        selection = Common.get_criteria_selection(criteria_menu)
        if not selection:
            return

        selected_criteria, value = selection
        print(f"Selected criteria: {selected_criteria['column']} with value '{value}'")

        validations = []
        if selected_criteria['column'] == "flight_number":
            validations.append({"table": "flights", "column": "flight_number", "value": value, "validation_type": "existing"})
        elif selected_criteria['column'] == "flight_id":
            validations.append({"table": "flights", "column": "flight_id", "value": value, "validation_type": "existing"})

        try:
            self.db_ops.validate_fields(validations)
        except ValueError as e:
            print(f"Validation error: {e}")
            return

        query = f"""
        SELECT p.pilot_id, p.first_name, p.last_name
        FROM pilot p
        JOIN flight_pilot fp ON p.pilot_id = fp.pilot_id
        JOIN flights f ON fp.flight_id = f.flight_id
        WHERE f.{selected_criteria['column']} = ?
        GROUP BY p.pilot_id, p.first_name, p.last_name
        ORDER BY p.last_name DESC;
        """
        result = self.db_ops.execute_query(query, (value,))
        if result:
            print(f"Pilots assigned to flight {value}:")    
            print(tabulate(result, headers=["Pilot ID", "First Name", "Last Name", "Flight Count"], tablefmt="grid"))
        else:
            print(f"No flights found for {selected_criteria['column']} '{value}'.")

    def summaries_scheduled_flights(self):

        query = """
        SELECT f.status AS flight_status, COUNT(*) AS flight_count
        FROM flights f
        WHERE f.status = 'Scheduled'
        GROUP BY f.status
        ORDER BY flight_count DESC;
        """
        result = self.db_ops.execute_query(query)
        if result:
            print("Scheduled Flights:")
            print(tabulate(result, headers=["Flight Status", "Count"], tablefmt="grid"))
        return
    
    def summaries_cancelled_flights(self):
        
        query = """
        SELECT f.status AS flight_status, COUNT(*) AS flight_count
        FROM flights f
        WHERE f.status = 'Cancelled'
        GROUP BY f.status
        ORDER BY flight_count DESC;
        """
        result = self.db_ops.execute_query(query)
        if result:
            print("Scheduled Flights:")
            print(tabulate(result, headers=["Flight Status", "Count"], tablefmt="grid"))
        return
