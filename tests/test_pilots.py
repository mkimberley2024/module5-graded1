import pytest
from unittest.mock import patch, MagicMock
from pilots import Pilots
import sqlite3

@pytest.fixture
def pilots_instance():
    pilots = Pilots("test.db")
    pilots.db_ops = MagicMock()
    return pilots

def test_assign_pilot_to_flight_valid(monkeypatch, pilots_instance):
    inputs = iter(["12", "5"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    pilots_instance.db_ops.execute_query = MagicMock()

    pilots_instance.assign_pilot_to_flight()

    # Get the actual call
    actual_call = pilots_instance.db_ops.execute_query.call_args
    assert "INSERT INTO flight_pilot" in actual_call[0][0]
    assert actual_call[0][1] == ("12", "5")

@pytest.mark.parametrize("inputs,validate_side_effect", [
    (["12", "999"], Exception("Pilot does not exist")),      # Non-existent pilot_id
    (["NOFLIGHT", "5"], Exception("Flight does not exist")), # Non-existent flight_number
])
def test_assign_pilot_to_flight_invalid(monkeypatch, pilots_instance, capsys, inputs, validate_side_effect):
    monkeypatch.setattr("builtins.input", lambda _: inputs.pop(0))
    pilots_instance.db_ops.execute_query = MagicMock()
    pilots_instance.db_ops.validate_fields.side_effect = validate_side_effect

    pilots_instance.assign_pilot_to_flight()
    captured = capsys.readouterr()
    assert "Error assigning pilot to flight:" in captured.out
    pilots_instance.db_ops.execute_query.assert_not_called()

def test_assign_pilot_to_flight_duplicate(monkeypatch, pilots_instance, capsys):
    # Simulate user input
    inputs = iter(["BA101", "1"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    # Mock validate_fields to pass
    pilots_instance.db_ops.validate_fields.return_value = True

    # Mock execute_query to raise IntegrityError
    pilots_instance.db_ops.execute_query.side_effect = sqlite3.IntegrityError("UNIQUE constraint failed: flight_pilot.flight_id, flight_pilot.pilot_id")

    pilots_instance.assign_pilot_to_flight()
    captured = capsys.readouterr()
    assert "Error assigning pilot to flight: UNIQUE constraint failed: flight_pilot.flight_id, flight_pilot.pilot_id\n" in captured.out

def assign_pilot_to_flight(self):
    flight_number = input("Enter Flight Number: ")
    pilot_id = input("Enter Pilot ID: ")

    # Optionally, check if pilot_id is numeric
    if not pilot_id.isdigit():
        print("Invalid Pilot ID. Please enter a valid number.")
        return

    # Validate pilot_id and flight_number
    validations = [
        {"table": "pilot", "column": "pilot_id", "value": pilot_id, "validation_type": "existing"},
        {"table": "flights", "column": "flight_number", "value": flight_number, "validation_type": "existing"},
    ]
    try:
        self.db_ops.validate_fields(validations)
    except Exception as e:
        print(f"Invalid Flight Number or Pilot ID: {e}")
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
    except sqlite3.IntegrityError:
        print("Pilot is already assigned to this flight")