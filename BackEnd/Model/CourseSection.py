#....................................................................................
# CourseSection Datamodel:
#____________________________________________________________________________________
#
# Enum codes, like DEPARTMENT_CODE, should be uppercase version of class object
# variables like department_code. Logic in the data formatter relies on this
# convention in the row_to_string() function.
#
#
#....................................................................................


from enum import Enum
from typing import Dict, List, Tuple
import re
from collections import defaultdict, Counter

class CourseSectionEnum(Enum):
	DEPARTMENT_CODE    = 'Department Code'
	SUBJECT_CODE       = 'Subject Code'
	CATALOG_NUMBER     = 'Catalog Number'
	SECTION            = 'Section #'
	COURSE_TITLE       = 'Course Title'
	SECTION_TYPE       = 'Section Type'
	TITLE_TOPIC        = 'Title/Topic'
	MEETING_PATTERN    = 'Meeting Pattern'
	MEETINGS           = 'Meetings'
	INSTRUCTOR         = 'Instructor'
	ROOM               = 'Room'
	SESSION            = 'Session'
	CAMPUS             = 'Campus'
	INST_METHOD        = 'Inst. Method'
	CONSENT            = 'Consent'
	CREDIT_HOURS_MIN   = 'Credit Hrs Min'
	CREDIT_HOURS       = 'Credit Hrs'
	GRADE_MODE         = 'Grade Mode'
	ATTRIBUTES         = 'Attributes'
	COURSE_ATTRIBUTES  = 'Course Attributes'
	ENROLLMENT         = 'Enrollment'
	MAX_ENROLLMENT     = 'Maximum Enrollment'
	WAIT_CAP           = 'Wait Cap'
	RM_CAP_REQUEST     = 'Rm Cap Request'
	CROSS_LISTINGS     = 'Cross-listings'
	CROSS_LIST_MAX     = 'Cross-list Maximum'
	CROSS_LIST_WAIT_CAP= 'Cross-list Wait Cap'
	LINK_TO            = 'Link To'
	COMMENTS           = 'Comments'
	NOTES1             = 'Notes#1'
	NOTES2             = 'Notes#2'


def lower(self):
	return self.lower

def parse_rooms(room: str) -> List[str]:
	if not room:
		return []

	# Split on semicolons or commas, and normalize
	parts = [part.strip() for part in room.replace(",", ";").split(";") if part.strip()]
	output = []

	for part in parts:
		if part.lower() == 'partially online':
			continue

		if part.isdigit() or part.lower().startswith("pki"):
			number = ''.join(filter(str.isdigit, part))
			output.append(f"Peter Kiewit Institute {number}")
		else:
			output.append(part)

	return output

    
def parse_meetings(line: str) -> List[Tuple[str, int, int]]:
	meetings = []
	for chunk in line.split(';'):
		parts = chunk.strip().split(maxsplit=2)
		if len(parts) < 2:
			continue
		days = parts[0]	# ex) "MW" or "TRF"
		time_range = parts[1]	# ex) "3pm-4:15pm"
		if '-' not in time_range:
			continue
		start_str, end_str = time_range.split('-')
		start_min = parse_time(start_str)
		end_min = parse_time(end_str)
		for d in days:	# days ex) "MW" -> ['M','W']
			meetings.append((d, start_min, end_min))
	return meetings

def parse_time(timestr: str) -> int:
	match = re.match(r'(\d{1,2})(?::(\d{2}))?(am|pm)', timestr.strip().lower())
	if not match:
		return 0
	hour = int(match.group(1))
	minute = int(match.group(2)) if match.group(2) else 0
	ampm = match.group(3)
	if ampm == 'pm' and hour != 12:
		hour += 12
	elif ampm == 'am' and hour == 12:
		hour = 0
	return hour * 60 + minute

def extract_room_numbers(rooms: List[str]) -> List[str]:
	if not rooms:
		return []
	room_numbers = []
	for r in rooms:
		match = re.search(r'\d+', r)
		room_numbers.append(match.group() if match else "To Be Announced")
	return room_numbers

