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
import Utils.course_section_factory as csvp
# Other
from flask import Flask, jsonify, session, request, redirect, url_for, flash
import os

#....................................................................................

application = Flask(__name__)
application.secret_key = 'your_secret_key'


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
	base_dir = os.path.dirname(__file__)
	csv_file = os.path.join(base_dir, 'Files', 'Spring2023.csv')
	attributes = [
		CourseSectionEnum.CATALOG_NUMBER,
		CourseSectionEnum.SECTION,
		CourseSectionEnum.ROOM,
		CourseSectionEnum.ENROLLMENT,
		CourseSectionEnum.MAX_ENROLLMENT,
	]
	course_section_instantiation_dict = csvp.build_course_sections(csv_file)
	data_row_list = generate_strings_section_view(course_section_instantiation_dict, attributes)
	
	html_content = "<html><head><title>Course Info</title></head><body><pre>"
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
    csv_file = os.path.join(base_dir, 'Files', 'Spring2023.csv')
    instantiation_dict = csvp.build_course_sections(csv_file)
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

#....................................................................................

if __name__ == "__main__":
	application.run()

#....................................................................................
