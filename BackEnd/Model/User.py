from enum import Enum
import re
from typing import Dict, List, Tuple
from Model.WorkspaceState import WorkspaceState, WorkspaceStateEnum
from Model.CourseSection import CourseSection, CourseSectionEnum
from Model.Classroom import Classroom, ClassroomEnum

class UserEnum(Enum):
	USER_ID                        = 'User ID'
	USER_PASSWORD                  = 'User Password'
	WORKSPACE_STATE                = 'Workspace State'

class User:
	def __init__(self, user_id: str, user_password: str, workspace_state: WorkspaceState) -> None:
		self.user_id = user_id
		self.user_password = user_password
		self.workspace_state = workspace_state

	@property
	def user_id(self) -> str:
		return self._user_id

	@user_id.setter
	def user_id(self, value: str) -> None:
		self._user_id = value

	@property
	def user_password(self) -> str:
		return self._user_password

	@user_password.setter
	def user_password(self, value: str) -> None:
		self._user_password = value

	@property
	def workspace_state(self) -> WorkspaceState:
		return self._workspace_state

	@workspace_state.setter
	def workspace_state(self, value: WorkspaceState) -> None:
		self._workspace_state = value
