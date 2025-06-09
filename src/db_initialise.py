import sqlite3
import os
import csv
import logging
from db_operations import DBOperations

def create_schema(db_filename):
    db_ops = DBOperations(db_filename)
    db_ops.connect()

    schema = [
        """
        CREATE TABLE IF NOT EXISTS airports (
            airport_id INTEGER PRIMARY KEY AUTOINCREMENT,
            airport_code TEXT UNIQUE NOT NULL,
            airport_name TEXT NOT NULL,
            city TEXT NOT NULL,
            country TEXT NOT NULL
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS aircraft (
            aircraft_id INTEGER PRIMARY KEY AUTOINCREMENT,
            registration_number TEXT UNIQUE NOT NULL,
            model TEXT NOT NULL,
            capacity INTEGER NOT NULL,
            status TEXT NOT NULL
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS pilot (
            pilot_id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            license_number TEXT UNIQUE NOT NULL,
            contact_info TEXT
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS flights (
            flight_id INTEGER PRIMARY KEY AUTOINCREMENT,
            flight_number TEXT UNIQUE NOT NULL,
            departure_airport_id INTEGER REFERENCES airports(airport_id),
            arrival_airport_id INTEGER REFERENCES airports(airport_id),
            departure_time TIMESTAMP NOT NULL,
            arrival_time TIMESTAMP NOT NULL,
            aircraft_id INTEGER REFERENCES aircraft(aircraft_id),
            status TEXT NOT NULL
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS flight_pilot (
            flight_id INTEGER PRIMARY KEY REFERENCES flights(flight_id),
            pilot_id INTEGER REFERENCES pilot(pilot_id)
        );

        """
    ]

    for query in schema:
        db_ops.execute_query(query)
    db_ops.close()


def insert_data(db_filename):
    db_ops = DBOperations(db_filename)
    db_ops.connect()

    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, 'tsv')  

    for filename in os.listdir(data_dir):
        if filename.endswith('.tsv'):  
            table_name = filename[:-4]  
            file_path = os.path.join(data_dir, filename)

            with open(file_path, 'r') as file:
                reader = csv.DictReader(file, delimiter='\t')  
                for row in reader:
                    columns = ', '.join(row.keys())
                    placeholders = ', '.join(['?' for _ in row.keys()])
                    values = tuple(row.values())

                    query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
                    db_ops.execute_query(query, values)

    db_ops.close()

def initialise_database(db_filename):
    db_ops = DBOperations(db_filename)
    db_ops.connect()
    if not db_ops.check_populated():
        if not db_ops.check_table_exists('flights'):
            create_schema(db_filename)
        insert_data(db_filename)
    else:
        logging.info("Database already populated with data.")


