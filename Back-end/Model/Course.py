from enum import Enum

# The Course class takes an input array that contains the attributes (columns) of a given
# extracted row from our CSV.

class Course:
	def __init__(self, attributes: list[str]) -> None:
		
        # Department Code
		self._department_code:      str = (
			attributes[     CourseColumn.DEPARTMENT_CODE.value]
		)
        # Subject Code
		self._subject_code:         str = (
			attributes[     CourseColumn.SUBJECT_CODE.value]
		)
		# Catalog Number
		self._catalog_number:       str = (
			attributes[     CourseColumn.CATALOG_NUMBER.value]
		)
		# Section
		self._section:              str = (
			attributes[     CourseColumn.SECTION.value]
		)
		# Course Title
		self._course_title:         str = (
			attributes[     CourseColumn.COURSE_TITLE.value]
		)
		# Section Type
		self._section_type:         str = (
			attributes[     CourseColumn.SECTION_TYPE.value]
		)
		# Title Topic
		self._title_topic:          str = (
			attributes[     CourseColumn.TITLE_TOPIC.value]
		)
		# Meeting Pattern
		self._meeting_pattern:      str = (
			attributes[     CourseColumn.MEETING_PATTERN.value]
		)
		# Meetings
		self._meetings:             str = (
			attributes[     CourseColumn.MEETINGS.value]
		)
		# Instructor
		self._instructor:           str = (
			attributes[     CourseColumn.INSTRUCTOR.value]
		)
		# Room
		self._room:                 str = (
			attributes[     CourseColumn.ROOM.value]
		)
		# Session
		self._session:              str = (
			attributes[     CourseColumn.SESSION.value]
		)
		# Campus
		self._campus:               str = (
			attributes[     CourseColumn.CAMPUS.value]
		)
		# Inst. Method
		self._inst_method:          str = (
			attributes[     CourseColumn.INST_METHOD.value]
		)
		# Consent
		self._consent:              str = (
			attributes[     CourseColumn.CONSENT.value]
		)
		# Credit Hours Min
		self._credit_hours_min:     int = (
			int(attributes[ CourseColumn.CREDIT_HOURS_MIN.value])
		)
		# Credit Hours
		self._credit_hours:         int = (
			int(attributes[ CourseColumn.CREDIT_HOURS.value])
		)
		# Grade Mode
		self._grade_mode:           str = (
			attributes[     CourseColumn.GRADE_MODE.value]
		)
		# Attributes
		self._attributes:           str = (
			attributes[     CourseColumn.ATTRIBUTES.value]
		)
		# Course Attributes
		self._course_attributes:    str = (
			attributes[     CourseColumn.COURSE_ATTRIBUTES.value]
		)
		# Enrollment
		self._enrollment:           int = (
			int(attributes[ CourseColumn.ENROLLMENT.value])
		)
		# Max Enrollment
		self._max_enrollment:       int = (
			int(attributes[ CourseColumn.MAX_ENROLLMENT.value])
		)
		# Wait Cap
		self._wait_cap:             int = (
			int(attributes[ CourseColumn.WAIT_CAP.value])
		)
		# Rm Cap Request
		self._rm_cap_request:       int = (
			int(attributes[ CourseColumn.RM_CAP_REQUEST.value])
		)
		# Cross-listings
		self._cross_listings:       str = (
			attributes[     CourseColumn.CROSS_LISTINGS.value]
		)
		# Cross-list Max
		self._cross_list_max:       str = (
			attributes[     CourseColumn.CROSS_LIST_MAX.value]
		)
		# Cross-list Wait Cap
		self._cross_list_wait_cap:  int = (
			int(attributes[ CourseColumn.CROSS_LIST_WAIT_CAP.value])
		)
		# Link To
		self._link_to:              str = (
			attributes[     CourseColumn.LINK_TO.value]
		)
		# Comments
		self._comments:             str = (
			attributes[     CourseColumn.COMMENTS.value]
		)
		# Notes 1
		self._notes1:               str = (
			attributes[     CourseColumn.NOTES1.value]
		)
		# Notes 2
		self._notes2:               str = (
			attributes[     CourseColumn.NOTES2.value]
		)


	@property
	def department_code(self) -> str:
		return self._department_code

	@department_code.setter
	def department_code(self, value: str) -> None:
		self._department_code = value

	@property
	def subject_code(self) -> str:
		return self._subject_code

	@subject_code.setter
	def subject_code(self, value: str) -> None:
		self._subject_code = value

	@property
	def catalog_number(self) -> str:
		return self._catalog_number

	@catalog_number.setter
	def catalog_number(self, value: str) -> None:
		self._catalog_number = value

	@property
	def section(self) -> str:
		return self._section

	@section.setter
	def section(self, value: str) -> None:
		self._section = value

	@property
	def course_title(self) -> str:
		return self._course_title

	@course_title.setter
	def course_title(self, value: str) -> None:
		self._course_title = value

	@property
	def section_type(self) -> str:
		return self._section_type

	@section_type.setter
	def section_type(self, value: str) -> None:
		self._section_type = value

	@property
	def title_topic(self) -> str:
		return self._title_topic

	@title_topic.setter
	def title_topic(self, value: str) -> None:
		self._title_topic = value

	@property
	def meeting_pattern(self) -> str:
		return self._meeting_pattern

	@meeting_pattern.setter
	def meeting_pattern(self, value: str) -> None:
		self._meeting_pattern = value

	@property
	def meetings(self) -> str:
		return self._meetings

	@meetings.setter
	def meetings(self, value: str) -> None:
		self._meetings = value

	@property
	def instructor(self) -> str:
		return self._instructor

	@instructor.setter
	def instructor(self, value: str) -> None:
		self._instructor = value

	@property
	def room(self) -> str:
		return self._room

	@room.setter
	def room(self, value: str) -> None:
		self._room = value

	@property
	def session(self) -> str:
		return self._session

	@session.setter
	def session(self, value: str) -> None:
		self._session = value

	@property
	def campus(self) -> str:
		return self._campus

	@campus.setter
	def campus(self, value: str) -> None:
		self._campus = value

	@property
	def inst_method(self) -> str:
		return self._inst_method

	@inst_method.setter
	def inst_method(self, value: str) -> None:
		self._inst_method = value

	@property
	def consent(self) -> str:
		return self._consent

	@consent.setter
	def consent(self, value: str) -> None:
		self._consent = value

	@property
	def credit_hours_min(self) -> int:
		return self._credit_hours_min

	@credit_hours_min.setter
	def credit_hours_min(self, value: int) -> None:
		self._credit_hours_min = value

	@property
	def credit_hours(self) -> int:
		return self._credit_hours

	@credit_hours.setter
	def credit_hours(self, value: int) -> None:
		self._credit_hours = value

	@property
	def grade_mode(self) -> str:
		return self._grade_mode

	@grade_mode.setter
	def grade_mode(self, value: str) -> None:
		self._grade_mode = value

	@property
	def attributes(self) -> str:
		return self._attributes

	@attributes.setter
	def attributes(self, value: str) -> None:
		self._attributes = value

	@property
	def course_attributes(self) -> str:
		return self._course_attributes

	@course_attributes.setter
	def course_attributes(self, value: str) -> None:
		self._course_attributes = value

	@property
	def enrollment(self) -> int:
		return self._enrollment

	@enrollment.setter
	def enrollment(self, value: int) -> None:
		self._enrollment = value

	@property
	def max_enrollment(self) -> int:
		return self._max_enrollment

	@max_enrollment.setter
	def max_enrollment(self, value: int) -> None:
		self._max_enrollment = value

	@property
	def wait_cap(self) -> int:
		return self._wait_cap

	@wait_cap.setter
	def wait_cap(self, value: int) -> None:
		self._wait_cap = value

	@property
	def rm_cap_request(self) -> int:
		return self._rm_cap_request

	@rm_cap_request.setter
	def rm_cap_request(self, value: int) -> None:
		self._rm_cap_request = value

	@property
	def cross_listings(self) -> str:
		return self._cross_listings

	@cross_listings.setter
	def cross_listings(self, value: str) -> None:
		self._cross_listings = value

	@property
	def cross_list_max(self) -> str:
		return self._cross_list_max

	@cross_list_max.setter
	def cross_list_max(self, value: str) -> None:
		self._cross_list_max = value

	@property
	def cross_list_wait_cap(self) -> int:
		return self._cross_list_wait_cap

	@cross_list_wait_cap.setter
	def cross_list_wait_cap(self, value: int) -> None:
		self._cross_list_wait_cap = value

	@property
	def link_to(self) -> str:
		return self._link_to

	@link_to.setter
	def link_to(self, value: str) -> None:
		self._link_to = value

	@property
	def comments(self) -> str:
		return self._comments

	@comments.setter
	def comments(self, value: str) -> None:
		self._comments = value

	@property
	def notes1(self) -> str:
		return self._notes1

	@notes1.setter
	def notes1(self, value: str) -> None:
		self._notes1 = value

	@property
	def notes2(self) -> str:
		return self._notes2

	@notes2.setter
	def notes2(self, value: str) -> None:
		self._notes2 = value


# This Enum gives readability to the instantiation assignment code in the Course class.

class CourseColumn(Enum):
	DEPARTMENT_CODE = 3
	SUBJECT_CODE = 4
	CATALOG_NUMBER = 5
	SECTION = 7
	COURSE_TITLE = 8
	SECTION_TYPE = 9
	TITLE_TOPIC = 10
	MEETING_PATTERN = 11
	MEETINGS = 12
	INSTRUCTOR = 13
	ROOM = 14
	SESSION = 16
	CAMPUS = 17
	INST_METHOD = 18
	CONSENT = 21
	CREDIT_HOURS_MIN = 22
	CREDIT_HOURS = 23
	GRADE_MODE = 24
	ATTRIBUTES = 25
	COURSE_ATTRIBUTES = 26
	ENROLLMENT = 28
	MAX_ENROLLMENT = 29
	WAIT_CAP = 30
	RM_CAP_REQUEST = 33
	CROSS_LISTINGS = 34
	CROSS_LIST_MAX = 35
	CROSS_LIST_WAIT_CAP = 38
	LINK_TO = 39
	COMMENTS = 40
	NOTES1 = 41
	NOTES2 = 42