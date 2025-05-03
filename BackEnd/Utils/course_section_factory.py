# Populates CourseSection objs

import csv
import os
import pandas as pd
import re
from typing import Dict, List, Optional
from Model.CourseSection import CourseSection, CourseSectionEnum

#....................................................................................
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
def build_course_sections(filename: str) -> Dict[str, CourseSection]:
	"""
	Reads a CSV and returns a dict of CourseSection objs
	"""


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
					row_data[enum_col.value] = strip_decimal(cell_str)
				else:
					row_data[enum_col.value] = cell_str

		# This whole block just constructs a unique id that we use as a dict key
		# for the course_sections dictionary
		catalog_sub_str = row_data.get("Subject Code", "")
		catalog_num_str = row_data.get("Catalog Number", "")
		section_str     = row_data.get("Section #", "")
		term            = row_data.get("Term", "")
		term_code       = row_data.get("Term Code", "")
		dept_code       = row_data.get("Department Code", "")
		course          = row_data.get("Course", "")
		title           = row_data.get("Course Title", "")
		title_topic     = row_data.get("Title/Topic", "")
		meeting_pattern = row_data.get("Meeting Pattern", "")
		instructor      = row_data.get("Instructor", "")
		room            = row_data.get("Room", "")
		status          = row_data.get("Status", "")
		session         = row_data.get("Session", "")
		campus          = row_data.get("Campus", "")
		inst_method     = row_data.get("Inst. Method", "")
		integ_partner   = row_data.get("Integ. Partner", "")
		schedule_print  = row_data.get("Schedule Print", "")
		consent         = row_data.get("Consent", "")
		credit_min      = row_data.get("Credit Hrs Min", "")
		credit_hrs      = row_data.get("Credit Hrs", "")
		grade_mode      = row_data.get("Grade Mode", "")
		attributes      = row_data.get("Attributes", "")
		course_attrs    = row_data.get("Course Attributes", "")
		room_attrs      = row_data.get("Room Attributes", "")
		enrollment      = row_data.get("Enrollment", "")
		max_enroll      = row_data.get("Maximum Enrollment", "")
		prior_enroll    = row_data.get("Prior Enrollment", "")
		proj_enroll     = row_data.get("Projected Enrollment", "")
		wait_cap        = row_data.get("Wait Cap", "")
		rm_cap_req      = row_data.get("Rm Cap Request", "")
		cross_list      = row_data.get("Cross-listings", "")
		cross_max       = row_data.get("Cross-list Maximum", "")
		cross_proj      = row_data.get("Cross-list Projected", "")
		cross_wait_cap  = row_data.get("Cross-list Wait Cap", "")
		cross_rm_req    = row_data.get("Cross-list Rm Cap Request", "")
		link_to         = row_data.get("Link To", "")
		comments        = row_data.get("Comments", "")
		notes1          = row_data.get("Notes#1", "")
		notes2          = row_data.get("Notes#2", "")


		key = f"{catalog_sub_str} {catalog_num_str}-{section_str}"

		# EXCLUSION LOGIC — use raw values here, not CourseSection object
		if len(key) > 1:
			if session in {'UNO 5-6 Weeks', 'Three Week'}:
				continue
			if inst_method in {'Totally Online', 'Off Campus'}:
				continue
			if room in {'Fully Online', 'Totally Online'}:
				continue
			if any(sub in room for sub in {'CPACS', 'Off Campus', 'Mammel', 'Durham'}):
				continue
			if meeting_pattern == 'Does Not Meet':
				continue

			cs = CourseSection(row_data)
			course_sections[key] = cs

	finalize_all_crosslistings(course_sections)

	filtered_sections = {}

	for key1,section1 in course_sections.items():
		if len(section1.id) > 5:
			filtered_sections[key1] = section1

	print(f"course_section_factory.py: Built {len(filtered_sections)} CourseSection objects.")

	return filtered_sections

#....................................................................................
def strip_decimal(attribute: str) -> str:
	"""
	Removes a trailing '.0'
	"""

	if attribute.endswith(".0"):
		attribute = attribute[:-2]
		return attribute
	return attribute

#....................................................................................
def finalize_all_crosslistings(sections: Dict[str, CourseSection]) -> None:
	"""
	Expands and removes duplicates from all crosslistings
	"""

	for sec_id, section in sections.items():
		expanded = set()
		stack = list(section.crosslistings_cleaned)

		# remove dupes of aggregate crosslistings
		while stack:
			c_id = stack.pop()
			if c_id not in expanded:
				expanded.add(c_id)
				if c_id in sections:
					stack.extend(sections[c_id].crosslistings_cleaned)

		section.crosslistings_cleaned = sorted(expanded)
