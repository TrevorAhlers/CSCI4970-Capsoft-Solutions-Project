# Makes frequency maps for historical assignment logic

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

#.........................................................................
def split_rooms(room):
	"""
	Splits a room string into a list of individual room names
	"""

	if not isinstance(room, str):
		room = str(room) if pd.notna(room) else ""
	if ';' in room:
		return [r for r in room.split("; ") if r != 'Partially Online']
	return [room] if room else []

#.........................................................................
def map_assignment_freq(filenames: List[str]) -> Dict[str, Dict[str, int]]:
	"""
	Builds a dict map of how often each CourseSection is assigned to specific rooms
	"""

	output_map: Dict[str, Dict[str, int]] = {}

	for filename in filenames:
		base_dir = os.path.dirname(__file__)
		input_csv_file = os.path.join(os.path.dirname(base_dir), 'Files', filename)
		df = pd.read_csv(input_csv_file, skiprows=2, header=0)

		for _, row in df.iterrows():
			subj = str(row.get("Subject Code", ""))
			num = str(row.get("Catalog Number", ""))
			section_str = strip_decimal(str(row.get("Section #", "")))
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

#.........................................................................
def map_department_freq(filenames: List[str]) -> Dict[str, Dict[str, int]]:
	"""
	Builds a dict map showing how often each department is used for each room
	"""

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

#.........................................................................
def strip_decimal(attribute: str) -> str:
	"""
	Removes any .0 values from numbers like 1.0
	"""
	return attribute[:-2] if attribute.endswith(".0") else attribute