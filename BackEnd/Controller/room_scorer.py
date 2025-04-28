#####################################################################################
# 	Room Scorer
#
#	Assigns scores to rooms for each course-section, so we know historically which
#	assignments have worked in the past, and how often.
#
#....................................................................................

import os
import pandas as pd
from typing import Dict, List, Optional
from Model.CourseSection import CourseSection, CourseSectionEnum
from Model.Classroom import Classroom

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

def split_rooms(room):
	
	if not isinstance(room, str):
		room = str(room) if pd.notna(room) else ""
	if ';' in room:
		return [r for r in room.split("; ") if r != 'Partially Online']
	return [room] if room else []



import os
import pandas as pd
from typing import Dict, List

def split_rooms(room):
	"""
    Splits a room string into a list of individual room values.

    This function processes the room string by splitting it at semicolons (`;`) and excluding any 
    rooms marked as 'Partially Online'. If the room string is empty or None, it returns an empty list.

    Args:
        room (str): A string containing room information, potentially with multiple room values
                    separated by semicolons.

    Returns:
        List[str]: A list of room names. If the room string is empty or None, an empty list is returned.
    """
	if not isinstance(room, str):
		room = str(room) if pd.notna(room) else ""
	if ';' in room:
		return [r for r in room.split('; ') if r != 'Partially Online']
	return [room] if room else []


def map_assignment_freq(filenames: List[str]) -> Dict[str, Dict[str, int]]:
	"""
    Maps the frequency of room assignments for each course-section across multiple files.

    This function processes multiple CSV files containing course-section information and assigns
    scores (frequencies) to each room where a course-section was assigned. It counts how often each 
    room was assigned for each course-section and stores this data in a dictionary.

    Args:
        filenames (List[str]): A list of CSV file names to process. Each file contains course-section data.

    Returns:
        Dict[str, Dict[str, int]]: A nested dictionary where the first key is the unique course-section 
                                    identifier (subject code, catalog number, and section number),
                                    and the second key is the room name. The value is the frequency of
                                    assignments for that room and course-section.
    """
	output_map: Dict[str, Dict[str, int]] = {}

	for filename in filenames:
		base_dir = os.path.dirname(__file__)
		input_csv_file = os.path.join(os.path.dirname(base_dir), 'Files', filename)
		df = pd.read_csv(input_csv_file, skiprows=2, header=0)

		for _, row in df.iterrows():
			subj = str(row.get("Subject Code", ""))
			num = str(row.get("Catalog Number", ""))
			section_str = make_int_str(str(row.get("Section #", "")))
			key = f"{subj} {num}-{section_str}"

			ss_room = row.get("Room", "")
			rooms = split_rooms(ss_room)

			if key not in output_map:
				output_map[key] = {}

			for room in rooms:
				if "Peter Kiewit Institute" in room:
					freq = output_map[key].get(room, 0)
					output_map[key][room] = freq + 1

	return output_map

def map_department_freq(filenames: List[str]) -> Dict[str, Dict[str, int]]:
	output_map: Dict[str, Dict[str, int]] = {}

	for filename in filenames:
		base_dir = os.path.dirname(__file__)
		input_csv_file = os.path.join(os.path.dirname(base_dir), 'Files', filename)
		df = pd.read_csv(input_csv_file, skiprows=2, header=0)

		for _, row in df.iterrows():
			dept = str(row.get("Subject Code", ""))
			room_str = row.get("Room", "")
			rooms = split_rooms(room_str)

			for room in rooms:
				if "Peter Kiewit Institute" in room:
					if room not in output_map:
						output_map[room] = {}
					output_map[room][dept] = output_map[room].get(dept, 0) + 1

	return output_map


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
	return attribute[:-2] if attribute.endswith(".0") else attribute