def time_to_str(minutes: int) -> str:
		hour = minutes // 60
		minute = minutes % 60
		ampm = "am"
		if hour == 0:
			hour = 12
		elif hour == 12:
			ampm = "pm"
		elif hour > 12:
			hour -= 12
			ampm = "pm"
		return f"{hour}:{minute:02}{ampm}"


def combine_section_info(
	section_id: str,
	meeting_times: List[Tuple[str, int, int]],
	rooms: List[str]) -> Tuple[List[Tuple[str, str, str, int, int]], str]:
	results = []
	warning = ""

	# single room => all times get that one room
	if len(rooms) == 1:
		for (day, start, end) in meeting_times:
			results.append((section_id, rooms[0], day, start, end))
		return results, warning

	# same count => pair in order
	if len(rooms) == len(meeting_times):
		for ((day, start, end), rm) in zip(meeting_times, rooms):
			results.append((section_id, rm, day, start, end))
		return results, warning

	# Condition 2a: two rooms, one meeting => double-booking
	if len(rooms) == 2 and len(meeting_times) == 1:
		(day, start, end) = meeting_times[0]
		results.append((section_id, rooms[0], day, start, end))
		results.append((section_id, rooms[1], day, start, end))
		return results, warning

	# Condition 1: two rooms, multiple meetings
	if len(rooms) == 2 and len(meeting_times) > 2:
		se_counts = Counter((mt[1], mt[2]) for mt in meeting_times)
		dup_start_end = [x for x, c in se_counts.items() if c > 1]
		if dup_start_end:
			# find second occurrence of that start-end
			(start_dup, end_dup) = dup_start_end[0]
			first_idx = None
			split_idx = None
			for i, (day, s, e) in enumerate(meeting_times):
				if s == start_dup and e == end_dup:
					if first_idx is None:
						first_idx = i
					else:
						split_idx = i
						break
			for i, (day, s, e) in enumerate(meeting_times):
				r = rooms[0] if split_idx and i < split_idx else rooms[1]
				results.append((section_id, r, day, s, e))
		else:
			# last time => second room, others => first
			for i, (day, s, e) in enumerate(meeting_times):
				if i == len(meeting_times) - 1:
					results.append((section_id, rooms[1], day, s, e))
				else:
					results.append((section_id, rooms[0], day, s, e))
		return results, warning

	# Condition 2b: more rooms than times
	if len(rooms) > 2 and len(meeting_times) > len(rooms):
		warning = f'Condition 2b triggered: 3+ rooms and 4+ meeting times. Make sure {section_id} has correct meeting times with each room it uses. Unable to determine automatically.'

	# Condition 3: len(rooms) > 2, len(meetings) > 3 => assign from the back
	if len(rooms) > 2 and len(meeting_times) > 3:
		mt_idx = len(meeting_times) - 1
		rm_idx = len(rooms) - 1
		while rm_idx >= 0 and mt_idx >= 0:
			day, start, end = meeting_times[mt_idx]
			results.append((section_id, rooms[rm_idx], day, start, end))
			mt_idx -= 1
			rm_idx -= 1
		while mt_idx >= 0:
			day, start, end = meeting_times[mt_idx]
			results.append((section_id, rooms[0], day, start, end))
			mt_idx -= 1
		results.reverse()
		return results, warning
	else:
		# Fallback: pair in order until one runs out
		warning = warning or f'Ambiguity in the meeting times versus rooms. Make sure {section_id} has correct meeting times with each room it uses.'
		for i, mt in enumerate(meeting_times):
			r = rooms[min(i, len(rooms)-1)]
			results.append((section_id, r, mt[0], mt[1], mt[2]))

		return results, warning

def parse_crosslistings(text):
	pattern = r"\b([A-Za-z]{3,5}(?:[\s-]\d{1,4}[A-Za-z]?)-)0*(\d{1,3})\b"
	matches = re.findall(pattern, text)
	section_ids = [m[0] + m[1] for m in matches]
	return section_ids

