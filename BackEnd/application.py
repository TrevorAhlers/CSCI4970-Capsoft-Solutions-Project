#####################################################################################
#	application.py - Flask Route File
#____________________________________________________________________________________
#
# Routes requests and manages program state.
# Each @application.route('') is executed when the address is visited.
#
#....................................................................................

# Local
from Model.CourseSection import CourseSection, CourseSectionEnum, combine_section_info, parse_meetings, parse_rooms, extract_room_numbers
from Model.Classroom import Classroom, ClassroomEnum
from Model.Conflict import Conflict
from Model.AssignmentFile import AssignmentFile
from Utils.course_section_data_formatter import generate_strings_section_view
import Utils.course_section_factory as csf
import Utils.classroom_factory as cf
import Utils.conflict_factory as cof
import Controller.assigner as assigner
import Controller.room_scorer as room_scorer
import Controller.exporter as exporter
# Other
from flask import Flask, jsonify, session, request, redirect, url_for, flash, send_file
import os
from flask_cors import CORS, cross_origin
import pickle # serialize
from typing import Dict, List
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from urllib.parse import unquote

from Model.User import User
from Model.WorkspaceState import WorkspaceState

from Data.user_repo import *
import Data.assignment_file_repo as af_db

from Data import user_repo
user_repo.init_db()


import json

DB_CONFIG = {
	'host': 'app-db-1.c6zkyqugocxt.us-east-1.rds.amazonaws.com',
	'user': 'capsoftdb',
	'password': 'csci4970',
	'database': 'maindb'
}

try:
	af_db.init_db()
except Exception as e:
	print(f"[INIT ERROR] {e}")

#....................................................................................
# FILE NAMES:
INPUT_CSV = 'Fall2025.csv'
#INPUT_CSV = 'Spring2023_test_261.csv'
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
CORS(
	application,
	resources={r"/*": {"origins": "*"}},
	allow_headers=["Content-Type", "Authorization"],
	supports_credentials=True
)

UPLOAD_FOLDER = 'uploads'
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
application.config['ALLOWED_EXTENSIONS'] = {'csv'}

#....................................................................................

@application.route('/')
def index():
	return 'OK', 200

@application.route('/api/register', methods=['POST'])
def register():
	data     = request.get_json(force=True) or {}
	username = data.get('username')  or data.get('user_id')
	email    = data.get('email')     or data.get('user_email')
	password = data.get('password')  or data.get('user_password')

	if not all([username, email, password]):
		return jsonify({'msg': 'Missing fields'}), 400

	key  = f"{username}:{email}"
	user = User(key, password, None)

	try:
		user_repo.upsert(user)
		application.logger.info("User %s registered", key)
		return jsonify({'msg': 'User created'}), 201
	except Exception as exc:
		application.logger.exception(exc)
		return jsonify({'msg': 'DB error'}), 500



@application.route('/api/login', methods=['POST'])
def login():
	data     = request.get_json(force=True) or {}
	username = data.get('username') or data.get('user_id')
	password = data.get('password') or data.get('user_password')

	if not all([username, password]):
		return jsonify(msg='Missing fields'), 400

	row = user_repo.get_by_username(username)
	if row is None or row.get('user_password') != password:
		return jsonify(msg='Bad credentials'), 401

	access = create_access_token(identity=row['user_id'])
	return jsonify(token=access), 200



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

