#####################################################################################
# 	Classroom Object Instantiation
# 
#
#....................................................................................

import csv
import os
import pandas as pd
import re
from typing import Dict, List, Optional
from Model.Classroom import Classroom, ClassroomEnum
from Model.CourseSection import CourseSection, CourseSectionEnum

def build_classrooms(filename: str, sections: Dict[str, CourseSection]) -> Dict[str, Classroom]:
	"""
    Builds a dictionary of Classroom objects from a CSV file and integrates course section assignments.

    Args:
        filename (str): The path to the CSV file containing classroom data.
        sections (Dict[str, CourseSection]): A dictionary of CourseSection objects representing scheduled courses.

    Returns:
        Dict[str, Classroom]: A dictionary mapping room numbers to Classroom objects.

    Functionality:
        - Reads classroom data from a CSV file.
        - Instantiates Classroom objects and assigns default values for missing attributes.
        - Adds missing classrooms from the course section data.
        - Associates sections with classrooms based on room assignments.
        - Prints the total number of classroom objects created.
    """

	classroom_keys = []

	df = pd.read_csv(filename, header=0)
	classrooms: Dict[str, Classroom] = {}

	for _, row in df.iterrows():
		row_data: Dict[str, str] = {}
		for enum_col in ClassroomEnum:
			if enum_col.value in df.columns:
				cell_value = row[enum_col.value]
				cell_str = str(cell_value) if pd.notna(cell_value) else ""
				row_data[enum_col.value] = cell_str

		room_num_str = row_data.get("Room Number", "")
		tokens = room_num_str.split()
		key = tokens[-1] if tokens else room_num_str
		key = "Peter Kiewit Institute " + key

		cl = Classroom(row_data)
		classroom_keys.append(cl.room)

		# Default object values
		if not cl.seats:
			cl.seats = "N/A"
		if not cl.computer_count:
			cl.computer_count = "N/A"
		if not cl.displays:
			cl.displays = "N/A"
		if not cl.info_and_connectivity:
			cl.info_and_connectivity = "N/A"

		classrooms[key] = cl

	for _,section in sections.items():
		for section_room in section.rooms:
			if section_room not in classroom_keys and section_room != 'To Be Announced':
				row_data = {
					"Room Number": section_room,
					"Seats": "N/A",
					"Displays": "N/A",
					"Computer Count": "N/A",
					"Information and Connectivity": "N/A",
					"Assigned": True,
				}
				classrooms[section_room] = Classroom(row_data)


	for _, section in sections.items():
		for section_room in section.rooms:
			if section_room in classrooms and section_room != 'To Be Announced':
				classrooms[section_room].add_course_section_object(section)

	print(f"classroom_factory.py: Built {len(classrooms)} Classroom objects.")


	return classrooms