from enum import Enum
import re
from typing import Dict, List, Tuple
from Model.WorkspaceState import WorkspaceState, WorkspaceStateEnum
from Model.CourseSection import CourseSection, CourseSectionEnum
from Model.Classroom import Classroom, ClassroomEnum

def make_time_single(times):
	"""
    Flattens a list of time intervals into a single list of time points.
    
    Args:
        times (List[List[int]]): A list of start and end time pairs.
    
    Returns:
        List[int]: A flattened list containing individual time points.
    """
	"""
    Flattens a list of time intervals into a single list of time points.
    
    Args:
        times (List[List[int]]): A list of start and end time pairs.
    
    Returns:
        List[int]: A flattened list containing individual time points.
    """
	output = []
	for x in times:
		output.append(x[0])
		output.append(x[1])
	return output
		
def generate_conflict_id(sections: List[CourseSection], times: List[List], rooms: List, msg: str) -> str:
	"""
    Generates a unique identifier for a conflict based on section IDs, times, rooms, and an optional message.
    
    Args:
        sections (List[CourseSection]): List of conflicting course sections.
        times (List[List[int]]): List of time intervals causing the conflict.
        rooms (List[str]): List of rooms involved in the conflict.
        msg (str): Additional conflict message.
    
    Returns:
        str: A unique string representing the conflict.
    """
	"""
    Generates a unique identifier for a conflict based on section IDs, times, rooms, and an optional message.
    
    Args:
        sections (List[CourseSection]): List of conflicting course sections.
        times (List[List[int]]): List of time intervals causing the conflict.
        rooms (List[str]): List of rooms involved in the conflict.
        msg (str): Additional conflict message.
    
    Returns:
        str: A unique string representing the conflict.
    """
	section_ids = [sec.id for sec in sections]

	time_parts = [f"{t[0]}-{t[1]}" for t in times]

	room_parts = [str(r) for r in rooms]

	parts = section_ids + time_parts + room_parts
	if msg:
		parts.append(msg)

	return "_".join(parts)

