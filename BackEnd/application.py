#####################################################################################
#	application.py - Flask Route File
#____________________________________________________________________________________
# 
# Line 43 is where you can start
#
# Routes requests and manages program state.
# Each @application.route('') is executed when the address
# is visited.
#
#....................................................................................

# Local
from Model.CourseSection import CourseSection, CourseSectionEnum
from Model.Classroom import Classroom, ClassroomEnum
from Model.Conflict import Conflict
#from Utils.assignment_file_manager import backup_session_data, restore_session_data
from Controller.course_section_data_formatter import generate_strings_section_view
import Utils.course_section_factory as csf
import Utils.classroom_factory as cf
import Utils.conflict_factory as cof
import Controller.assigner as assigner
import Utils.room_scorer as room_scorer
# Other
from flask import Flask, jsonify, session, request, redirect, url_for, flash
import os
from flask_cors import CORS


#....................................................................................

# FILE NAMES: (note it's currently using a test CSV to show a conflict)
INPUT_CSV = 'Fall2025.csv'
ROOMS_CSV = 'PKIRooms.csv'
TRAINING_CSVS = ["Fall2022.csv", "Fall2025.csv", "Spring2023.csv"]

#....................................................................................

application = Flask(__name__)
application.secret_key = 'your_secret_key'
CORS(application)


#....................................................................................
#####################################################################################
# 	User Landing Page
#____________________________________________________________________________________
#
# -Currently prototyping datamodel object instantiation.
# -In production, these route functions will be on standby for
#  angular to fetch data in JSON format
#
#....................................................................................
@application.route('/')
def index():

	sections = build_sections()
	classrooms = build_classrooms()

	# Frequency map populates section object attribute: room_freq
	# this attribute contains a dictionary of all the rooms this
	# section has been assigned to, and how many times.
	#
	# The idea is to reinforce valid room assignments with as much
	# input data as possible, and can even continue to do so if the
	# users add finalized assignment csvs to the training data.
	sections = build_freq_map(sections)

	
	# # Print all sections and their room(s).
	for _,section in sections.items():
		print(f'-------------------------------')
		print(f'Section: {section.id}')
		#for room in section.room_numbers:
		#print(section.room_numbers)
		print(section.parsed_meetings)
		print(section.room_freq)
		
	# for _,class1 in classrooms.items():
	# 	print(f'===============================')
	# 	print("Class",class1.room)
	# 	print("Seats",class1.seats)


	assigner.assign_sections_to_rooms(classrooms, sections)

	conflicts = build_conflicts(sections, classrooms)

	attributes = []

	for attr in CourseSectionEnum:
		attributes.append(attr)
	
	#for conflict in conflicts:
		#print(conflict.to_str())
	

	data_row_list = generate_strings_section_view(sections, attributes)

	html_content = "<html><head><title>Course Info</title></head><body><pre>"
	# Build a header row from the attribute names
	header_row = " | ".join([f"{attr.name:<30.30}" for attr in attributes])
	html_content += header_row + "\n"
	html_content += "-" * len(header_row) + "\n"

	for row in data_row_list:
		html_content += f"{row}\n"
	html_content += "</pre></body></html>"
	return html_content


#....................................................................................
#####################################################################################
# 	GET CourseSection Objects for the Input Spreadsheet
#____________________________________________________________________________________
# Description placeholder text
#....................................................................................
@application.route('/api/course-info')
def course_info():
    base_dir = os.path.dirname(__file__)
    section_csv_file = os.path.join(base_dir, 'Files', 'Spring2023.csv')
    instantiation_dict = csf.build_course_sections(section_csv_file)
    info_list = generate_strings_section_view(instantiation_dict)
    return jsonify(info_list)


@application.route('/api/data', methods=['GET'])
def get_data():
    base_dir = os.path.dirname(__file__)
    csv_file = os.path.join(base_dir, 'Files', INPUT_CSV)
    
    attributes = [
        CourseSectionEnum.CATALOG_NUMBER,
        CourseSectionEnum.SECTION,
        CourseSectionEnum.ROOM,
        CourseSectionEnum.ENROLLMENT,
        CourseSectionEnum.MAX_ENROLLMENT,
    ]
    
    course_section_instantiation_dict = csf.build_course_sections(csv_file)
    data_row_list = generate_strings_section_view(course_section_instantiation_dict, attributes)

    data = []
    for row in data_row_list:
        values = row.split(" | ")  # Assuming data is formatted similarly
        entry = {attr.name: values[i] for i, attr in enumerate(attributes)}
        data.append(entry)

    return jsonify({"courses": data})

#....................................................................................
# Helper functions:

def build_freq_map(sections):
	freq_map = room_scorer.map_assignment_freq(TRAINING_CSVS)
	for id,freq_section in freq_map.items():
		if id in sections:
			sections[id].room_freq = freq_section
	return sections

def build_classrooms():
	base_dir = os.path.dirname(__file__)
	classroom_csv_file = os.path.join(base_dir, 'Files', ROOMS_CSV)
	classroom_instantiation_dict = cf.build_classrooms(classroom_csv_file)
	return classroom_instantiation_dict

def build_sections():
	base_dir = os.path.dirname(__file__)
	section_csv_file = os.path.join(base_dir, 'Files', INPUT_CSV)
	course_section_instantiation_dict = csf.build_course_sections(section_csv_file)
	return course_section_instantiation_dict

def build_conflicts(sections, classrooms):
	conflict_instantiation_list = cof.build_conflicts(sections, classrooms)
	return conflict_instantiation_list


#....................................................................................

if __name__ == '__main__':
    application.run(debug=True)

#....................................................................................
