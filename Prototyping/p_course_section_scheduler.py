#####################################################################################
#   CourseSection Scheduling Logic Prototype
#____________________________________________________________________________________
#
#....................................................................................

from p_CourseSection import CourseSection, CourseSectionEnum
from p_course_section_factory import build_course_sections
from p_course_section_data_formatter import generate_strings_section_view

import os, sys

#....................................................................................
#####################################################################################
# 	Main Prototyping Logic
#....................................................................................
def main():
    # Set up out dictionary of course section objects
    course_section_obj_dict = prepare_section_obj_dict()

    # Pull some information from these objects using methods from our
    # p_CourseSection.py data model
    print("Class name:",course_section_obj_dict["1030-1"].course_title)
    print("Classroom",course_section_obj_dict["1030-1"].room)
    print("Number of enrolled students:",course_section_obj_dict["1030-1"].enrollment)
    print("Maximum capacity of enrolled students:",course_section_obj_dict["1030-1"].max_enrollment)

    # Note to Haresh: This data is raw, and it might be a good idea to create methods
    # in the p_CourseSection.py datamodel that return cleaned values instead so we can
    # call course_section_obj_dict["1030-1"].course_title_clean for example.


#....................................................................................
#####################################################################################
# 	Reads the CSV and creates a dictionary of CourseSection 
# objects. Each entry is keyed by "Catalog Number-Section #", for example "1030-1".
#....................................................................................
def prepare_section_obj_dict():
    base_dir = os.path.dirname(__file__)
    csv_file = os.path.join(base_dir, 'p_Spring2023.csv')
    course_section_instantiation_dict = build_course_sections(csv_file)

    return course_section_instantiation_dict

if __name__ == "__main__":
    main()