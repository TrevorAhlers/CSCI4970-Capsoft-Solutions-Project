

from Model.CourseSection import CourseSection, CourseSectionColumn
import Utils.csv_parser as csvp
import csv
import os

def main():
    base_dir = os.path.dirname(__file__)
    csv_file = os.path.join(base_dir, '..', 'Files', 'Spring2023.csv')

    instantiation_dict = csvp.build_course_sections(csv_file)
    
    display_lines = view_1(instantiation_dict)

    for line in display_lines:
          print(line)

def view_1(input_dict):
    display = []
	# Create header row for the display
    header = f"{'Instructor':20} | {'Session':30} | {'Enrollment':20}"
    display.append(header)
    display.append("-" * len(header))
	# For each CourseSection object, format a display line using its attributes
    for key, course_section in input_dict.items():
        display_line = []
        if course_section.catalog_number:
             display_line = (
                f"{course_section.catalog_number:<20} | "
                f"{course_section.session:<30} | "
                f"{course_section.enrollment:<20}"
                )
        if display_line != []:
            display.append(display_line)
    return display

if __name__ == "__main__":
    main()