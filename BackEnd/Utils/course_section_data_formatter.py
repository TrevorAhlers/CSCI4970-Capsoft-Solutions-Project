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
      """
    Main function that runs the script. Currently, it just prints a message indicating
    that the script ran. It does not produce any output.
    """
      print("course_section_data_formatter: Ran as main() ... No output.")

#####################################################################################
# Takes dictionary of CourseSection objects and outputs formatted strings or "data
# rows".
#....................................................................................
def generate_strings_section_view(course_section_objects: dict, attributes: list) -> list[str]:
    """
    Generates a list of formatted strings (rows) to represent the attributes of CourseSection objects.

    This function iterates over a dictionary of CourseSection objects and formats their specified attributes
    into a list of strings, which can be used for reporting or data export.

    Args:
        course_section_objects (dict): A dictionary where the keys are section IDs and the values are CourseSection objects.
        attributes (list): A list of attributes (as strings) that should be included in the output. These attributes will be 
        used to extract data from each CourseSection object.

    Returns:
        list[str]: A list of strings, each representing a row of formatted data for a CourseSection object.
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
#####################################################################################
# Takes dictionary of CourseSection objects and outputs formatted strings or "data
# rows".
#....................................................................................
def row_to_string(course_section, attributes):
    """
    Converts a CourseSection object into a formatted string based on its attributes.

    This function extracts the specified attributes from the CourseSection object and formats them into a
    single string, with each attribute separated by a pipe character ("|").

    Args:
        course_section (CourseSection): The CourseSection object whose attributes will be extracted and formatted.
        attributes (list): A list of attributes (as strings) that should be included in the formatted output.

    Returns:
        str: A string that represents the CourseSection's specified attributes, formatted with each attribute
             separated by a pipe character ("|").
    """

    display_values = []
    for attr in attributes:
        value = getattr(course_section, attr.name.lower(), "")
        display_values.append(f"{value:<30.30}")
    return " | ".join(display_values)

#....................................................................................

if __name__ == "__main__":
      main()