@application.route('/edit/save/<id>', methods=['POST'])
def save_course_section_edits(id: str):
	print(f'[ROUTE HIT] /edit/save/<id>')
	decoded_id = unquote(id)
	assignment_file = load_assignment_file()

	if decoded_id not in assignment_file.sections:
		return jsonify({"error": "Course not found"}), 404

	data = request.get_json()
	base_section = assignment_file.sections[decoded_id]
	linked_ids = [decoded_id] + base_section.crosslistings_cleaned

	new_room = data.get("room", base_section.room)
	new_meeting = data.get("meeting1", base_section.meeting_pattern)
	new_instructor = data.get("instructor", base_section.instructor)

	for sec_id in linked_ids:
		if sec_id not in assignment_file.sections:
			continue
		sec = assignment_file.sections[sec_id]
		sec.room = new_room
		sec.meeting_pattern = new_meeting
		sec.instructor = new_instructor

	# update these fields
	base_section.cross_listings = data.get("crossListings", base_section.cross_listings)
	base_section.max_enrollment = data.get("maxEnrollment", base_section.max_enrollment)
	base_section.enrollment = data.get("enrollment", base_section.enrollment)
	base_section.comments = data.get("comments", base_section.comments)
	base_section.notes1 = data.get("notes1", base_section.notes1)
	base_section.notes2 = data.get("notes2", base_section.notes2)

	# Recompute schedules
	for sec in assignment_file.sections.values():
		sec.parsed_meetings = parse_meetings(sec.meeting_pattern)
		sec.rooms = parse_rooms(sec.room)
		sec.room_numbers = extract_room_numbers(sec.rooms)
		sec.schedule, sec.warning = combine_section_info(sec.id, sec.parsed_meetings, sec.rooms)

	for classroom in assignment_file.classrooms.values():
		classroom.schedule = [[] for _ in range(7 * 1440)]

	for sec in assignment_file.sections.values():
		for (_, room_name, _, _, _) in sec.schedule:
			if room_name in assignment_file.classrooms:
				assignment_file.classrooms[room_name].add_course_section_object(sec)

	new_conflicts = build_conflicts(assignment_file.sections, assignment_file.classrooms)
	assignment_file.conflicts = preserve_ignored_conflicts(assignment_file.conflicts, new_conflicts)
	rebuild_conflict_lists(assignment_file)
	save_assignment_file(assignment_file)

	print(f'/edit/save/{decoded_id} — updated')
	return jsonify({ "message": f"Update successful: {decoded_id}" })


@application.route('/edit/<id>', methods=['GET'])
def get_editable_course_data(id: str):
	print(f'application.py: /edit/{id}')
	decoded_id = unquote(id)
	assignment_file = load_assignment_file()

	if decoded_id not in assignment_file.sections:
		return jsonify({"error": "Course not found"}), 404

	section = assignment_file.sections[decoded_id]

	return jsonify({
		"id": section.id,
		"room": section.room,
		"meeting1": section.meeting_pattern,
		"crossListings": section.cross_listings,
		"maxEnrollment": section.max_enrollment,
		"enrollment": section.enrollment,
		"comments": section.comments
	})

@application.route('/conflicts/active', methods=['GET'])
def conflicts_active():
	"""
	Returns [Conflict] array to populate the conflict pane
	for an AssignmentFile. (active tab)

	This is returned in a List so we can iterate over each
	Conflict object to populate each conflict box component
	on the FrontEnd.
	"""
	af   = load_assignment_file()
	resp = []
	for idx, c in enumerate(af.conflicts):
		if c.ignored:
			continue
		resp.append({
			"id": str(idx),
			"content": render_conflict(c),
			"ignored": False
		})
	return jsonify(resp)


@application.route('/conflicts/ignored', methods=['GET'])
def conflicts_ignored():
	"""
	Returns [Conflict] array to populate the conflict pane
	for an AssignmentFile. (ignore tab)

	This is returned in a List so we can iterate over each
	Conflict object to populate each conflict box component
	on the FrontEnd.
	"""
	af   = load_assignment_file()
	resp = []
	for idx, c in enumerate(af.conflicts):
		if not c.ignored:
			continue
		resp.append({
			"id": str(idx),
			"content": render_conflict(c),
			"ignored": True
		})
	return jsonify(resp)


@application.route('/conflict/ignore/<id>', methods=['PUT'])
def conflict_ignore(id: str):
	print(f'[ROUTE HIT] /conflict/ignore/<id>')
	try:
		i = int(id)
		af = load_assignment_file()
		af.conflicts[i].ignored = True
		rebuild_conflict_lists(af)
		save_assignment_file(af)
		return '', 204
	except (ValueError, IndexError):
		return 'invalid id', 400

@application.route('/conflict/activate/<id>', methods=['PUT'])
def conflict_activate(id: str):
	print(f'[ROUTE HIT] /conflict/activate/<id>')
	try:
		i = int(id)
		af = load_assignment_file()
		af.conflicts[i].ignored = False
		rebuild_conflict_lists(af)
		save_assignment_file(af)
		return '', 204
	except (ValueError, IndexError):
		return 'invalid id', 400


