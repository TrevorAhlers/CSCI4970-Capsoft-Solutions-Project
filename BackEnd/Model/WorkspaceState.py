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
	"""
    A class that represents the state of a user's workspace, including various view and sorting preferences
    for course, classroom, and building views.

    Attributes:
        _workspace_name (str): The name of the workspace (default is 'default').
        _view (str): The current view of the workspace.
        _course_view_style (str): The style of the course view.
        _course_view_sort_by (str): The attribute by which courses are sorted.
        _course_view_sort_direction (str): The direction of sorting for the course view.
        _classroom_view_sort_by (str): The attribute by which classrooms are sorted.
        _classroom_view_sort_direction (str): The direction of sorting for the classroom view.
        _building_view_sort_by (str): The attribute by which buildings are sorted.
        _building_view_sort_direction (str): The direction of sorting for the building view.
        _left_pane (str): The state of the left pane.
        _right_pane (str): The state of the right pane.
        _conflicts (str): The list of conflicts in the workspace.
        _ignores (str): The list of items to ignore in the workspace.
    """
	def __init__(self, attributes: Dict[str, str]) -> None:
		"""
        Initializes the WorkspaceState with the given attributes.

        Args:
            attributes (Dict[str, str]): A dictionary containing key-value pairs for the workspace attributes.
        """

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
		"""
        Gets the sections attribute of the workspace state.

        Returns:
            str: The sections of the workspace.
        """
		return self._sections

	@sections.setter
	def sections(self, value: str) -> None:
		"""
        Sets the sections attribute of the workspace state.

        Args:
            value (str): The new sections value to be set.
        """
		self._sections = value

	@property
	def classrooms(self) -> str:
		"""
        Gets the classrooms attribute of the workspace state.

        Returns:
            str: The classrooms of the workspace.
        """
		return self._classrooms

	@classrooms.setter
	def classrooms(self, value: str) -> None:
		"""
        Sets the classrooms attribute of the workspace state.

        Args:
            value (str): The new classrooms value to be set.
        """
		self._classrooms = value

	@property
	def view(self) -> str:
		"""
        Gets the current view of the workspace.

        Returns:
            str: The current view.
        """
		return self._view

	@view.setter
	def view(self, value: str) -> None:
		"""
        Sets the current view of the workspace.

        Args:
            value (str): The new view to be set.
        """
		self._view = value

	@property
	def course_view_sort_by(self) -> str:
		"""
        Gets the attribute by which courses are sorted.

        Returns:
            str: The course view sort by attribute.
        """
		return self._course_view_sort_by

	@course_view_sort_by.setter
	def course_view_sort_by(self, value: str) -> None:
		"""
        Sets the attribute by which courses are sorted.

        Args:
            value (str): The new sort by value for courses.
        """
		self._course_view_sort_by = value

	@property
	def course_view_sort_direction(self) -> str:
		"""
        Gets the direction by which courses are sorted.

        Returns:
            str: The course view sort direction.
        """
		return self._course_view_sort_direction

	@course_view_sort_direction.setter
	def course_view_sort_direction(self, value: str) -> None:
		"""
        Sets the direction by which courses are sorted.

        Args:
            value (str): The new sort direction for courses.
        """
		self._course_view_sort_direction = value

	@property
	def classroom_view_sort_by(self) -> str:
		"""
        Gets the attribute by which classrooms are sorted.

        Returns:
            str: The classroom view sort by attribute.
        """
		return self._classroom_view_sort_by

	@classroom_view_sort_by.setter
	def classroom_view_sort_by(self, value: str) -> None:
		"""
        Sets the attribute by which classrooms are sorted.

        Args:
            value (str): The new sort by value for classrooms.
        """
		self._classroom_view_sort_by = value

	@property
	def classroom_view_sort_direction(self) -> str:
		"""
        Gets the direction by which classrooms are sorted.

        Returns:
            str: The classroom view sort direction.
        """
		return self._classroom_view_sort_direction

	@classroom_view_sort_direction.setter
	def classroom_view_sort_direction(self, value: str) -> None:
		"""
        Sets the direction by which classrooms are sorted.

        Args:
            value (str): The new sort direction for classrooms.
        """
		self._classroom_view_sort_direction = value

	@property
	def building_view_sort_by(self) -> str:
		"""
        Gets the attribute by which buildings are sorted.

        Returns:
            str: The building view sort by attribute.
        """
		return self._building_view_sort_by

	@building_view_sort_by.setter
	def building_view_sort_by(self, value: str) -> None:
		"""
        Sets the attribute by which buildings are sorted.

        Args:
            value (str): The new sort by value for buildings.
        """
		self._building_view_sort_by = value

	@property
	def building_view_sort_direction(self) -> str:
		"""
        Gets the direction by which buildings are sorted.

        Returns:
            str: The building view sort direction.
        """
		return self._building_view_sort_direction

	@building_view_sort_direction.setter
	def building_view_sort_direction(self, value: str) -> None:
		"""
        Sets the direction by which buildings are sorted.

        Args:
            value (str): The new sort direction for buildings.
        """
		self._building_view_sort_direction = value

	@property
	def sort_by(self) -> str:
		"""
        Gets the current sort by attribute of the workspace state.

        Returns:
            str: The sort by attribute.
        """
		return self._sort_by

	@sort_by.setter
	def sort_by(self, value: str) -> None:
		"""
        Sets the sort by attribute of the workspace state.

        Args:
            value (str): The new sort by value to be set.
        """
		self._sort_by = value

	@property
	def sort_direction(self) -> str:
		"""
        Gets the current sort direction of the workspace state.

        Returns:
            str: The sort direction.
        """
		return self._sort_direction

	@sort_direction.setter
	def sort_direction(self, value: str) -> None:
		"""
        Sets the sort direction attribute of the workspace state.

        Args:
            value (str): The new sort direction to be set.
        """
		self._sort_direction = value

	@property
	def left_pane(self) -> str:
		"""
        Gets the state of the left pane.

        Returns:
            str: The state of the left pane.
        """
		return self._left_pane

	@left_pane.setter
	def left_pane(self, value: str) -> None:
		"""
        Sets the state of the left pane.

        Args:
            value (str): The new state of the left pane.
        """
		self._left_pane = value

	@property
	def right_pane(self) -> str:
		"""
        Gets the state of the right pane.

        Returns:
            str: The state of the right pane.
        """
		return self._right_pane

	@right_pane.setter
	def right_pane(self, value: str) -> None:
		"""
        Sets the state of the right pane.

        Args:
            value (str): The new state of the right pane.
        """
		self._right_pane = value

	@property
	def conflicts(self) -> str:
		"""
        Gets the conflicts list of the workspace state.

        Returns:
            str: The list of conflicts.
        """
		return self._conflicts

	@conflicts.setter
	def conflicts(self, value: str) -> None:
		"""
        Sets the conflicts list of the workspace state.

        Args:
            value (str): The new conflicts list to be set.
        """
		self._conflicts = value

	@property
	def ignores(self) -> str:
		"""
        Gets the ignores list of the workspace state.

        Returns:
            str: The list of ignored items.
        """
		return self._ignores

	@ignores.setter
	def ignores(self, value: str) -> None:
		"""
        Sets the ignores list of the workspace state.

        Args:
            value (str): The new ignores list to be set.
        """
		self._ignores = value
