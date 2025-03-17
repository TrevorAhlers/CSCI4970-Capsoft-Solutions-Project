from enum import Enum
import re
from typing import Dict, List, Tuple
#from Model.CourseSection import CourseSection, CourseSectionEnum
#from Model.Classroom import Classroom, ClassroomEnum

class WorkspaceStateEnum(Enum):
	VIEW                            = 'View'
	COURSE_VIEW_STYLE				= 'Course View Style'
	COURSE_VIEW_SORT_BY             = 'Course View Sort By'
	COURSE_VIEW_SORT_DIRECTION      = 'Course View Sort Direction'
	CLASSROOM_VIEW_SORT_BY          = 'Room View Sort By'
	CLASSROOM_VIEW_SORT_DIRECTION   = 'Room View Sort Direction'
	BUILDING_VIEW_SORT_BY           = 'Building View Sort By'
	BUILDING_VIEW_SORT_DIRECTION    = 'Building View Sort Direction'
	LEFT_PANE                       = 'Left Pane'
	RIGHT_PANE                      = 'Right Pane'
	CONFLICTS                       = 'Conflicts List'
	IGNORES                         = 'Ignore List'

class WorkspaceState:
	def __init__(self, attributes: Dict[str, str]) -> None:

		# Workspace
		# --------------------------------------------------------------------------------------
		self._workspace_name			  = 'default'
		self._view                        = attributes[WorkspaceStateEnum.VIEW.value]

		# Course View (List)
		self._course_view_style			  = attributes[WorkspaceStateEnum.COURSE_VIEW_STYLE.value]
		self._course_view_sort_by         = attributes[WorkspaceStateEnum.COURSE_VIEW_SORT_BY.value]
		self._course_view_sort_direction  = attributes[WorkspaceStateEnum.COURSE_VIEW_SORT_DIRECTION.value]

		# Classroom View (Week Calendar)
		self._classroom_view_sort_by      = attributes[WorkspaceStateEnum.CLASSROOM_VIEW_SORT_BY.value]
		self._classroom_view_sort_direction = attributes[WorkspaceStateEnum.CLASSROOM_VIEW_SORT_DIRECTION.value]

		# Building View (Compact Calendar)
		self._building_view_sort_by       = attributes[WorkspaceStateEnum.BUILDING_VIEW_SORT_BY.value]
		self._building_view_sort_direction = attributes[WorkspaceStateEnum.BUILDING_VIEW_SORT_DIRECTION.value]

		self._left_pane                   = attributes[WorkspaceStateEnum.LEFT_PANE.value]
		self._right_pane                  = attributes[WorkspaceStateEnum.RIGHT_PANE.value]

		# --------------------------------------------------------------------------------------

		self._conflicts                   = attributes[WorkspaceStateEnum.CONFLICTS.value]
		self._ignores                     = attributes[WorkspaceStateEnum.IGNORES.value]

	@property
	def sections(self) -> str:
		return self._sections

	@sections.setter
	def sections(self, value: str) -> None:
		self._sections = value

	@property
	def classrooms(self) -> str:
		return self._classrooms

	@classrooms.setter
	def classrooms(self, value: str) -> None:
		self._classrooms = value

	@property
	def view(self) -> str:
		return self._view

	@view.setter
	def view(self, value: str) -> None:
		self._view = value

	@property
	def course_view_sort_by(self) -> str:
		return self._course_view_sort_by

	@course_view_sort_by.setter
	def course_view_sort_by(self, value: str) -> None:
		self._course_view_sort_by = value

	@property
	def course_view_sort_direction(self) -> str:
		return self._course_view_sort_direction

	@course_view_sort_direction.setter
	def course_view_sort_direction(self, value: str) -> None:
		self._course_view_sort_direction = value

	@property
	def classroom_view_sort_by(self) -> str:
		return self._classroom_view_sort_by

	@classroom_view_sort_by.setter
	def classroom_view_sort_by(self, value: str) -> None:
		self._classroom_view_sort_by = value

	@property
	def classroom_view_sort_direction(self) -> str:
		return self._classroom_view_sort_direction

	@classroom_view_sort_direction.setter
	def classroom_view_sort_direction(self, value: str) -> None:
		self._classroom_view_sort_direction = value

	@property
	def building_view_sort_by(self) -> str:
		return self._building_view_sort_by

	@building_view_sort_by.setter
	def building_view_sort_by(self, value: str) -> None:
		self._building_view_sort_by = value

	@property
	def building_view_sort_direction(self) -> str:
		return self._building_view_sort_direction

	@building_view_sort_direction.setter
	def building_view_sort_direction(self, value: str) -> None:
		self._building_view_sort_direction = value

	@property
	def sort_by(self) -> str:
		return self._sort_by

	@sort_by.setter
	def sort_by(self, value: str) -> None:
		self._sort_by = value

	@property
	def sort_direction(self) -> str:
		return self._sort_direction

	@sort_direction.setter
	def sort_direction(self, value: str) -> None:
		self._sort_direction = value

	@property
	def left_pane(self) -> str:
		return self._left_pane

	@left_pane.setter
	def left_pane(self, value: str) -> None:
		self._left_pane = value

	@property
	def right_pane(self) -> str:
		return self._right_pane

	@right_pane.setter
	def right_pane(self, value: str) -> None:
		self._right_pane = value

	@property
	def conflicts(self) -> str:
		return self._conflicts

	@conflicts.setter
	def conflicts(self, value: str) -> None:
		self._conflicts = value

	@property
	def ignores(self) -> str:
		return self._ignores

	@ignores.setter
	def ignores(self, value: str) -> None:
		self._ignores = value
