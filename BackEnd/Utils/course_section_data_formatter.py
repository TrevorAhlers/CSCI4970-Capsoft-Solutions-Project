#####################################################################################
#   CourseSection Data Formatter
#____________________________________________________________________________________
#
#  CourseSection Objects + Needed Attributes -> List of Strings to Represent Data
#....................................................................................

from Model.CourseSection import CourseSection, CourseSectionEnum
from Utils import course_section_factory as csf

import csv
import os
import sys

def main():
      print("course_section_data_formatter: Ran as main() ... No output.")

#####################################################################################
# Takes dictionary of CourseSection objects and outputs formatted strings or "data
# rows".
#....................................................................................
def generate_strings_section_view(course_section_objects: dict, attributes: list) -> list[str]:

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
#####################################################################################
# Takes dictionary of CourseSection objects and outputs formatted strings or "data
# rows".
#....................................................................................
def row_to_string(course_section, attributes):

    display_values = []
    for attr in attributes:
        value = getattr(course_section, attr.name.lower(), "")
        display_values.append(f"{value:<30.30}")
    return " | ".join(display_values)

#....................................................................................

if __name__ == "__main__":
      main()