class CourseSection:
	def __init__(self, attributes: Dict[str, str]) -> None:
		self._department_code   = attributes[		CourseSectionEnum.DEPARTMENT_CODE.value]
		self._subject_code      = attributes[		CourseSectionEnum.SUBJECT_CODE.value]
		self._catalog_number    = attributes[		CourseSectionEnum.CATALOG_NUMBER.value]
		self._section           = attributes[		CourseSectionEnum.SECTION.value]
		self._course 			= f'{self._catalog_number} {self._section}'
		self._course_title      = attributes[		CourseSectionEnum.COURSE_TITLE.value]
		self._section_type      = attributes[		CourseSectionEnum.SECTION_TYPE.value]
		self._title_topic       = attributes[		CourseSectionEnum.TITLE_TOPIC.value]
		self._meeting_pattern   = attributes[		CourseSectionEnum.MEETING_PATTERN.value]
		self._instructor        = attributes[		CourseSectionEnum.INSTRUCTOR.value]
		self._room = (
			attributes.get(CourseSectionEnum.ROOM.value)
			if "Peter Kiewit Institute" in str(attributes.get(CourseSectionEnum.ROOM.value, ""))
			else "To Be Announced")
		self._session           = attributes[		CourseSectionEnum.SESSION.value]
		self._campus            = attributes[		CourseSectionEnum.CAMPUS.value]
		self._inst_method       = attributes[		CourseSectionEnum.INST_METHOD.value]
		self._consent           = attributes[		CourseSectionEnum.CONSENT.value]
		self._credit_hours_min  = attributes[	    CourseSectionEnum.CREDIT_HOURS_MIN.value]
		self._credit_hours      = attributes[   	CourseSectionEnum.CREDIT_HOURS.value]
		self._grade_mode        = attributes[		CourseSectionEnum.GRADE_MODE.value]
		self._attributes        = attributes[		CourseSectionEnum.ATTRIBUTES.value]
		self._course_attributes = attributes[		CourseSectionEnum.COURSE_ATTRIBUTES.value]
		self._enrollment        = attributes[	    CourseSectionEnum.ENROLLMENT.value]
		self._max_enrollment    = attributes[	    CourseSectionEnum.MAX_ENROLLMENT.value]
		self._wait_cap          = attributes[	    CourseSectionEnum.WAIT_CAP.value]
		self._rm_cap_request    = attributes[	    CourseSectionEnum.RM_CAP_REQUEST.value]
		self._cross_listings    = attributes[		CourseSectionEnum.CROSS_LISTINGS.value]
		self._cross_list_max    = attributes[		CourseSectionEnum.CROSS_LIST_MAX.value]
		self._cross_list_wait_cap = attributes[	    CourseSectionEnum.CROSS_LIST_WAIT_CAP.value]
		self._link_to           = attributes[		CourseSectionEnum.LINK_TO.value]
		self._comments          = attributes[		CourseSectionEnum.COMMENTS.value]
		self._notes1            = attributes[		CourseSectionEnum.NOTES1.value]
		try:
			self._notes2            = attributes[		CourseSectionEnum.NOTES2.value]
		except:
			self._notes2			= ""

		self._id = f'{self._subject_code} {self._catalog_number}-{self._section}'
		self._parsed_meetings = parse_meetings(self._meeting_pattern)
		self._start_time = [self._parsed_meetings[0][1]] if parse_meetings(self._meeting_pattern) else -1
		self._end_time   = [self._parsed_meetings[0][2]] if parse_meetings(self._meeting_pattern) else -1
		self._rooms = parse_rooms(self._room)
		self._room_numbers = extract_room_numbers(self._rooms)
		self._schedule,self._warning = combine_section_info(self._id, self._parsed_meetings, self._rooms)
		self.update_meetings(self._schedule)

		self._room_freq = {}
		
		self._crosslistings_cleaned = parse_crosslistings(self._cross_listings)


	def update_meetings(self, value: List[Tuple[str, str, str, int, int]]) -> None:

		if not value:
			self._parsed_meetings = []
			self._meeting_pattern = ""
			self._room = ""
			return

		self._parsed_meetings = [(day, start, end) for _, _, day, start, end in value]
		
		groups = defaultdict(list)
		for section_id, room, day, start, end in value:
			groups[(room, start, end)].append(day)
		chunks = []
		all_rooms = []
		for (room, start, end), days in groups.items():
			days_str = "".join(sorted(days))
			chunks.append(f"{days_str} {time_to_str(start)}-{time_to_str(end)}")
			all_rooms.append(room)
		self._meeting_pattern = "; ".join(chunks)
		self._room = "; ".join(sorted(set(all_rooms)))
		self._schedule,_ = combine_section_info(self._id, self._parsed_meetings, self._rooms)

	@property
	def warning(self) -> str:
		return self._warning

	@warning.setter
	def warning(self, value: str) -> None:
		self._warning = value 

	@property
	def crosslistings_cleaned(self) -> List:
		return self._crosslistings_cleaned

	@crosslistings_cleaned.setter
	def crosslistings_cleaned(self, value: List) -> None:
		self._crosslistings_cleaned = value 

	@property
	def start_time(self) -> int:
		return self._start_time

	@start_time.setter
	def start_time(self, value: int) -> None:
		self._start_time = value 

	@property
	def end_time(self) -> int:
		return self._end_time

	@end_time.setter
	def end_time(self, value: int) -> None:
		self._end_time = value 

	@property
	def course(self) -> str:
		return self._course

	@course.setter
	def course(self, value: str) -> None:
		self._course = value 

	@property
	def schedule(self) -> List:
		return self._schedule

	@schedule.setter
	def schedule(self, value: List) -> None:
		self._schedule = value 

	@property
	def room_freq(self) -> Dict[str, int]:
		return self._room_freq

	@room_freq.setter
	def room_freq(self, value: Dict[str, int]) -> None:
		self._room_freq = value 

	@property
	def room_numbers(self) -> List:
		return self._room_numbers

	@room_numbers.setter
	def room_numbers(self, value: List) -> None:
		self._room_numbers = value 

	@property
	def parsed_meetings(self) -> List:
		return self._parsed_meetings

	@parsed_meetings.setter
	def parsed_meetings(self, value: List) -> None:
		self._parsed_meetings = value

	@property
	def rooms(self) -> List:
		return self._rooms

	@rooms.setter
	def rooms(self, value) -> None:
		if isinstance(value, str):
			self._rooms = parse_rooms(value)
		elif isinstance(value, list):
			self._rooms = value
		else:
			raise TypeError("rooms must be a string or a list of strings")

	def add_room(self, value: str) -> None:
		self._rooms.append(value)

	@property
	def id(self) -> str:
		return self._id

	@id.setter
	def id(self, value: str) -> None:
		self._id = value

	@property
	def department_code(self) -> str:
		return self._department_code

	@department_code.setter
	def department_code(self, value: str) -> None:
		self._department_code = value

	@property
	def subject_code(self) -> str:
		return self._subject_code

	@subject_code.setter
	def subject_code(self, value: str) -> None:
		self._subject_code = value

	@property
	def catalog_number(self) -> str:
		return self._catalog_number

	@catalog_number.setter
	def catalog_number(self, value: str) -> None:
		self._catalog_number = value

	@property
	def section(self) -> str:
		return self._section

	@section.setter
	def section(self, value: str) -> None:
		self._section = value

	@property
	def course_title(self) -> str:
		return self._course_title

	@course_title.setter
	def course_title(self, value: str) -> None:
		self._course_title = value

	@property
	def section_type(self) -> str:
		return self._section_type

	@section_type.setter
	def section_type(self, value: str) -> None:
		self._section_type = value

	@property
	def title_topic(self) -> str:
		return self._title_topic

	@title_topic.setter
	def title_topic(self, value: str) -> None:
		self._title_topic = value

	@property
	def meeting_pattern(self) -> str:
		return self._meeting_pattern

	@meeting_pattern.setter
	def meeting_pattern(self, value: str) -> None:
		self._meeting_pattern = value

	@property
	def meetings(self) -> str:
		return self._meetings

	@meetings.setter
	def meetings(self, value: str) -> None:
		self._meetings = value

	@property
	def instructor(self) -> str:
		return self._instructor

	@instructor.setter
	def instructor(self, value: str) -> None:
		self._instructor = value

	@property
	def room(self) -> str:
		return self._room

	@room.setter
	def room(self, value: str) -> None:
		self._room = value

	@property
	def session(self) -> str:
		return self._session

	@session.setter
	def session(self, value: str) -> None:
		self._session = value

	@property
	def campus(self) -> str:
		return self._campus

	@campus.setter
	def campus(self, value: str) -> None:
		self._campus = value

	@property
	def inst_method(self) -> str:
		return self._inst_method

	@inst_method.setter
	def inst_method(self, value: str) -> None:
		self._inst_method = value

	@property
	def consent(self) -> str:
		return self._consent

	@consent.setter
	def consent(self, value: str) -> None:
		self._consent = value

	@property
	def credit_hours_min(self) -> int:
		return self._credit_hours_min

	@credit_hours_min.setter
	def credit_hours_min(self, value: int) -> None:
		self._credit_hours_min = value

	@property
	def credit_hours(self) -> int:
		return self._credit_hours

	@credit_hours.setter
	def credit_hours(self, value: int) -> None:
		self._credit_hours = value

	@property
	def grade_mode(self) -> str:
		return self._grade_mode

	@grade_mode.setter
	def grade_mode(self, value: str) -> None:
		self._grade_mode = value

	@property
	def attributes(self) -> str:
		return self._attributes

	@attributes.setter
	def attributes(self, value: str) -> None:
		self._attributes = value

	@property
	def course_attributes(self) -> str:
		return self._course_attributes

	@course_attributes.setter
	def course_attributes(self, value: str) -> None:
		self._course_attributes = value

	@property
	def enrollment(self) -> int:
		return self._enrollment

	@enrollment.setter
	def enrollment(self, value: int) -> None:
		self._enrollment = value

	@property
	def max_enrollment(self) -> int:
		return self._max_enrollment

	@max_enrollment.setter
	def max_enrollment(self, value: int) -> None:
		self._max_enrollment = value

	@property
	def wait_cap(self) -> int:
		return self._wait_cap

	@wait_cap.setter
	def wait_cap(self, value: int) -> None:
		self._wait_cap = value

	@property
	def rm_cap_request(self) -> int:
		return self._rm_cap_request

	@rm_cap_request.setter
	def rm_cap_request(self, value: int) -> None:
		self._rm_cap_request = value

	@property
	def cross_listings(self) -> str:
		return self._cross_listings

	@cross_listings.setter
	def cross_listings(self, value: str) -> None:
		self._cross_listings = value

	@property
	def cross_list_max(self) -> str:
		return self._cross_list_max

	@cross_list_max.setter
	def cross_list_max(self, value: str) -> None:
		self._cross_list_max = value

	@property
	def cross_list_wait_cap(self) -> int:
		return self._cross_list_wait_cap

	@cross_list_wait_cap.setter
	def cross_list_wait_cap(self, value: int) -> None:
		self._cross_list_wait_cap = value

	@property
	def link_to(self) -> str:
		return self._link_to

	@link_to.setter
	def link_to(self, value: str) -> None:
		self._link_to = value

	@property
	def comments(self) -> str:
		return self._comments

	@comments.setter
	def comments(self, value: str) -> None:
		self._comments = value

	@property
	def notes1(self) -> str:
		return self._notes1

	@notes1.setter
	def notes1(self, value: str) -> None:
		self._notes1 = value

	@property
	def notes2(self) -> str:
		return self._notes2

	@notes2.setter
	def notes2(self, value: str) -> None:
		self._notes2 = value
