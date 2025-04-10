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
from Model.AssignmentFile import AssignmentFile
from Utils.course_section_data_formatter import generate_strings_section_view
from Data.user_repo import *
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
import pickle # serialize
from typing import Dict, List
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from urllib.parse import unquote

#....................................................................................
# FILE NAMES:
#INPUT_CSV = 'Spring2023_unassigned.csv'
INPUT_CSV = 'Spring2023_test_261.csv'
ROOMS_CSV = 'PKIRooms.csv'
UNASSIGNED_CSV = 'Spring2023 conflict.csv'
OUTPUT_CSV = 'OutputCSV.csv'
TRAINING_CSVS = ["Fall2022.csv", "Fall2025.csv", "Spring2023.csv"]

#....................................................................................
# INIT
application = Flask(__name__)
application.secret_key = 'your_secret_key'
application.config['JWT_SECRET_KEY'] = 'super-secret'
jwt = JWTManager(application)
CORS(application)

UPLOAD_FOLDER = 'uploads'
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
application.config['ALLOWED_EXTENSIONS'] = {'csv'}

#....................................................................................

@application.route('/')
#@jwt_required()
def index():
	"""
	Prototype initialization of backend.
	String output of various debugging and logging.
	HTML output to return spreadsheet view of data in formatted strings.
	"""
	
	sections, classrooms, conflicts = build_all()

	assignment_file = AssignmentFile(sections, classrooms, conflicts)

	save_assignment_file(assignment_file)

	# for conflict in assignment_file.conflicts:
	# 	print(conflict.to_str())

	# for id,section in assignment_file.sections.items():
	# 	print(f'+++++++++++++++++++++++++++++')
	# 	print(f'section.id: {section.id}')
	# 	print(f'section.enrollment: {section.enrollment}')
	# 	print(f'section.max_enrollment: {section.max_enrollment}')

	attributes = []
	for attr in CourseSectionEnum:
		attributes.append(attr)

	export(assignment_file.sections)

	data_row_list = generate_strings_section_view(assignment_file.sections, attributes)

	html_content = "<html><head><title>Course Info</title></head><body><pre>"
	# Build a header row from the attribute names
	header_row = " | ".join([f"{attr.name:<30.30}" for attr in attributes])
	html_content += header_row + "\n"
	html_content += "-" * len(header_row) + "\n"

	for row in data_row_list:
		html_content += f"{row}\n"
	html_content += "</pre></body></html>"
	return html_content


# @application.route('/login', methods=['POST'])
# def login():
# 	"""
# 	Authenticates users and routes to the app home.
# 	Allows users to register.
# 	"""
# 	username = request.json.get('username')
# 	password = request.json.get('password')
# 	# Simple check, replace with your real user verification
# 	if username == "testuser" and password == "testpass":
# 		access_token = create_access_token(identity=username)
# 		return jsonify(access_token=access_token), 200
# 	return jsonify({"msg": "Invalid credentials"}), 401


@application.route('/details/<id>', methods=['GET'])
def details(id: str):
    """
    Returns CourseSection data to populate the details pane
    for a given selection
    """
	
    # Decode the ID to handle any URL encoding
	# The FrontEnd was sending spaces as "20%"
	# for example... so this fixes stuff like that
    decoded_id = unquote(id)
    
    assignment_file = load_assignment_file()

    if decoded_id not in assignment_file.sections:
        return jsonify({"error": "Course not found"}), 404

    section = assignment_file.sections[decoded_id]

    title = f'<p>Course: {section.course_title}</p>'

    content = ''
    content += f'<p>ID: {section.id}</p>'
    content += f'<p>Type: {section.section_type}</p>'
    content += f'<p>Meetings: {section.meeting_pattern}</p>'
    content += f'<p>Instructor: {section.instructor}</p>'
    content += f'<p>Room: {section.room}</p>'
    content += f'<p>Session: {section.session}</p>'
    content += f'<p>Campus: {section.campus}</p>'
    content += f'<p>Inst. Method: {section.inst_method}</p>'
    content += f'<p>Consent: {section.consent}</p>'
    content += f'<p>Credit Hrs Minimum: {section.credit_hours_min}</p>'
    content += f'<p>Credit Hrs: {section.credit_hours}</p>'
    content += f'<p>Grade Mode: {section.grade_mode}</p>'
    content += f'<p>Attributes: {section.attributes}</p>'
    content += f'<p>Course Attributes: {section.course_attributes}</p>'
    content += f'<p>Enrollment: {section.enrollment}</p>'
    content += f'<p>Max Enrollment: {section.max_enrollment}</p>'
    content += f'<p>Wait Capacity: {section.wait_cap}</p>'
    content += f'<p>Room Capacity Req.: {section.rm_cap_request}</p>'
    content += f'<p>Crosslistings: {section.cross_listings}</p>'
    content += f'<p>Crosslist Maximum: {section.cross_list_max}</p>'
    content += f'<p>Crosslist Waitlist Capacity: {section.cross_list_wait_cap}</p>'
    content += f'<p>Link to: {section.link_to}</p>'
    content += f'<p>Comments: {section.comments}</p>'
    content += f'<p>Notes 1: {section.notes1}</p>'
    content += f'<p>Notes 2: {section.notes2}</p>'
    content += f'<p>Schedule: {section.schedule}</p>'
    content += f'<p>Warning: {section.warning}</p>'

    print(f'application.py: /details/{decoded_id}')
    return jsonify({"content": title + content})




