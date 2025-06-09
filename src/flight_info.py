from db_operations import DBOperations
from tabulate import tabulate
from common import Common
import textwrap

class FlightInfo:

  def __init__(self, db_filename):
    self.db_ops = DBOperations(db_filename)
    self.db_ops.connect()

  def set_flight_id(self, flightID):
    self.flightID = flightID

  def set_flight_origin(self, flightOrigin):
    self.flight_origin = flightOrigin

  def set_flight_destination(self, flightDestination):
    self.flight_destination = flightDestination

  def set_status(self, status):
    self.status = status

  def get_flight_id(self):
    return self.flightID

  def get_flight_origin(self):
    return self.flightOrigin

  def get_airport_name(self, airportId):
    pass
  

  def get_status(self):
    return self.status

  def __str__(self):
    return str(
      self.flightID
    ) + "\n" + self.flightOrigin + "\n" + self.flightDestination + "\n" + str(
      self.status)
  
  def create_flight(self):
    print("Creating a new flight...")
    flight_number = input("Enter flight number: ")
    departure_airport_name = input("Enter departure airport name: ")
    arrival_airport_name = input("Enter arrival airport name: ")
    departure_time = input("Enter departure time (YYYY-MM-DD HH:MM:SS): ")
    arrival_time = input("Enter arrival time (YYYY-MM-DD HH:MM:SS): ")
    aircraft_id = input("Enter aircraft ID: ")
    status = input("Enter flight status: ")

    # Validate aircraft_id and flight_number
    validations = [
        {"table": "aircraft", "column": "aircraft_id", "value": aircraft_id, "validation_type": "existing"},
        {"table": "flights", "column": "flight_number", "value": flight_number, "validation_type": "unique"},
        {"table": "airports", "column": "airport_name", "value": departure_airport_name, "validation_type": "existing"},
        {"table": "airports", "column": "airport_name", "value": arrival_airport_name, "validation_type": "existing"}
    ]
    try:
        self.db_ops.validate_fields(validations)
    except ValueError as e:
        print(f"Validation error: {e}")
        return


    query = textwrap.dedent("""
    INSERT INTO flights (
        flight_number, departure_airport_id, arrival_airport_id, 
        departure_time, arrival_time, aircraft_id, status
    )
    VALUES (
        ?, 
        (SELECT airport_id FROM airports WHERE airport_name = ?),
        (SELECT airport_id FROM airports WHERE airport_name = ?),
        ?, ?, ?, ?
    );
    """)

    params = (
        flight_number,
        departure_airport_name,
        arrival_airport_name,
        departure_time,
        arrival_time,
        aircraft_id,
        status
    )
    try:
        self.db_ops.execute_query(query, params)
        print("Flight created successfully.")
    except ValueError as e:
        print(f"Error: {e}")
        raise
    except sqlite3.IntegrityError as e:
        print(f"Database error: {e}")
        raise

  def update_flight_information(self):
    try:
        flight_number = input("Enter the Flight Number to update: ")
        if not self.db_ops.check_validation("flights", "flight_number", flight_number):
            print(f"Flight Number {flight_number} does not exist. Valid Flight Numbers are:")
            self.view_all_flights()
            return

        fields_to_update = {
            "flight_number": input("Enter new flight number (leave blank to keep current): "),
            "departure_airport_id": input("Enter new departure airport ID (leave blank to keep current): "),
            "arrival_airport_id": input("Enter new arrival airport ID (leave blank to keep current): "),
            "departure_time": input("Enter new departure time (YYYY-MM-DD HH:MM:SS, leave blank to keep current): "),
            "arrival_time": input("Enter new arrival time (YYYY-MM-DD HH:MM:SS, leave blank to keep current): "),
            "aircraft_id": input("Enter new aircraft ID (leave blank to keep current): "),
            "status": input("Enter new flight status (leave blank to keep current): "),
        }

        # Validate fields that are not empty
        validations = []
        if fields_to_update["departure_airport_id"]:
            validations.append({"table": "airports", "column": "airport_id", "value": fields_to_update["departure_airport_id"], "validation_type": "existing"})
        if fields_to_update["arrival_airport_id"]:
            validations.append({"table": "airports", "column": "airport_id", "value": fields_to_update["arrival_airport_id"], "validation_type": "existing"})
        if fields_to_update["aircraft_id"]:
            validations.append({"table": "aircraft", "column": "aircraft_id", "value": fields_to_update["aircraft_id"], "validation_type": "existing"})

        self.db_ops.validate_fields(validations)

        updates, params = Common.prepare_updates(fields_to_update)
        if not updates:
            print("No fields to update.")
            return

        params.append(flight_number)  # Add flight_id for the WHERE clause
        update_query = f"UPDATE flights SET {', '.join(updates)} WHERE flight_number = ?;"

        self.db_ops.execute_query(update_query, tuple(params))
        print(f"Flight {flight_number} updated successfully.")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")



  def view_flights_by_criteria(self):
    criteria_menu = [
        {"option": 1, "description": "By Flight ID", "column": "flights.flight_id"},
        {"option": 2, "description": "By Aircraft Registration", "column": "aircraft.registration_number"},
        {"option": 3, "description": "By Destination Airport", "column": "arrival_airport.airport_name"},
        {"option": 4, "description": "By Departure Airport", "column": "departure_airport.airport_name"},
        {"option": 5, "description": "By Status", "column": "flights.status"},
        {"option": 6, "description": "By Departure Time", "column": "flights.departure_time"},
        {"option": 7, "description": "By Arrival Time", "column": "flights.arrival_time"},
        {"option": 8, "description": "By Flight Number", "column": "flights.flight_number"},
    ]

    # Use the Common class to get the user's selection
    selection = Common.get_criteria_selection(criteria_menu)
    if not selection:
        return

    selected_criteria, search_value = selection

    query = f"""
    SELECT 
        flights.flight_id,
        flights.flight_number,
        departure_airport.airport_name AS departure_airport_name,
        arrival_airport.airport_name AS arrival_airport_name,
        flights.departure_time,
        flights.arrival_time,
        flights.status,
        aircraft.model AS aircraft_model,
        aircraft.registration_number AS aircraft_registration
    FROM 
        flights
    JOIN 
        airports AS departure_airport ON flights.departure_airport_id = departure_airport.airport_id
    JOIN 
        airports AS arrival_airport ON flights.arrival_airport_id = arrival_airport.airport_id
    JOIN 
        aircraft ON flights.aircraft_id = aircraft.aircraft_id
    WHERE 
        {selected_criteria['column']} = ?;
    """

    try:
        results = self.db_ops.execute_query(query, (search_value,))
        if results:
            headers = [
                "Flight ID", "Flight Number", "Departure Airport", "Arrival Airport",
                "Departure Time", "Arrival Time", "Status", "Aircraft Model", "Aircraft Registration"
            ]
            table = tabulate(results, headers=headers, tablefmt="grid")
            print(table)
        else:
            print("No flights found matching the given criteria.")
    except Exception as e:
        print(f"Error retrieving flights: {e}")

  def view_all_flights(self):

    query = """
      SELECT 
          flights.flight_id,
          flights.flight_number,
          departure_airport.airport_name AS departure_airport_name,
          arrival_airport.airport_name AS arrival_airport_name,
          flights.departure_time,
          flights.arrival_time,
          flights.status,
          aircraft.model AS aircraft_model,
          aircraft.registration_number AS aircraft_registration
      FROM 
          flights
      JOIN 
          airports AS departure_airport ON flights.departure_airport_id = departure_airport.airport_id
      JOIN 
          airports AS arrival_airport ON flights.arrival_airport_id = arrival_airport.airport_id
      JOIN 
          aircraft ON flights.aircraft_id = aircraft.aircraft_id;
      """

    results = self.db_ops.execute_query(query)  # Use DBOperations to execute query

    if results:
        headers = [
            "Flight ID", "Flight Number", "Departure Airport", "Arrival Airport",
            "Departure Time", "Arrival Time", "Status", "Aircraft Model", "Aircraft Registration"
        ]
        table = tabulate(results, headers=headers, tablefmt="grid")
        print(table)
    else:
          print("No flights found.")
     

  def delete_flight(self):
    try:
        flight_number = input("Enter the Flight Number to delete: ")
        # Get the flight_id for the given flight_number
        flight_id_query = "SELECT flight_id FROM flights WHERE flight_number = ?;"
        cursor = self.db_ops.execute_query(flight_id_query, (flight_number,))
        result = cursor.fetchall()
        if not result:
            print(f"Flight Number {flight_number} does not exist. Valid Flight Numbers are:")
            self.view_all_flights()
            return
        flight_id = result[0][0]

        # Delete related records in child tables
        self.db_ops.execute_query("DELETE FROM flight_pilot WHERE flight_id = ?;", (flight_id,))

        # Now delete the flight itself
        self.db_ops.execute_query("DELETE FROM flights WHERE flight_number = ?;", (flight_number,))
        print(f"Flight {flight_number} deleted successfully.")
    except Exception as e:
        print(f"Error deleting flight: {e}")