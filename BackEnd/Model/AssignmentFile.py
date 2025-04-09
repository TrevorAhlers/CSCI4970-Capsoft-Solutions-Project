from enum import Enum
import re
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
	def __init__(self, sections: Dict[str, CourseSection], classrooms: Dict[str, Classroom], conflicts: Dict[str, Conflict]) -> None:
		self._sections 		= sections
		self._classrooms 	= classrooms
		self._conflicts 	= conflicts


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