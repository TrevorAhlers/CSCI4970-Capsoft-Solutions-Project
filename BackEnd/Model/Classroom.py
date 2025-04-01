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

	"""
    Converts a time string like '9am' or '10:30pm' into the number of minutes 
    from midnight (0..1439).
    
    Args:
        timestr (str): Time string in the format 'H:MMam/pm' or 'Ham/pm'.
    
    Returns:
        int: The equivalent time in minutes since midnight.
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
#####################################################################################
# 	Given "MW 3pm-4:15pm; F 8:30am-10:20am", return a list of (day, start_min, end_min).
#	For example: [('M', 900, 975), ('W', 900, 975), ('F', 510, 620)].
#....................................................................................
def parse_meeting_line(line: str) -> List[Tuple[str, int, int]]:

	"""
    Parses a string of course meeting times and returns a list of (day, start, end) 
    tuples with the corresponding start and end times in minutes.

    Args:
        line (str): A string representing meeting days and times (e.g. 'MW 3pm-4:15pm; F 8:30am-10:20am').

    Returns:
        List[Tuple[str, int, int]]: A list of tuples representing each meeting's day and time in minutes.
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

def make_int_str(attribute: str) -> str:

	"""
    Converts a string attribute to an integer string if it ends with '.0'.
    
    Args:
        attribute (str): The attribute to check and convert.
    
    Returns:
        str: The integer string if the attribute ends with '.0', otherwise returns the original string.
    """

	if attribute.endswith(".0"):
		attribute = attribute[:-2]
		return attribute
	return attribute

class ClassroomEnum(Enum):

	"""
    Enum class for classroom attributes used for data mapping.
    """

	ROOM             		= 'Room Number'
	SEATS                   = 'Seats'
	DISPLAYS                = 'Displays'
	COMPUTER_COUNT          = 'Computer Count'
	INFO_AND_CONNECTIVITY   = 'Information and Connectivity'
	#DEPARTMENT              = 'Department'

class Classroom:

	"""
    A class representing a classroom with its attributes and schedule. It supports adding courses
    and finding scheduling conflicts based on its weekly availability.
    """

	def __init__(self, attributes: Dict[str, str]) -> None:

		"""
        Initializes a Classroom object with the given attributes.
        
        Args:
            attributes (Dict[str, str]): A dictionary containing classroom attributes.
        """

		self._room		             = attributes[ClassroomEnum.ROOM.value]
		self._seats                  = make_int_str(attributes[ClassroomEnum.SEATS.value])
		self._displays               = attributes[ClassroomEnum.DISPLAYS.value]
		self._computer_count         = attributes[ClassroomEnum.COMPUTER_COUNT.value]
		self._info_and_connectivity  = attributes[ClassroomEnum.INFO_AND_CONNECTIVITY.value]
		self._sections				 = []
		self._assigned				 = [True if self._room else False]
		# self._department             = attributes[ClassroomEnum.DEPARTMENT.value]

		# A 1440 * possible_days = total items
		self._minute_schedule: List[List[str]] = [[] for _ in range(7 * 1440)]

	@property
	def sections(self) -> List:

		"""
        Gets the list of course sections assigned to this classroom.
        
        Returns:
            List: The list of course sections assigned to the classroom.
        """

		return self._sections
	
	def add_section(self, value: CourseSection) -> None:
		"""
        Adds a course section to the classroom.
        
        Args:
            value (CourseSection): The course section to add.
        """
		self._sections.append(value)

	@sections.setter
	def sections(self, value: List) -> None:
		"""
        Sets the list of course sections for the classroom.
        
        Args:
            value (List): The list of course sections.
        """
		self._sections = value

	@property
	def room(self) -> str:
		"""
        Gets the classroom room number.
        
        Returns:
            str: The classroom room number.
        """
		return self._room

	@room.setter
	def room(self, value: str) -> None:
		"""
        Sets the classroom room number.
        
        Args:
            value (str): The room number to set.
        """
		self._room = value

	@property
	def seats(self) -> str:
		"""
        Gets the number of seats in the classroom.
        
        Returns:
            str: The number of seats in the classroom.
        """
		return self._seats

	@seats.setter
	def seats(self, value: str) -> None:
		"""
        Sets the number of seats in the classroom.
        
        Args:
            value (str): The number of seats to set.
        """
		self._seats = value

	@property
	def displays(self) -> str:
		"""
        Gets the number of displays in the classroom.
        
        Returns:
            str: The number of displays in the classroom.
        """
		return self._displays

	@displays.setter
	def displays(self, value: str) -> None:
		"""
        Sets the number of displays in the classroom.
        
        Args:
            value (str): The number of displays to set.
        """
		self._displays = value

	@property
	def computer_count(self) -> str:
		"""
        Gets the number of computers in the classroom.
        
        Returns:
            str: The number of computers in the classroom.
        """
		return self._computer_count

	@computer_count.setter
	def computer_count(self, value: str) -> None:
		"""
        Sets the number of computers in the classroom.
        
        Args:
            value (str): The number of computers to set.
        """
		self._computer_count = value

	@property
	def info_and_connectivity(self) -> str:
		"""
        Gets the information and connectivity details for the classroom.
        
        Returns:
            str: The information and connectivity details.
        """
		return self._info_and_connectivity

	@info_and_connectivity.setter
	def info_and_connectivity(self, value: str) -> None:
		"""
        Sets the information and connectivity details for the classroom.
        
        Args:
            value (str): The information and connectivity details to set.
        """
		self._info_and_connectivity = value