@application.route('/conflicts/all', methods=['GET'])
def conflicts_all():
	"""
	Returns [Conflict] array to populate the conflict pane
	for an AssignmentFile.

	This is returned in a List so we can iterate over each
	Conflict object to populate each conflict box component
	on the FrontEnd.
	"""
	assignment_file = load_assignment_file()
	content_list = []

	for conflict in assignment_file.conflicts:
		if conflict.ignored:
			continue

		title = '<h2>Conflict:</h2>'

		if not conflict.conflict_message:
			conflict_sections = ""
			for section in conflict.sections:
				conflict_sections += f'<p>{section.id or ""}: </p><br>'
				conflict_sections += f'<p>{section.meeting_pattern or ""} </p><br>'
			full_conflict = title + conflict_sections
		else:
			msg = conflict.conflict_message or ''
			full_conflict = title + f'<p>{msg}</p><br>'

		content_list.append(full_conflict or '')

	print(f'application.py: /conflict/all')
	return jsonify(content_list)


@application.route('/conflict/ignore/<id>', methods=['GET'])
def conflict_ignore(id: str):
	"""
	Updates a Conflict object to have it's attribute "ignored"
	set to True.
	"""
	assignment_file = load_assignment_file()
	for conflict in assignment_file.conflicts:
		if conflict.id == id:
			conflict.ignored = True
	save_assignment_file(assignment_file)
	print(f'application.py: /conflict/ignore/{id}')

@application.route('/conflict/unignore/<id>', methods=['GET'])
def conflict_unignore(id: str):
	"""
	Updates a Conflict object to have it's attribute "ignored"
	set to False.
	"""
	assignment_file = load_assignment_file()
	for conflict in assignment_file.conflicts:
		if conflict.id == id:
			conflict.ignored = False
	save_assignment_file(assignment_file)
	print(f'application.py: /conflict/ignore/{id}')

@application.route('/get-username')
#@jwt_required()
def get_username():
	pass
	# user = get_user_from_db(host: str, user: str, password: str, database: str, user_id: str)


@application.route('/api/course-info')
#@jwt_required()
def course_info():
	"""
	GET CourseSection Objects for the Input Spreadsheet
	"""
	base_dir = os.path.dirname(__file__)
	section_csv_file = os.path.join(base_dir, 'Files', 'Spring2023.csv')
	instantiation_dict = csf.build_course_sections(section_csv_file)
	info_list = generate_strings_section_view(instantiation_dict)
	print('application.py: /course-info')
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

		sections, classrooms, conflicts = build_all()
		assignment_file = AssignmentFile(sections, classrooms, conflicts)
		save_assignment_file(assignment_file)

		return jsonify({"message": "File uploaded and memory updated", "filename": file.filename})
	
	print('application.py: /upload')

	return jsonify({"message": "Invalid file format. Only CSV files are allowed."}), 400


@application.route('/api/data', methods=['GET'])
def get_data():
	assignment_file = load_assignment_file()

	assigner.default_assignment(assignment_file.classrooms, assignment_file.sections)
	conflicts = build_conflicts(assignment_file.sections, assignment_file.classrooms)
	export(assignment_file.sections)

	attributes = [
		CourseSectionEnum.SECTION,
		CourseSectionEnum.ROOM,
		CourseSectionEnum.ENROLLMENT,
		CourseSectionEnum.MAX_ENROLLMENT,
		CourseSectionEnum.MEETING_PATTERN,
	]

	data_row_list = generate_strings_section_view(assignment_file.sections, attributes)

	data = []
	section_keys = list(assignment_file.sections.keys())

	for i, row in enumerate(data_row_list):
		values = row.split(" | ")
		section = assignment_file.sections[section_keys[i]]

		entry = {}
		entry["id"] = section.id  # first column
		for j, attr in enumerate(attributes):
			entry[attr.name] = values[j]

		data.append(entry)
	
	print('application.py: /api/data')

	return jsonify({"courses": data})



#....................................................................................
# Helper functions:
#....................................................................................
def build_all():
	sections: 	Dict[str,CourseSection] = build_sections()
	classrooms: Dict[str,Classroom] 	= build_classrooms(sections)
	build_freq_map(sections)
	build_department_freq_map(sections, classrooms)
	assigner.default_assignment(classrooms, sections)
	conflicts = build_conflicts(sections, classrooms)
	return sections, classrooms, conflicts

def build_freq_map(sections: Dict[str,CourseSection]):
	freq_map = room_scorer.map_assignment_freq(TRAINING_CSVS)
	for id, freq_section in freq_map.items():
		if id in sections:
			sections[id].room_freq = freq_section


def build_department_freq_map(sections: Dict[str,CourseSection], classrooms: Dict[str,Classroom]):
	freq_map = room_scorer.map_department_freq(TRAINING_CSVS)
	if freq_map:
		for id, freq_section in freq_map.items():
			if id in classrooms:
				classrooms[id].department_counts = freq_section

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

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in application.config['ALLOWED_EXTENSIONS']


def get_data():
	sections: 	Dict[str,CourseSection] = build_sections()
	classrooms: Dict[str,Classroom] 	= build_classrooms(sections)
	sections = build_freq_map(sections)
	classrooms, sections = assigner.default_assignment(classrooms, sections)
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
		values = row.split(" | ")  # Assuming data is formatted similarly
		entry = {attr.name: values[i] for i, attr in enumerate(attributes)}
		data.append(entry)

	return jsonify({"courses": data})

def save_assignment_file(assignment_file: AssignmentFile):
	with open('assignment_file.pkl', 'wb') as f:
		pickle.dump(assignment_file, f)

def load_assignment_file():
	with open('assignment_file.pkl', 'rb') as f:
		return pickle.load(f)
	
def make_assignment_file(sections: Dict[str,CourseSection], classrooms: Dict[str,Classroom], conflicts: List[Conflict]):
	assignment_file = AssignmentFile(sections, classrooms, conflicts)
	return assignment_file

#....................................................................................
if __name__ == '__main__':
	application.run(debug=True)
#....................................................................................
