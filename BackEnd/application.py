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
from Utils.state_manager import backup_session_data, restore_session_data
from Controller.course_section_data_formatter import generate_strings_section_view
import Utils.course_section_factory as csf
import Utils.classroom_factory as cf
import Controller.assigner as assigner
# Other
from flask import Flask, jsonify, session, request, redirect, url_for, flash
import os
from flask_cors import CORS


#....................................................................................

# FILE NAMES: (note it's currently using a test CSV to show a conflict)
INPUT_CSV = 'Spring2023 conflict.csv'
ROOMS_CSV = 'PKIRooms.csv'

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

	assigner.assign_sections_to_rooms(classrooms, sections)

	attributes = []

	for attr in CourseSectionEnum:
		attributes.append(attr)

	
	data_row_list = generate_strings_section_view(sections, attributes)


	# testing conflicts
	section1 = sections["3030-1"]
	section3 = sections["3030-3"]

	print(section1.room, "--", section1.meetings)
	print(section3.room, "--", section3.meetings)

	print(classrooms["117"].find_conflicts())

	
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

#....................................................................................
#####################################################################################
# 	Modify Session Data
#____________________________________________________________________________________
# Description placeholder text
#....................................................................................
@application.route('/modify', methods=['POST'])
def modify():
	backup_session_data()  # Backup current state before modifying
	state = session.get('state', {})
	state['data'] = request.form.get('data')
	session['state'] = state
	return redirect(url_for('index'))

#....................................................................................
#####################################################################################
# 	Abort Session
#____________________________________________________________________________________
# Description placeholder text
#....................................................................................
@application.route('/abort')
def abort():
	if restore_session_data():
		flash("Changes aborted and state restored.")
	else:
		flash("No previous state found.")
	return redirect(url_for('index'))




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


#....................................................................................

if __name__ == '__main__':
    application.run(debug=True)

#....................................................................................
