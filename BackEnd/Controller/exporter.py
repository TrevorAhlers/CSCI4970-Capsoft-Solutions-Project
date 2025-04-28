from typing import Dict
from Model.Classroom import Classroom
from Model.CourseSection import CourseSection
import pandas as pd
import csv

float_headers = [
	"Section #",
	"Credit Hrs Min",
	"Credit Hrs",
	"Enrollment",
	"Maximum Enrollment",
	"Wait Cap",
	"Rm Cap Request",
	"Cross-list Maximum",
	"Cross-list Wait Cap",
	"Cross-list Rm Cap Request",
]

def update_csv_with_room(input_file: str, output_file: str, sections: Dict[str, CourseSection]) -> None:
	"""
    Updates a CSV file with room information based on sections.

    This function reads an input CSV file, processes the section data, and then writes a new CSV
    file that includes room information from the `sections` dictionary. It updates the "Room" column 
    for each section if the section exists in the `sections` dictionary.

    Args:
        input_file (str): Path to the input CSV file that contains course data.
        output_file (str): Path where the updated CSV file with room information will be saved.
        sections (Dict[str, CourseSection]): A dictionary where the key is a unique section identifier
    	(e.g., "SubjectCode CatalogNumber-SectionNumber"),
        and the value is a `CourseSection` object containing the room(s) information.

    Returns:
        None: The function modifies the output file and does not return any value.
    """
	df = pd.read_csv(input_file, skiprows=2, header=0)
	# non NaN values... use empty strings
	df = df.fillna("")
	
	if "Room" in df.columns:
		df["Room"] = df["Room"].astype(str)
	else:
		df["Room"] = ""
	
	# update rooms as information allows
	for idx, row in df.iterrows():
		subject_code = str(row.get("Subject Code", "")).strip()
		catalog_number = str(row.get("Catalog Number", "")).strip()
		section_number = make_int_str(str(row.get("Section #", "")).strip())
		key = f"{subject_code} {catalog_number}-{section_number}"
		
		if key in sections:
			rooms = sections[key].rooms
			# koin room numbers
			room_update_str = "; ".join(rooms)
			df.at[idx, "Room"] = room_update_str
	
	# write to csv
	df.to_csv(output_file, index=False, quoting=csv.QUOTE_ALL)

def make_int_str(attribute: str) -> str:
	"""
    Converts a string representing a float (ending in .0) to an integer string.

    If the input string represents a floating-point number with a ".0" suffix, it removes the 
    ".0" and returns the integer part as a string. If there is no ".0", it simply returns the original string.

    Args:
        attribute (str): The string to be processed, potentially representing a float.

    Returns:
        str: The processed string, which is either the original string or a string without ".0".
    """
	if attribute.endswith(".0"):
		attribute = attribute[:-2]
		return attribute
	return attribute