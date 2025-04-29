from enum import Enum
import re
import random
from datetime import datetime
from typing import Dict, List, Tuple
from Model.WorkspaceState import WorkspaceState, WorkspaceStateEnum
from Model.CourseSection import CourseSection, CourseSectionEnum
from Model.Classroom import Classroom, ClassroomEnum
from Model.Conflict import Conflict

class AssignmentFileEnum(Enum):
	SECTIONS                        = 'Sections'
	CLASSROOMS                      = 'Classrooms'
	CONFLICTS                       = 'Conflicts'

class AssignmentFile:
	def __init__(self, sections: Dict[str, CourseSection], classrooms: Dict[str, Classroom], conflicts: List[Conflict], filename: str = None) -> None:
		self._sections 			= sections
		self._classrooms 		= classrooms
		self._conflicts 		= conflicts
		self._ignored_conflicts = []
		self._active_conflicts  = []

		for conflict in conflicts:
			if conflict.ignored:
				self._ignored_conflicts.append(conflict)
			else:
				self._active_conflicts.append(conflict)

		if filename:
			self._filename = filename
		else:
			ts = datetime.now().strftime('%Y%m%d%H%M%S%f')
			rand_num = random.randint(0,999)
			self._filename = f"{ts}_{rand_num}"


	@property
	def ignored_conflicts(self) -> List[Conflict]:
		return self._ignored_conflicts

	@ignored_conflicts.setter
	def ignored_conflicts(self, value: List[Conflict]) -> None:
		self._ignored_conflicts = value

	@property
	def active_conflicts(self) -> List[Conflict]:
		return self._active_conflicts

	@active_conflicts.setter
	def active_conflicts(self, value: List[Conflict]) -> None:
		self._active_conflicts = value

	@property
	def sections(self) -> Dict[str,CourseSection]:
		return self._sections

	@sections.setter
	def sections(self, value: Dict[str,CourseSection]) -> None:
		self._sections = value

	@property
	def classrooms(self) -> Dict[str,Classroom]:
		return self._classrooms

	@classrooms.setter
	def classrooms(self, value: Dict[str,Classroom]) -> None:
		self._classrooms = value

	@property
	def conflicts(self) -> List[Conflict]:
		return self._conflicts

	@conflicts.setter
	def conflicts(self, value: List[Conflict]) -> None:
		self._conflicts = value

	@property
	def ignores(self) -> List[Conflict]:
		return self._ignores

	@ignores.setter
	def ignores(self, value: List[Conflict]) -> None:
		self._ignores = value