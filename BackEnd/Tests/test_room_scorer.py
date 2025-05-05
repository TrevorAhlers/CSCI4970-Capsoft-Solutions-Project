import pytest
import os
import sys
import pandas as pd
from unittest.mock import patch, MagicMock

# Add the path for the Controller module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Controller.room_scorer import split_rooms, map_assignment_freq, map_department_freq, make_int_str


# Test the split_rooms function
def test_split_rooms():
    # Test a string with multiple rooms
    room = "Peter Kiewit Institute 101; Peter Kiewit Institute 102"
    result = split_rooms(room)
    assert result == ["Peter Kiewit Institute 101", "Peter Kiewit Institute 102"], f"Expected ['Peter Kiewit Institute 101', 'Peter Kiewit Institute 102'], got {result}"

    # Test a string with a single room
    room = "Peter Kiewit Institute 101"
    result = split_rooms(room)
    assert result == ["Peter Kiewit Institute 101"], f"Expected ['Peter Kiewit Institute 101'], got {result}"

    # Test an empty room
    room = ""
    result = split_rooms(room)
    assert result == [], f"Expected [], got {result}"

    # Test a non-string value
    room = None
    result = split_rooms(room)
    assert result == [], f"Expected [], got {result}"

    # Test a case where 'Partially Online' is present
    room = "Peter Kiewit Institute 101; Partially Online; Peter Kiewit Institute 102"
    result = split_rooms(room)
    assert result == ["Peter Kiewit Institute 101", "Peter Kiewit Institute 102"], f"Expected ['Peter Kiewit Institute 101', 'Peter Kiewit Institute 102'], got {result}"


@patch("pandas.read_csv")
def test_map_assignment_freq(mock_read_csv):
    # Mock DataFrame with rooms containing "Peter Kiewit Institute"
    data = {
        "Subject Code": ["CS", "MATH", "CS"],
        "Catalog Number": ["101", "201", "102"],
        "Section #": ["1", "2", "1"],
        "Room": [
            "Peter Kiewit Institute 101; Peter Kiewit Institute 156; Peter Kiewit Institute 102",
            "Peter Kiewit Institute 103", 
            "Peter Kiewit Institute 252"
        ],
    }
    df_mock = pd.DataFrame(data)
    mock_read_csv.return_value = df_mock

    filenames = ["mock_file.csv"]
    result = map_assignment_freq(filenames)

    # The expected result should now include the specific rooms
    expected_result = {
        "CS 101-1": {"Peter Kiewit Institute 101": 1, "Peter Kiewit Institute 156": 1, "Peter Kiewit Institute 102": 1},
        "MATH 201-2": {"Peter Kiewit Institute 103": 1},
        "CS 102-1": {"Peter Kiewit Institute 252": 1},
    }
    
    # Assert that the result matches the expected result
    assert result == expected_result, f"Expected {expected_result}, got {result}"



@patch("pandas.read_csv")
def test_map_department_freq(mock_read_csv):
    # Mock DataFrame with rooms and subject codes, including "Peter Kiewit Institute"
    data = {
        "Subject Code": ["CS", "MATH", "CS"],
        "Catalog Number": ["101", "201", "102"],
        "Section #": ["1", "2", "1"],
        "Room": [
            "Peter Kiewit Institute 101; Peter Kiewit Institute 245; Peter Kiewit Institute 102",
            "Peter Kiewit Institute 103", 
            "Peter Kiewit Institute 252"
        ],
    }
    df_mock = pd.DataFrame(data)
    mock_read_csv.return_value = df_mock

    filenames = ["mock_file.csv"]
    result = map_department_freq(filenames)

    # Adjusted expected result based on the mock data
    expected_result = {
        "Peter Kiewit Institute 101": {"CS": 1},  # CS appears in Room 101
        "Peter Kiewit Institute 102": {"CS": 1},  # CS appears in Room 102
        "Peter Kiewit Institute 103": {"MATH": 1},  # MATH appears in Room 103
        "Peter Kiewit Institute 245": {"CS": 1},  # CS appears in Room 245
        "Peter Kiewit Institute 252": {"CS": 1},  # CS appears in Room 252
    }
    
    # Assert that the result matches the expected result
    assert result == expected_result, f"Expected {expected_result}, got {result}"



# Test the make_int_str function
def test_make_int_str():
    # Test with a string ending in ".0"
    result = make_int_str("123.0")
    assert result == "123", f"Expected '123', got {result}"

    # Test with a string not ending in ".0"
    result = make_int_str("123")
    assert result == "123", f"Expected '123', got {result}"

    # Test with a string with a different format
    result = make_int_str("001.0")
    assert result == "001", f"Expected '001', got {result}"


# Run the tests
if __name__ == "__main__":
    pytest.main()
