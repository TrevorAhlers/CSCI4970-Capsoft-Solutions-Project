from enum import Enum
import re
from typing import Dict, List, Tuple
from Model.WorkspaceState import WorkspaceState, WorkspaceStateEnum
from Model.CourseSection import CourseSection, CourseSectionEnum
from Model.Classroom import Classroom, ClassroomEnum

class UserEnum(Enum):
	WORKSPACE_STATE                 = 'Workspace State'


class User:
	def __init__(self, workspace_state: WorkspaceState) -> None:
		self._workspace_state = workspace_state[UserEnum.SECTIONS.value]


	@property
	def _workspace_state(self) -> WorkspaceState:
		return self._workspace_state

	@_workspace_state.setter
	def sections(self, value: WorkspaceState) -> None:
		self._workspace_state = value