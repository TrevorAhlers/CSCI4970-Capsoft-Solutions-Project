#####################################################################################
#	application.py - Flask Route File
#____________________________________________________________________________________
#
# Routes requests and manages program state.
# Each @application.route('') is executed when the address is visited.
#
#....................................................................................

# Local
from Model.CourseSection import CourseSection, CourseSectionEnum
from Model.Classroom import Classroom, ClassroomEnum
from Model.Conflict import Conflict
#from Utils.assignment_file_manager import backup_session_data, restore_session_data
from Utils.course_section_data_formatter import generate_strings_section_view
import Utils.course_section_factory as csf
import Utils.classroom_factory as cf
import Utils.conflict_factory as cof
import Controller.assigner as assigner
import Controller.room_scorer as room_scorer
import Controller.exporter as exporter
# Other
from flask import Flask, jsonify, session, request, redirect, url_for, flash
import os
from flask_cors import CORS
import pickle
from typing import Dict
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

#....................................................................................
# FILE NAMES: (note it's currently using a test CSV to show a conflict)
INPUT_CSV = 'Spring2023_unassigned.csv'
#INPUT_CSV = 'Spring2023_test_261.csv'
ROOMS_CSV = 'PKIRooms.csv'
UNASSIGNED_CSV = 'Spring2023 conflict.csv'
OUTPUT_CSV = 'OutputCSV.csv'
TRAINING_CSVS = ["Fall2022.csv", "Fall2025.csv", "Spring2023.csv"]

#....................................................................................
application = Flask(__name__)
application.secret_key = 'your_secret_key'
application.config['JWT_SECRET_KEY'] = 'super-secret'
jwt = JWTManager(application)
CORS(application)

UPLOAD_FOLDER = 'uploads'
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
application.config['ALLOWED_EXTENSIONS'] = {'csv'}

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in application.config['ALLOWED_EXTENSIONS']

def get_data():
	sections: 	Dict[str, CourseSection] = build_sections()
	classrooms: Dict[str, Classroom] = build_classrooms(sections)
	sections = build_freq_map(sections)

	# Removed the return capture since dictionaries are mutated in place
	assigner.default_assignment(classrooms, sections)

	conflicts = build_conflicts(sections, classrooms)
	export(sections)

	base_dir = os.path.dirname(__file__)
	csv_file = os.path.join(base_dir, 'Files', OUTPUT_CSV)

	attributes = [
		CourseSectionEnum.CATALOG_NUMBER,
		CourseSectionEnum.SECTION,
		CourseSectionEnum.ROOM,
		CourseSectionEnum.ENROLLMENT,
		CourseSectionEnum.MAX_ENROLLMENT,
	]

	data_row_list = generate_strings_section_view(sections, attributes)
	data = []
	for row in data_row_list:
		values = row.split(" | ")
		entry = {attr.name: values[i] for i, attr in enumerate(attributes)}
		data.append(entry)

	return jsonify({"courses": data})


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
#@jwt_required()
def index():
	sections: 	Dict[str,CourseSection] = build_sections()
	classrooms: Dict[str,Classroom] 	= build_classrooms(sections)

	# Frequency map populates section object attribute: room_freq
	sections = build_freq_map(sections)
	build_department_freq_map(sections, classrooms)

	# Removed the return capture for the same reason
	assigner.default_assignment(classrooms, sections)

	conflicts = build_conflicts(sections, classrooms)
	for conflict in conflicts:
		print(conflict.to_str())

	attributes = []
	for attr in CourseSectionEnum:
		attributes.append(attr)

	export(sections)

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
# 	Login page
#____________________________________________________________________________________
# 	jwt_extended authentication
#....................................................................................
@application.route('/login', methods=['POST'])
def login():
	username = request.json.get('username')
	password = request.json.get('password')
	# Simple check, replace with your real user verification
	if username == "testuser" and password == "testpass":
		access_token = create_access_token(identity=username)
		return jsonify(access_token=access_token), 200
	return jsonify({"msg": "Invalid credentials"}), 401


