#..................................................................
# Main Application
#
# Routes requests and manages program state.
# Each @application.route('') is executed when the address
# is visited.
#
# We employ our state
# We employ our data model to 
#..................................................................

from Model.CourseSection import CourseSection, CourseSectionColumn
from flask import Flask, jsonify, session, request, redirect, url_for, flash
from Utils.state_manager import backup_session_data, restore_session_data
from Controller.section_data_formatter import view_1 as v1
import Utils.csv_parser as csvp
import os

application = Flask(__name__)
application.secret_key = 'your_secret_key'

###################################################################
# User Landing Page
#..................................................................
#
# -Currently prototyping datamodel object instantiation.
# -In production, these route functions will be on standby for
#  angular to fetch data in JSON format
#
###################################################################
@application.route('/')
def index():
	base_dir = os.path.dirname(__file__)
	csv_file = os.path.join(base_dir, 'Files', 'Spring2023.csv')
	instantiation_dict = csvp.build_course_sections(csv_file)
	info_list = v1(instantiation_dict)
	
	# Build HTML content by wrapping each row in <p> tags
	html_content = "<html><head><title>Course Info</title></head><body>"
	for row in info_list:
		html_content += f"<p>{row}</p>"
	html_content += "</body></html>"
	return html_content

###################################################################
# GET CourseSection Objects for the Input Spreadsheet
#..................................................................
#
###################################################################
@application.route('/api/course-info')
def course_info():
    base_dir = os.path.dirname(__file__)
    csv_file = os.path.join(base_dir, 'Files', 'Spring2023.csv')
    instantiation_dict = csvp.build_course_sections(csv_file)
    info_list = v1(instantiation_dict)
    return jsonify(info_list)

###################################################################
# Modify Session Data
#..................................................................
#
###################################################################
@application.route('/modify', methods=['POST'])
def modify():
	backup_session_data()  # Backup current state before modifying
	state = session.get('state', {})
	state['data'] = request.form.get('data')
	session['state'] = state
	return redirect(url_for('index'))

###################################################################
# Abort Session
#..................................................................
#
###################################################################
@application.route('/abort')
def abort():
	if restore_session_data():
		flash("Changes aborted and state restored.")
	else:
		flash("No previous state found.")
	return redirect(url_for('index'))

if __name__ == "__main__":
	application.run()
