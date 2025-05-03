from enum import Enum
import re
from typing import Dict, List, Tuple
from Model.CourseSection import CourseSection

DAY_OFFSETS = {
	'M': 0 * 1440,
	'T': 1 * 1440,
	'W': 2 * 1440,
	'R': 3 * 1440,
	'F': 4 * 1440,
	'S': 5 * 1440
}

SUBJECT_CODES = {
	"AREN": "Architectural Engineering",
	"BIOI": "Bioinformatics",
	"BMI": "Biomedical Informatics",
	"CIST": "College of Information Science & Technology",
	"CIVE": "Civil Engineering",
	"CNST": "Construction Management",
	"CONE": "Construction Engineering",
	"CSCI": "Computer Science",
	"CYBR": "Cybersecurity",
	"ECEN": "Electrical & Computer Engineering",
	"ENGR": "Engineering",
	"ENVE": "Environmental Engineering",
	"HONR": "Honors Program",
	"ISQA": "Information Systems & Quantitative Analysis",
	"ITIN": "IT Innovation",
	"MATH": "Mathematics",
	"MECH": "Mechanical Engineering",
	"SCMT": "Supply Chain Management"
}

#....................................................................................
def parse_time(timestr: str) -> int:
	"""
	Convert a time string like '3pm' or '10:30am' into total minutes from midnight
	"""

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

#....................................................................................
def parse_meeting_line(line: str) -> List[Tuple[str, int, int]]:
	"""
	Break a string like 'MW 3pm-4:15pm' into a list of day/start/end time tuples
	"""

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
		for d in days:	# ex) "MW" -> ['M','W']
			meetings.append((d, start_min, end_min))
	return meetings

#....................................................................................
def strip_decimal(attribute: str) -> str:
	"""
	Strip trailing '.0'
	"""

	if attribute.endswith(".0"):
		attribute = attribute[:-2]
		return attribute
	return attribute

#....................................................................................
class ClassroomEnum(Enum):
	ROOM             		= 'Room Number'
	SEATS                   = 'Seats'
	DISPLAYS                = 'Displays'
	COMPUTER_COUNT          = 'Computer Count'
	INFO_AND_CONNECTIVITY   = 'Information and Connectivity'

#....................................................................................
class Classroom:
	def __init__(self, attributes: Dict[str, str]) -> None:
		self._room		             = attributes[ClassroomEnum.ROOM.value]
		self._seats                  = strip_decimal(attributes[ClassroomEnum.SEATS.value])
		self._displays               = attributes[ClassroomEnum.DISPLAYS.value]
		self._computer_count         = attributes[ClassroomEnum.COMPUTER_COUNT.value]
		self._info_and_connectivity  = attributes[ClassroomEnum.INFO_AND_CONNECTIVITY.value]
		self._sections				 = []
		self._assigned				 = [True if self._room else False]
		self._department_counts             = {}

		# A 1440 * possible_days = total items
		self._minute_schedule: List[List[str]] = [[] for _ in range(7 * 1440)]

#....................................................................................
	@property
	def department_counts(self) -> Dict:
		return self._department_counts

	@department_counts.setter
	def department_counts(self, value: Dict) -> None:
		self._department_counts = value

	@property
	def assigned(self) -> bool:
		return bool(self._room)

	@property
	def sections(self) -> List:
		return self._sections
	
	def add_section(self, value: CourseSection) -> None:
		self._sections.append(value)

	@sections.setter
	def sections(self, value: List) -> None:
		self._sections = value

	@property
	def room(self) -> str:
		return self._room

	@room.setter
	def room(self, value: str) -> None:
		self._room = value

	@property
	def seats(self) -> str:
		return self._seats

	@seats.setter
	def seats(self, value: str) -> None:
		self._seats = value

	@property
	def displays(self) -> str:
		return self._displays

	@displays.setter
	def displays(self, value: str) -> None:
		self._displays = value

	@property
	def computer_count(self) -> str:
		return self._computer_count

	@computer_count.setter
	def computer_count(self, value: str) -> None:
		self._computer_count = value

	@property
	def info_and_connectivity(self) -> str:
		return self._info_and_connectivity

	@info_and_connectivity.setter
	def info_and_connectivity(self, value: str) -> None:
		self._info_and_connectivity = value

	@property
	def schedule(self) -> List[List[str]]:
		return self._minute_schedule

	@schedule.setter
	def schedule(self, value: List[List[str]]) -> None:
		self._minute_schedule = value

#....................................................................................
	def add_course_section(self, course_id: str, room: str, start_slot: int, end_slot: int) -> None:
		"""
		Sets a time range in the schedule for a course in this room
		"""

		for minute in range(start_slot, end_slot):
			if room != ['To Be Announced']:
				self._minute_schedule[minute].append(course_id)

#....................................................................................
	def remove_course_section(self, course_id: str) -> None:
		"""
		Remove a course from all minutes it was occupying in the schedule
		"""

		for minute_list in self._minute_schedule:
			while course_id in minute_list:
				minute_list.remove(course_id)

#....................................................................................
	def add_course_section_object(self, course_section_object: CourseSection) -> None:
		"""
		Insert a course section object into the schedule
		"""

		schedule = course_section_object.schedule
		self.add_section(course_section_object)

		
		course_section_object.update_meetings(schedule)


		for section_id, room, d, start_min, end_min in schedule:
			if d in DAY_OFFSETS:
				day_offset = DAY_OFFSETS[d]
				start_slot = day_offset + start_min
				end_slot = day_offset + end_min
				self.add_course_section(section_id, room, start_slot, end_slot)

#....................................................................................
	def gather_intervals(self) -> List[Tuple[str, int, int]]:
		"""
		Convert the minute schedule into a list of course times
		"""

		intervals: List[Tuple[str, int, int]] = []

		all_courses = set()
		for minute_list in self._minute_schedule:
			all_courses.update(minute_list)

		for cid in all_courses:
			in_block = False
			block_start = 0

			for minute in range(7 * 1440):
				if cid in self._minute_schedule[minute]:
					if not in_block:
						in_block = True
						block_start = minute
				else:
					if in_block:
						intervals.append((cid, block_start, minute))
						in_block = False
			if in_block:
				intervals.append((cid, block_start, 7 * 1440))
		return intervals

#....................................................................................
	def find_conflicts(self) -> List[Tuple[str, int, int, str, int, int]]:
		"""
		Check for overlapping intervals for courses and return conflicts
		"""

		conflict_set = set()
		intervals = self.gather_intervals()

		for i in range(len(intervals)):
			cid1, start1, end1 = intervals[i]
			for j in range(i + 1, len(intervals)):
				cid2, start2, end2 = intervals[j]
				if cid1 == cid2:
					continue
				if start1 < end2 and start2 < end1:
					# Reduces redundancy by making a conflict signature (canonical form)
					conflict = tuple(sorted([(cid1, start1, end1), (cid2, start2, end2)]))
					conflict_set.add(conflict)
		
		# Convert set items back to flat tuples if needed.
		conflicts = [first + second for first, second in conflict_set]
		return conflicts