#....................................................................................
#####################################################################################
# 	GET CourseSection Objects for the Input Spreadsheet
#____________________________________________________________________________________
# Description placeholder text
#....................................................................................
@application.route('/api/course-info')
#@jwt_required()
def course_info():
	base_dir = os.path.dirname(__file__)
	section_csv_file = os.path.join(base_dir, 'Files', 'Spring2023.csv')
	instantiation_dict = csf.build_course_sections(section_csv_file)
	info_list = generate_strings_section_view(instantiation_dict)
	return jsonify(info_list)

@application.route('/upload', methods=['POST'])
#@jwt_required()
def upload():
	if not os.path.exists(application.config['UPLOAD_FOLDER']):
		os.makedirs(application.config['UPLOAD_FOLDER'])

	if 'file' not in request.files:
		return jsonify({"message": "No file part"}), 400

	file = request.files['file']
	if file.filename == '':
		return jsonify({"message": "No selected file"}), 400

	if file and allowed_file(file.filename):
		filename = os.path.join(application.config['UPLOAD_FOLDER'], file.filename)
		file.save(filename)
		global INPUT_CSV
		INPUT_CSV = file.filename
		print(INPUT_CSV)
		print(file.filename)
		return jsonify({"message": "File uploaded successfully", "filename": file.filename})

	return jsonify({"message": "Invalid file format. Only CSV files are allowed."}), 400


@application.route('/api/data', methods=['GET'])
#@jwt_required()
def get_data_endpoint():
	sections: 	Dict[str,CourseSection] = build_sections()
	classrooms: Dict[str,Classroom] 	= build_classrooms(sections)
	sections = build_freq_map(sections)

	# Same pass-by-reference fix here
	assigner.default_assignment(classrooms, sections)

	conflicts = build_conflicts(sections, classrooms)
	export(sections)

	base_dir = os.path.dirname(__file__)
	csv_file = os.path.join(base_dir, 'Files', OUTPUT_CSV)

	attributes = [
		CourseSectionEnum.CATALOG_NUMBER,
		CourseSectionEnum.SECTION,
		CourseSectionEnum.ROOM,
		CourseSectionEnum.ENROLLMENT,
		CourseSectionEnum.MAX_ENROLLMENT,
	]

	data_row_list = generate_strings_section_view(sections, attributes)
	data = []
	for row in data_row_list:
		values = row.split(" | ")
		entry = {attr.name: values[i] for i, attr in enumerate(attributes)}
		data.append(entry)

	return jsonify({"courses": data})

#....................................................................................
# Helper functions:
#....................................................................................
def build_freq_map(sections):
	freq_map = room_scorer.map_assignment_freq(TRAINING_CSVS)
	for id, freq_section in freq_map.items():
		if id in sections:
			sections[id].room_freq = freq_section
	return sections

def build_department_freq_map(sections, classrooms):
	freq_map = room_scorer.map_department_freq(TRAINING_CSVS)
	for id, freq_section in freq_map.items():
		if id in sections:
			sections[id].room_freq = freq_section
	return sections

def build_classrooms(sections):
	base_dir = os.path.dirname(__file__)
	classroom_csv_file = os.path.join(base_dir, 'Files', ROOMS_CSV)
	classroom_instantiation_dict = cf.build_classrooms(classroom_csv_file, sections)
	return classroom_instantiation_dict

def build_sections():
	base_dir = os.path.dirname(__file__)
	section_csv_file = os.path.join(base_dir, 'Files', INPUT_CSV)
	course_section_instantiation_dict = csf.build_course_sections(section_csv_file)
	return course_section_instantiation_dict

def build_conflicts(sections, classrooms):
	conflict_instantiation_list = cof.build_conflicts(sections, classrooms)
	return conflict_instantiation_list

def export(sections):
	base_dir = os.path.dirname(__file__)
	input_csv_file = os.path.join(base_dir, 'Files', INPUT_CSV)
	output_csv_file = os.path.join(base_dir, 'Files', 'Exports', OUTPUT_CSV)
	conflict_instantiation_list = exporter.update_csv_with_room(input_csv_file, output_csv_file, sections)
	return conflict_instantiation_list

#....................................................................................
if __name__ == '__main__':
	application.run(debug=True)
#....................................................................................
