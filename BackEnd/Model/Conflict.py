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
		
	

class Conflict:
	def __init__(self, sections: List[CourseSection], times: List[List]) -> None:
		self._sections                    = sections
		self._section_count               = len(sections)
		self._times                       = times
		self._times_single                = make_time_single(times)
		self._conflict_area_start         = min(make_time_single(times)) if times else 0
		self._conflict_area_end           = max(make_time_single(times)) if times else 0
		self._classroom                   = sections[0].room_number


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
	def classroom(self) -> str:
		return self._classroom

	@classroom.setter
	def classroom(self, value: str) -> None:
		self._classroom = value

	def to_str(self) -> str:
		one = f'-----------------------\nConflict: \nRoom: {self._classroom}\nSection Count: {self._section_count}\n'
		two = 'Sections: '
		for section in self._sections:
			two += f'{section.id}, '
		two = two[:-2]
		three = f'\nConflict from: {self._conflict_area_start} to {self._conflict_area_end}.'
		return one + two + three
