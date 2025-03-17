#####################################################################################
# 	CourseSection Object Instantiation
#
#
#	Data extraction from input CSV and preparing the data to populate class objects.
#	All functions skip the first two lines of the file and treat the third line
#	as the header row (skiprows=2, header=0).
#
#	Builds a dictionary of CourseSection objects keyed by columns: "Catalog Number"
# 	[hyphen] "Section #""
#
#	Example: course_sections["1030-1"] = new CourseSection(inputDictionary)
# 
# 	We use the course_sections dictionary to look-up a CourseSection Object by
# 	its course code with its section number.
#....................................................................................

import csv
import os
import pandas as pd
import re
from typing import Dict, List, Optional
from p_CourseSection import CourseSection, CourseSectionEnum

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


#....................................................................................
#####################################################################################
# 	Reads the CSV and creates a dictionary of CourseSection 
# objects. Each entry is keyed by "Catalog Number-Section #", for example "1030-1".
#....................................................................................
def build_course_sections(filename: str) -> Dict[str, CourseSection]:
	df = pd.read_csv(filename, skiprows=2, header=0)
	course_sections: Dict[str, CourseSection] = {}

	for _, row in df.iterrows():
		row_data: Dict[str, str] = {}
		for enum_col in CourseSectionEnum:
			if enum_col.value in df.columns:
				cell_value = row[enum_col.value]
				cell_str = str(cell_value) if pd.notna(cell_value) else ""

				# We make_int() if it can be a value that ends in ".0", which we
				# don't want.
				if enum_col.value in float_headers:
					row_data[enum_col.value] = make_int(cell_str)
				else:
					row_data[enum_col.value] = cell_str

		# This whole block just constructs a unique id that we use as a dict key
		# for the course_sections dictionary
		catalog_num_str = row_data.get("Catalog Number", "")
		section_str = row_data.get("Section #", "")
		key = f"{catalog_num_str}-{section_str}"

		if len(key) > 1:
			#print(key)
			course_sections[key] = CourseSection(row_data)

	print(f"Built {len(course_sections)} CourseSection objects.")
	return course_sections


#....................................................................................
#####################################################################################
# 	Removes trailing ".0" if it exists in the attribute 
#....................................................................................
def make_int(attribute: str) -> str:
	if attribute.endswith(".0"):
		attribute = attribute[:-2]
		return attribute
	return attribute


#....................................................................................
#####################################################################################
# 	Reads the CSV to find all attribute strings
#....................................................................................
def get_headers(filename: str, defaults: Optional[Dict[int, str]] = None) -> List[str]:

	try:
		df = pd.read_csv(filename, skiprows=2, header=0)
		if not defaults:
			defaults = {}
		columns = list(df.columns)
		for i, col_name in enumerate(columns):
			if not col_name.strip():
				columns[i] = defaults.get(i, f"Column{i+1}")
		return columns
	except FileNotFoundError as e:
		raise FileNotFoundError(f"CSV file not found: {filename}") from e

#....................................................................................
#####################################################################################
# 	Reads the CSV to find any 'Peter Kiewit Institute ###' pattern in the text data.
#....................................................................................
def get_classroom(filename: str) -> None:

	try:
		df = pd.read_csv(filename, skiprows=2, header=0)
		text_data = df.to_string()
		pattern = r"Peter Kiewit Institute [0-9]{3}"
		rooms = re.findall(pattern, text_data)
		print(rooms)
	except KeyError as e:
		raise KeyError(f"Expected column missing in CSV: {str(e)}") from e

#....................................................................................
#####################################################################################
# 	Reads the CSV and extracts meeting patterns from the 'Meeting Pattern' column 
# using a regex.
#....................................................................................
def get_meeting_pattern(filename: str) -> None:

	try:
		df = pd.read_csv(filename, skiprows=2, header=0)
		regex_times = (
			r'(M|MW|TR|F|T|W|R|MWF|S|MR)\s'
			r'([0-9]{1,2}(:[0-9]{2})?[AaPp][Mm])\-([0-9]{1,2}(:[0-9]{2})?[AaPp][Mm])'
			r'(; (M|MW|TR|F|T|W|R|S)\s([0-9]{1,2}(:[0-9]{2})?[AaPp][Mm])\-([0-9]{1,2}(:[0-9]{2})?[AaPp][Mm]))?'
		)
		meeting_data = df['Meeting Pattern'].astype(str)
		matched = [mp for mp in meeting_data if re.search(regex_times, mp)]
		print(matched)
		print(len(matched))
	except KeyError as e:
		raise KeyError(f"Expected column missing in CSV: {str(e)}") from e

#....................................................................................
#####################################################################################
# 	Reads the CSV and finds any uppercase letters in 'Course' and 'Course Title'
# columns.
#....................................................................................
def get_course_code_and_title(filename: str) -> None:

	try:
		df = pd.read_csv(filename, skiprows=2, header=0)
		regex_caps = r'[A-Z]'

		courses = df['Course'].astype(str)
		courses_with_caps = [c for c in courses if re.search(regex_caps, c)]
		print(courses_with_caps)

		titles = df['Course Title'].astype(str)
		titles_with_caps = [t for t in titles if re.search(regex_caps, t)]
		print(titles_with_caps)
	except KeyError as e:
		raise KeyError(f"Expected column missing in CSV: {str(e)}") from e

#....................................................................................