#....................................................................................
#####################################################################################
# 	# Occupies minutes [start_slot, end_slot) in the _minute_schedule.
#....................................................................................
	def add_course_section(self, course_id: str, room: str, start_slot: int, end_slot: int) -> None:
		"""
        Adds a course section to the classroom's minute schedule.
        
        Args:
            course_id (str): The unique identifier for the course.
            room (str): The room where the course will be held.
            start_slot (int): The starting minute of the course.
            end_slot (int): The ending minute of the course.
        """
		for minute in range(start_slot, end_slot):
			if room != ['TBD']:
				self._minute_schedule[minute].append(course_id)

#....................................................................................
#####################################################################################
# 	Removes course_id from all minutes in the schedule.
#....................................................................................
	def remove_course_section(self, course_id: str) -> None:
		"""
        Removes a course section from the classroom's schedule.
        
        Args:
            course_id (str): The unique identifier for the course to remove.
        """
		for minute_list in self._minute_schedule:
			while course_id in minute_list:
				minute_list.remove(course_id)

#....................................................................................
#####################################################################################
# 	Parses course_section_object.meetings (assuming it's something like
#	'MW 3pm-4:15pm; F 8:30am-10:20am') and adds it to this room's schedule.
#....................................................................................
	def add_course_section_object(self, course_section_object: CourseSection) -> None:

		"""
        Parses the course section object and adds it to the classroom's schedule.
        
        Args:
            course_section_object (CourseSection): The course section object to add.
        """
		
		schedule = course_section_object.schedule
		self.add_section(course_section_object)
		for section_id, room, d, start_min, end_min in schedule:
			if d in DAY_OFFSETS:
				day_offset = DAY_OFFSETS[d]
				start_slot = day_offset + start_min
				end_slot = day_offset + end_min
				self.add_course_section(section_id, room, start_slot, end_slot)

#....................................................................................
#####################################################################################
# Convert minute-based schedule to intervals
#....................................................................................
	def gather_intervals(self) -> List[Tuple[str, int, int]]:
		# Scans the minute_schedule to produce a list of (course_id, start_min, end_min).
		# For example, if a course occupies minutes 540..560, we store (course_id, 540, 560).

		"""
        Gathers all course schedule intervals from the classroom's minute schedule.
        
        Returns:
            List[Tuple[str, int, int]]: A list of tuples containing course ID and the time intervals.
        """

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

#....................................................................................
#####################################################################################
# Return interval overlaps as conflicts
#....................................................................................
	def find_conflicts(self) -> List[Tuple[str, int, int, str, int, int]]:
		"""
        Finds conflicts between courses by checking overlapping time intervals.
        
        Returns:
            List[Tuple[str, int, int, str, int, int]]: A list of conflicts, where each conflict
            contains two overlapping course intervals.
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