@application.route('/api/course-info')
@jwt_required()
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
def upload():
	print(f'[ROUTE HIT] /upload')
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

		try:
			old_af = load_assignment_file()
			old_conflicts = old_af.conflicts
		except Exception:
			old_conflicts = []

		sections, classrooms, new_conflicts = build_all()
		
		for sec in sections.values():
			sec.parsed_meetings = parse_meetings(sec.meeting_pattern)
			sec.rooms = parse_rooms(sec.room)
			sec.room_numbers = extract_room_numbers(sec.rooms)
			sec.schedule, sec.warning = combine_section_info(sec.id, sec.parsed_meetings, sec.rooms)

		for classroom in classrooms.values():
			classroom.schedule = [[] for _ in range(7 * 1440)]

		for sec in sections.values():
			for (_, room_name, _, _, _) in sec.schedule:
				if room_name in classrooms:
					classrooms[room_name].add_course_section_object(sec)

		preserved_conflicts = preserve_ignored_conflicts(old_conflicts, new_conflicts)
		assignment_file = AssignmentFile(sections, classrooms, preserved_conflicts)
		save_assignment_file(assignment_file)

		print('application.py: /upload')
		return jsonify({"message": "File uploaded and memory updated", "filename": file.filename})

	print('application.py: /upload')
	return jsonify({"message": "Invalid file format. Only CSV files are allowed."}), 400




@application.route('/api/columns', methods=['GET'])
def get_all_column_keys():
	from Model.CourseSection import CourseSectionEnum
	columns = [e.name for e in CourseSectionEnum]
	return jsonify({"columns": columns})

@application.route('/api/download', methods=['GET'])
def download_csv():
	assignment_file = load_assignment_file()

	export(assignment_file.sections)

	base_dir = os.path.dirname(__file__)
	file_path = os.path.join(base_dir, 'Files', 'Exports', OUTPUT_CSV)

	if not os.path.exists(file_path):
		return jsonify({"error": "File not found"}), 404

	return send_file(
		file_path,
		as_attachment=True,
		download_name='room_assignments.csv',
		mimetype='text/csv'
	)


@application.route('/api/data', methods=['GET'])
@jwt_required()
def get_data():
	print(f'[ROUTE HIT] /api/data')
	assignment_file = load_assignment_file()

	for sec in assignment_file.sections.values():
		sec.parsed_meetings = parse_meetings(sec.meeting_pattern)
		sec.rooms = parse_rooms(sec.room)
		sec.room_numbers = extract_room_numbers(sec.rooms)
		sec.schedule, sec.warning = combine_section_info(sec.id, sec.parsed_meetings, sec.rooms)

	# Clear all classroom minute schedules
	for classroom in assignment_file.classrooms.values():
		classroom.schedule = [[] for _ in range(7 * 1440)]

	# Re-add sections to classrooms
	for sec in assignment_file.sections.values():
		for (_, room_name, _, _, _) in sec.schedule:
			if room_name in assignment_file.classrooms:
				assignment_file.classrooms[room_name].add_course_section_object(sec)

	# Rebuild and preserve previous conflicts
	new_conflicts = build_conflicts(assignment_file.sections, assignment_file.classrooms)
	assignment_file.conflicts = preserve_ignored_conflicts(assignment_file.conflicts, new_conflicts)
	rebuild_conflict_lists(assignment_file)
	save_assignment_file(assignment_file)

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
		entry["id"] = section.id
		for j, attr in enumerate(attributes):
			entry[attr.name] = values[j]

		data.append(entry)

	print('application.py: /api/data')
	return jsonify({"courses": data})



@application.route('/assignment-files', methods=['GET'])
def get_assignment_files():
	"""
	For displaying file names in the file-manager pane.
	"""
	rows = af_db.list_assignment_files() or []   # old code might explode on None
	return jsonify([{'id': r[0], 'filename': r[1]} for r in rows])

@application.route('/assignment-file/<int:fid>', methods=['GET'])
def load_assignment_file_from_db(fid: int):
	print(f'[ROUTE HIT] /assignment-file/<int:fid>')
	try:
		prev_af = load_assignment_file()
		prev_conflicts = prev_af.conflicts
	except Exception:
		prev_conflicts = []

	af = af_db.load_assignment_file(fid)
	if af is None:
		return 'file not found', 404

	af.conflicts = preserve_ignored_conflicts(prev_conflicts, af.conflicts)
	rebuild_conflict_lists(af)
	save_assignment_file(af)
	return '', 204


