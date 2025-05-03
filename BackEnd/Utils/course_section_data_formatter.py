# Retrieves data from CourseSection objs and outputs a formatted string to be a data row

from Model.CourseSection import CourseSection, CourseSectionEnum
from Utils import course_section_factory as csf


#....................................................................................
def generate_strings_section_view(course_section_objects: dict[str, CourseSection], attributes: list) -> list[str]:
	"""
	Takes a dict of CourseSection objects and a list of attributes, returns a list of formatted strings
	"""

	# This list is our Function output.
	# List of formatted strings (rows) of text to represent object attributes.
	display = []

	# For each CourseSection object, format a display line using its attributes
	for key, course_section in course_section_objects.items():

		display_line = []

		# If line is blank, skip this for loop iteration
		# We check course_section because it should be reliably
		# present if a class section is on the line to extract.
		if not course_section.catalog_number:
				continue
		
		display_line = row_to_string(course_section, attributes)

		if display_line != []:
			display.append(display_line)
	return display

#....................................................................................
def row_to_string(course_section: CourseSection, attributes):
	"""
	Takes one CourseSection and a list of attributes, returns a single formatted string row.
	"""

	display_values = []
	for attr in attributes:
		value = getattr(course_section, attr.name.lower(), "")
		display_values.append(f"{str(value):<30.30}")
	return " | ".join(display_values)