class Conflict:
	"""
    Represents a scheduling conflict between multiple course sections in classrooms.
    """
	"""
    Represents a scheduling conflict between multiple course sections in classrooms.
    """
	def __init__(self, sections: List[CourseSection], times: List[List], rooms: List, msg: str = "") -> None:
		"""
        Initializes a Conflict instance.
        
        Args:
            sections (List[CourseSection]): List of conflicting course sections.
            times (List[List[int]]): List of time intervals causing the conflict.
            rooms (List[str]): List of rooms where the conflict occurs.
            msg (str, optional): Additional conflict message. Defaults to "".
        """
		"""
        Initializes a Conflict instance.
        
        Args:
            sections (List[CourseSection]): List of conflicting course sections.
            times (List[List[int]]): List of time intervals causing the conflict.
            rooms (List[str]): List of rooms where the conflict occurs.
            msg (str, optional): Additional conflict message. Defaults to "".
        """
		self._id 						  = generate_conflict_id(sections, times, rooms, msg)
		self._sections                    = sections
		self._section_count               = len(sections)
		self._times                       = times
		self._times_single                = make_time_single(times)
		self._conflict_area_start         = min(make_time_single(times)) if times else 0
		self._conflict_area_end           = max(make_time_single(times)) if times else 0
		self._classrooms                   = rooms
		self._conflict_message			  = msg

	@property
	def section_count(self) -> int:
		"""Gets the number of conflicting sections."""
		"""Gets the number of conflicting sections."""
		return self._section_count

	@section_count.setter
	def section_count(self, value: int) -> None:
		"""
		Sets the number of conflicting sections.
		
		Args:
			value (int): The number of sections involved in the conflict.
		"""
		"""
		Sets the number of conflicting sections.
		
		Args:
			value (int): The number of sections involved in the conflict.
		"""
		self._section_count = value

	@property
	def conflict_message(self) -> str:
		"""Gets the conflict message."""
		"""Gets the conflict message."""
		return self._conflict_message

	@conflict_message.setter
	def conflict_message(self, value: str) -> None:
		"""
		Sets the conflict message.
		
		Args:
			value (str): A descriptive message about the conflict.
		"""
		"""
		Sets the conflict message.
		
		Args:
			value (str): A descriptive message about the conflict.
		"""
		self._conflict_message = value

	@property
	def id(self) -> str:
		"""Gets the unique conflict identifier."""
		"""Gets the unique conflict identifier."""
		return self._id

	@id.setter
	def id(self, value: str) -> None:
		"""
		Sets the unique conflict identifier.
		
		Args:
			value (str): The new conflict identifier.
		"""
		"""
		Sets the unique conflict identifier.
		
		Args:
			value (str): The new conflict identifier.
		"""
		self._id = value

	@property
	def sections(self) -> List[CourseSection]:
		"""Gets the list of conflicting course sections."""
		"""Gets the list of conflicting course sections."""
		return self._sections

	@sections.setter
	def sections(self, value: List[CourseSection]) -> None:
		"""
		Sets the list of conflicting course sections.
		
		Args:
			value (List[CourseSection]): A new list of conflicting sections.
		"""
		"""
		Sets the list of conflicting course sections.
		
		Args:
			value (List[CourseSection]): A new list of conflicting sections.
		"""
		self._sections = value

	@property
	def section_count(self) -> int:


		return self._section_count

	@property
	def times(self) -> List[List]:
		"""Gets the list of conflicting time intervals."""
		"""Gets the list of conflicting time intervals."""
		return self._times

	@times.setter
	def times(self, value: List[List]) -> None:
		"""
		Sets the list of conflicting time intervals.
		
		Args:
			value (List[List]): A new list of time intervals.
		"""
		"""
		Sets the list of conflicting time intervals.
		
		Args:
			value (List[List]): A new list of time intervals.
		"""
		self._times = value

	@property
	def conflict_area_start(self) -> int:
		"""Gets the start time of the conflict."""
		"""Gets the start time of the conflict."""
		return self._conflict_area_start

	@conflict_area_start.setter
	def conflict_area_start(self, value: int) -> None:
		"""
		Sets the start time of the conflict.
		
		Args:
			value (int): The start time of the conflict in minutes from midnight.
		"""
		"""
		Sets the start time of the conflict.
		
		Args:
			value (int): The start time of the conflict in minutes from midnight.
		"""
		self._conflict_area_start = value

	@property
	def conflict_area_end(self) -> int:
		"""Gets the end time of the conflict."""
		"""Gets the end time of the conflict."""
		return self._conflict_area_end

	@conflict_area_end.setter
	def conflict_area_end(self, value: int) -> None:
		"""
		Sets the end time of the conflict.
		
		Args:
			value (int): The end time of the conflict in minutes from midnight.
		"""
		"""
		Sets the end time of the conflict.
		
		Args:
			value (int): The end time of the conflict in minutes from midnight.
		"""
		self._conflict_area_end = value

	@property
	def classrooms(self) -> List:
		"""Gets the list of conflicting classrooms."""
		"""Gets the list of conflicting classrooms."""
		return self._classrooms

	@classrooms.setter
	def classrooms(self, value: List) -> None:
		"""
		Sets the list of conflicting classrooms.
		
		Args:
			value (List): A new list of conflicting classrooms.
		"""
		"""
		Sets the list of conflicting classrooms.
		
		Args:
			value (List): A new list of conflicting classrooms.
		"""
		self._classrooms = value

	def to_str(self) -> str:
		"""
        Returns a formatted string representation of the conflict.
        
        Returns:
            str: A formatted string describing the conflict details.
        """
		"""
        Returns a formatted string representation of the conflict.
        
        Returns:
            str: A formatted string describing the conflict details.
        """
		out_str = ""

		one = f'-----------------------\nConflict: \nRoom: {self._classrooms}\nSection Count: {self._section_count}\n'
		out_str += one

		two = 'Sections: '
		for section in self._sections:
			two += f'{section.id}, '
		two = two[:-2]
		if self._sections:
			out_str += two

		three = f'\nConflict from: {self._conflict_area_start} to {self._conflict_area_end}'
		if self._conflict_area_start > 0 or self._conflict_area_end > 0:
			out_str += three

		if self._conflict_message:
			four = "\n" + f'Message: {self._conflict_message}'
			out_str += four
		
		return out_str