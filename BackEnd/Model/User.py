from enum import Enum
import re
from typing import Dict, List, Tuple
from Model.WorkspaceState import WorkspaceState, WorkspaceStateEnum
from Model.CourseSection import CourseSection, CourseSectionEnum
from Model.Classroom import Classroom, ClassroomEnum

class UserEnum(Enum):
	WORKSPACE_STATE                 = 'Workspace State'


class User:
	"""
    A class to represent a user with an associated workspace state.

    Attributes:
        _workspace_state (WorkspaceState): The current state of the user's workspace.
    """

	"""
    A class to represent a user with an associated workspace state.

    Attributes:
        _workspace_state (WorkspaceState): The current state of the user's workspace.
    """

	def __init__(self, workspace_state: WorkspaceState) -> None:
		"""
        Initializes a new User instance.

        Args:
            workspace_state (WorkspaceState): A dictionary-like object containing various 
                                              elements of the user's workspace state.
        """
		"""
        Initializes a new User instance.

        Args:
            workspace_state (WorkspaceState): A dictionary-like object containing various 
                                              elements of the user's workspace state.
        """
		self._workspace_state = workspace_state[UserEnum.SECTIONS.value]


	@property
	def _workspace_state(self) -> WorkspaceState:
		"""
        Gets the current workspace state of the user.

        Returns:
            WorkspaceState: The workspace state.
        """
		"""
        Gets the current workspace state of the user.

        Returns:
            WorkspaceState: The workspace state.
        """
		return self._workspace_state

	@_workspace_state.setter
	def sections(self, value: WorkspaceState) -> None:
		"""
        Sets the workspace state for the user.

        Args:
            value (WorkspaceState): The new workspace state.
        """
		"""
        Sets the workspace state for the user.

        Args:
            value (WorkspaceState): The new workspace state.
        """
		self._workspace_state = value