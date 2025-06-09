import sqlite3
import logging

class DBOperations:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None

    def connect(self):
        self.connection = sqlite3.connect(self.db_name)
        self.connection.set_trace_callback(logging.info)

    def execute_query(self, query, params=()):
        if not self.connection:
            self.connect()
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        self.connection.commit()

        formatted_query = query
        for param in params:
            formatted_query = formatted_query.replace("?", f"'{param}'", 1)
        #logging.info(f"Executed query: {formatted_query.strip()}")

        return cursor

    def fetch_all(self, query, params=()):
        cursor = self.execute_query(query, params)
        return cursor.fetchall()

    def close(self):
        if self.connection:
            self.connection.close()

    def check_populated(self):
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name='flights';"
        cursor = self.execute_query(query)
        return cursor.fetchone() is not None
    
    def check_table_exists(self, table_name):
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name=?;"
        cursor = self.execute_query(query, (table_name,))
        return cursor.fetchone() is not None
    
    def check_validation(self, table, column, value):
        query = f"SELECT COUNT(*) FROM {table} WHERE {column} = ?;"
        logging.info(f"Executing validation query: {query} with value: {value}")
        cursor = self.execute_query(query, (value,))
        result = cursor.fetchone()  # Fetch the result from the cursor
        logging.info(f"Validation result: {result}")
        return result[0] > 0 if result else False

    def print_all(self, table_name):
        query = f"SELECT * FROM {table_name};"
        results = self.fetch_all(query)
        if results:
            for row in results:
                print(row)
        else:
            print(f"No records found in {table_name}.")
        logging.info(f"Printed all records from {table_name}.")

    def validate_fields(self, validations):
        for validation in validations:
            query = f"SELECT COUNT(*) FROM {validation['table']} WHERE {validation['column']} = ?;"
            cursor = self.execute_query(query, (validation["value"],))
            result = cursor.fetchone()
            is_valid = result[0] > 0 if result else False

            if validation["validation_type"] == "existing" and not is_valid:
                raise ValueError(
                    f"Validation failed: {validation['value']} does not exist in {validation['table']}.{validation['column']}."
                )
            elif validation["validation_type"] == "unique" and is_valid:
                raise ValueError(
                    f"Validation failed: {validation['value']} already exists in {validation['table']}.{validation['column']}."
                )
            elif validation["validation_type"] == "not_empty" and not validation["value"]:
                raise ValueError(
                    f"Validation failed: {validation['column']} cannot be empty."
                )