@application.route('/assignment-file/init/<int:fid>', methods=['POST'])
def init_assignment_file_from_db(fid: int):
	print(f'[ROUTE HIT] /assignment-file/init/<int:fid>')
	try:
		prev_af = load_assignment_file()
		prev_conflicts = prev_af.conflicts
	except Exception:
		prev_conflicts = []

	try:
		af = af_db.load_assignment_file(fid)
		if af is None:
			raise ValueError(f"Assignment file with ID {fid} not found.")

		af.conflicts = preserve_ignored_conflicts(prev_conflicts, af.conflicts)
		rebuild_conflict_lists(af)
		save_assignment_file(af)

		return '', 204
	except ValueError as e:
		return str(e), 404


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
	section_csv_file = os.path.join(base_dir, application.config['UPLOAD_FOLDER'], INPUT_CSV)
	return csf.build_course_sections(section_csv_file)

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

@application.route('/api/data/columns', methods=['POST'])
def get_data_with_columns():
	data = request.get_json()
	selected_cols = data.get("columns", [])

	# convert strings to CourseSectionEnum members
	attributes = [CourseSectionEnum[col] for col in selected_cols]

	assignment_file = load_assignment_file()
	data_row_list = generate_strings_section_view(assignment_file.sections, attributes)

	section_keys = list(assignment_file.sections.keys())
	result = []

	for i, row in enumerate(data_row_list):
		values = row.split(" | ")
		section = assignment_file.sections[section_keys[i]]
		entry = {"id": section.id}
		for j, attr in enumerate(attributes):
			entry[attr.name] = values[j]
		result.append(entry)

	return jsonify({"courses": result})


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
	try:
		with open('assignment_file.pkl', 'rb') as f:
			return pickle.load(f)
	except FileNotFoundError:
		return AssignmentFile({}, {}, [])

	
def make_assignment_file(sections: Dict[str,CourseSection], classrooms: Dict[str,Classroom], conflicts: List[Conflict]):
	assignment_file = AssignmentFile(sections, classrooms, conflicts)
	return assignment_file

def rebuild_conflict_lists(assignment_file):
    assignment_file.active_conflicts  = [conflict for conflict in assignment_file.conflicts if not conflict.ignored]
    assignment_file.ignored_conflicts = [conflict for conflict in assignment_file.conflicts if conflict.ignored]

def render_conflict(c: Conflict) -> str:
	if not c.sections:
		return "<h2>Conflict:</h2><p>No section data available</p><br>"
	title = f"<h2>Conflict: {c.sections[0].rooms}</h2>" if hasattr(c.sections[0], 'rooms') else "<h2>Conflict:</h2>"
	if c.conflict_message:
		return f"{title}<p>{c.conflict_message}</p><br>"
	parts = ''.join(
		f"<p>{s.id or ''}:</p><p>{s.meeting_pattern or ''}</p><br>"
		for s in c.sections
	)

	return f"{title}{parts}"

def preserve_ignored_conflicts(old_conflicts: List[Conflict], new_conflicts: List[Conflict]) -> List[Conflict]:
	def signature(c: Conflict):
		ids = tuple(sorted(s.id for s in c.sections))
		return (ids, c.conflict_message)

	ignored_signatures = {
		signature(c)
		for c in old_conflicts if c.ignored
	}

	for c in new_conflicts:
		if signature(c) in ignored_signatures:
			c.ignored = True

	return new_conflicts

#....................................................................................
# DB Stuff

def persist_current_assignment_file(af: AssignmentFile):
	af_db.store_assignment_file(af)

def load_assignmentfile_from_db_and_initialize_state(fid: int):
	af = af_db.load_assignment_file(fid)
	if af is None:
		raise ValueError(f"Assignment file with ID {fid} not found.")

	ignored_conflicts = af._ignored_conflicts.copy()

	rebuild_conflict_lists(af)

	af._ignored_conflicts = ignored_conflicts
	save_assignment_file(af)








#....................................................................................
if __name__ == '__main__':
	application.run(debug=True)
#....................................................................................