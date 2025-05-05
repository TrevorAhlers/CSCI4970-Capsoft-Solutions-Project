import csv
import pandas as pd
import tempfile
import os
import pytest
from typing import Dict

# Add the path for the Controller module
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Controller.exporter import update_csv_with_room, make_int_str

# A lightweight mock for CourseSection
class FakeCourseSection:
    def __init__(self, rooms):
        self.rooms = rooms

def test_update_csv_with_room():
    # Sample input data
    csv_content = '''Some header info to skip
Another header row
"Subject Code","Catalog Number","Section #","Room"
"CS","101","1",""
"MATH","201","2",""
"CS","102","3",""
'''


    # Fake CourseSection dict with room assignments
    sections: Dict[str, FakeCourseSection] = {
        "CS 101-1": FakeCourseSection(["Peter Kiewit Institute 101"]),
        "CS 102-3": FakeCourseSection(["Peter Kiewit Institute 252", "Peter Kiewit Institute 253"]),
    }

    with tempfile.TemporaryDirectory() as tmpdirname:
        input_path = os.path.join(tmpdirname, "input.csv")
        output_path = os.path.join(tmpdirname, "output.csv")

        # Write the test CSV input file
        with open(input_path, "w") as f:
            f.write(csv_content)

        # Call the function being tested
        update_csv_with_room(input_path, output_path, sections)

        # Read the result into a DataFrame
        result_df = pd.read_csv(output_path)

        # Verify the result
        assert result_df.loc[0, "Room"] == "Peter Kiewit Institute 101"
        assert pd.isna(result_df.loc[1, "Room"])
        assert result_df.loc[2, "Room"] == "Peter Kiewit Institute 252; Peter Kiewit Institute 253"

def test_make_int_str():
    # Should strip ".0" from the end
    assert make_int_str("123.0") == "123"
    assert make_int_str("001.0") == "001"

    # Should leave strings without ".0" unchanged
    assert make_int_str("123") == "123"
    assert make_int_str("0") == "0"
    assert make_int_str("abc") == "abc"

    # Should not break on short strings
    assert make_int_str("") == ""
    assert make_int_str(".0") == ""  # technically matches `.0`