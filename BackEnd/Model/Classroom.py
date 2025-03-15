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

#....................................................................................
#####################################################################################
# 	Convert something like "9am" or "10:30pm" to minutes (0..1439) from midnight.
#....................................................................................
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

#....................................................................................
#####################################################################################
# 	Given "MW 3pm-4:15pm; F 8:30am-10:20am", return a list of (day, start_min, end_min).
#	For example: [('M', 900, 975), ('W', 900, 975), ('F', 510, 620)].
#....................................................................................
def parse_meeting_line(line: str) -> List[Tuple[str, int, int]]:
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

def make_int_str(attribute: str) -> str:
	if attribute.endswith(".0"):
		attribute = attribute[:-2]
		return attribute
	return attribute

class ClassroomEnum(Enum):
	ROOM             = 'Room Number'
	SEATS                   = 'Seats'
	DISPLAYS                = 'Displays'
	COMPUTER_COUNT          = 'Computer Count'
	INFO_AND_CONNECTIVITY   = 'Information and Connectivity'
	#DEPARTMENT              = 'Department'

class Classroom:
	def __init__(self, attributes: Dict[str, str]) -> None:
		self._room		             = attributes[ClassroomEnum.ROOM.value]
		self._seats                  = make_int_str(attributes[ClassroomEnum.SEATS.value])
		self._displays               = attributes[ClassroomEnum.DISPLAYS.value]
		self._computer_count         = attributes[ClassroomEnum.COMPUTER_COUNT.value]
		self._info_and_connectivity  = attributes[ClassroomEnum.INFO_AND_CONNECTIVITY.value]
		# self._department             = attributes[ClassroomEnum.DEPARTMENT.value]

		# A 1440 * possible_days = total slots if we combine days into one array.
		# For simplicity, we’ll do only 1440 per day and add offsets for T/W/etc. below.
		# This example just keeps 7*1440 to handle up to Saturday.
		self._minute_schedule: List[List[str]] = [[] for _ in range(7 * 1440)]

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

#....................................................................................
#####################################################################################
# 	# Occupies minutes [start_slot, end_slot) in the _minute_schedule.
#....................................................................................
	def add_course_section(self, course_id: str, start_slot: int, end_slot: int) -> None:
		for minute in range(start_slot, end_slot):
			self._minute_schedule[minute].append(course_id)

#....................................................................................
#####################################################################################
# 	Removes course_id from all minutes in the schedule.
#....................................................................................
	def remove_course_section(self, course_id: str) -> None:
		for minute_list in self._minute_schedule:
			while course_id in minute_list:
				minute_list.remove(course_id)

#....................................................................................
#####################################################################################
# 	Parses course_section_object.meetings (assuming it's something like
#	'MW 3pm-4:15pm; F 8:30am-10:20am') and adds it to this room's schedule.
#....................................................................................
	def add_course_section_object(self, course_section_object) -> None:
		meeting_str = course_section_object.parsed_meetings
		course_id = f"{course_section_object.id}"
		for d, start_min, end_min in meeting_str:
			if d in DAY_OFFSETS:
				day_offset = DAY_OFFSETS[d]
				start_slot = day_offset + start_min
				end_slot = day_offset + end_min
				self.add_course_section(course_id, start_slot, end_slot)

	# ------------------------------------------------------------------
	# Convert minute-based schedule to intervals, then find conflicts
	# ------------------------------------------------------------------
	def _gather_intervals(self) -> List[Tuple[str, int, int]]:
		# Scans the minute_schedule to produce a list of (course_id, start_min, end_min).
		# For example, if a course occupies minutes 540..560, we store (course_id, 540, 560).

		intervals: List[Tuple[str, int, int]] = []
		# Collect all distinct course IDs
		all_courses = set()
		for minute_list in self._minute_schedule:
			all_courses.update(minute_list)

		# For each course, walk the 0..1439 range and build intervals
		for cid in all_courses:
			in_block = False
			block_start = 0
			for minute in range(1440):
				if cid in self._minute_schedule[minute]:
					if not in_block:
						# start a block
						in_block = True
						block_start = minute
				else:
					if in_block:
						# close the block
						intervals.append([cid, block_start, minute])
						in_block = False
			# if we end the day still in a block
			if in_block:
				intervals.append((cid, block_start, 1440))

		return intervals

	def find_conflicts(self) -> List[Tuple[str, int, int, str, int, int]]:
		# Identify all overlaps among intervals. Returns a list of tuples:
		# (course_id1, start1, end1, course_id2, start2, end2).

		conflicts = []
		intervals = self._gather_intervals()

		for i in range(len(intervals)):
			cid1, start1, end1 = intervals[i]
			for j in range(i + 1, len(intervals)):
				cid2, start2, end2 = intervals[j]
				if cid1 == cid2:
					continue  # don't compare same course to itself
				# Overlap if each interval starts before the other ends
				if start1 < end2 and start2 < end1:
					add1 = [cid1, start1, end1, cid2, start2, end2]
					if add1 not in conflicts:
						conflicts.append(add1)

		return conflicts