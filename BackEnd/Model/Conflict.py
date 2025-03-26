from enum import Enum
import re
from typing import Dict, List, Tuple
from Model.WorkspaceState import WorkspaceState, WorkspaceStateEnum
from Model.CourseSection import CourseSection, CourseSectionEnum
from Model.Classroom import Classroom, ClassroomEnum

def make_time_single(times):
	output = []
	for x in times:
		output.append(x[0])
		output.append(x[1])
	return output
		
def generate_conflict_id(sections: List[CourseSection], times: List[List], rooms: List, msg: str) -> str:
	section_ids = [sec.id for sec in sections]

	time_parts = [f"{t[0]}-{t[1]}" for t in times]

	room_parts = [str(r) for r in rooms]

	parts = section_ids + time_parts + room_parts
	if msg:
		parts.append(msg)

	return "_".join(parts)

class Conflict:
	def __init__(self, sections: List[CourseSection], times: List[List], rooms: List, msg: str = "") -> None:
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
		return self._section_count

	@section_count.setter
	def section_count(self, value: int) -> None:
		self._section_count = value

	@property
	def conflict_message(self) -> str:
		return self._conflict_message

	@conflict_message.setter
	def conflict_message(self, value: str) -> None:
		self._conflict_message = value

	@property
	def id(self) -> str:
		return self._id

	@id.setter
	def id(self, value: str) -> None:
		self._id = value

	@property
	def sections(self) -> List[CourseSection]:
		return self._sections

	@sections.setter
	def sections(self, value: List[CourseSection]) -> None:
		self._sections = value

	@property
	def section_count(self) -> int:
		return self._section_count

	@property
	def times(self) -> List[List]:
		return self._times

	@times.setter
	def times(self, value: List[List]) -> None:
		self._times = value

	@property
	def conflict_area_start(self) -> int:
		return self._conflict_area_start

	@conflict_area_start.setter
	def conflict_area_start(self, value: int) -> None:
		self._conflict_area_start = value

	@property
	def conflict_area_end(self) -> int:
		return self._conflict_area_end

	@conflict_area_end.setter
	def conflict_area_end(self, value: int) -> None:
		self._conflict_area_end = value

	@property
	def classrooms(self) -> List:
		return self._classrooms

	@classrooms.setter
	def classrooms(self, value: List) -> None:
		self._classrooms = value

	def to_str(self) -> str:
		one = f'-----------------------\nConflict: \nRoom: {self._classrooms}\nSection Count: {self._section_count}\n'
		two = 'Sections: '
		for section in self._sections:
			two += f'{section.id}, '
		two = two[:-2]
		three = f'\nConflict from: {self._conflict_area_start} to {self._conflict_area_end}'
		if self._conflict_message:
			four = "\n" + f'Message: {self._conflict_message}'
			return one + two + three + four
		return one + two + three