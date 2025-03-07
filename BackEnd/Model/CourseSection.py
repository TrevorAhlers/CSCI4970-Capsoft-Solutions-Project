#....................................................................................
# CourseSection Datamodel:
#____________________________________________________________________________________
#
# Enum codes, like DEPARTMENT_CODE, should be uppercase version of class object
# variables like department_code. Logic in the data formatter relies on this
# convention in the row_to_string() function.
#
# TODO: Make methods to clean data
#
#....................................................................................

from enum import Enum
from typing import Dict, Optional

class CourseSectionEnum(Enum):
    DEPARTMENT_CODE    = 'Department Code'
    SUBJECT_CODE       = 'Subject Code'
    CATALOG_NUMBER     = 'Catalog Number'
    SECTION            = 'Section #'
    COURSE_TITLE       = 'Course Title'
    SECTION_TYPE       = 'Section Type'
    TITLE_TOPIC        = 'Title/Topic'
    MEETING_PATTERN    = 'Meeting Pattern'
    MEETINGS           = 'Meetings'
    INSTRUCTOR         = 'Instructor'
    ROOM               = 'Room'
    SESSION            = 'Session'
    CAMPUS             = 'Campus'
    INST_METHOD        = 'Inst. Method'
    CONSENT            = 'Consent'
    CREDIT_HOURS_MIN   = 'Credit Hrs Min'
    CREDIT_HOURS       = 'Credit Hrs'
    GRADE_MODE         = 'Grade Mode'
    ATTRIBUTES         = 'Attributes'
    COURSE_ATTRIBUTES  = 'Course Attributes'
    ENROLLMENT         = 'Enrollment'
    MAX_ENROLLMENT     = 'Maximum Enrollment'
    WAIT_CAP           = 'Wait Cap'
    RM_CAP_REQUEST     = 'Rm Cap Request'
    CROSS_LISTINGS     = 'Cross-listings'
    CROSS_LIST_MAX     = 'Cross-list Maximum'
    CROSS_LIST_WAIT_CAP= 'Cross-list Wait Cap'
    LINK_TO            = 'Link To'
    COMMENTS           = 'Comments'
    NOTES1             = 'Notes#1'
    NOTES2             = 'Notes#2'

    def lower(self):
        return self.lower


class CourseSection:
    def __init__(self, attributes: Dict[str, str]) -> None:
        # Look up each attribute using the enum's value (i.e. header text)
        self._department_code   = attributes[		CourseSectionEnum.DEPARTMENT_CODE.value]
        self._subject_code      = attributes[		CourseSectionEnum.SUBJECT_CODE.value]
        self._catalog_number    = attributes[		CourseSectionEnum.CATALOG_NUMBER.value]
        self._section           = attributes[		CourseSectionEnum.SECTION.value]
        self._course_title      = attributes[		CourseSectionEnum.COURSE_TITLE.value]
        self._section_type      = attributes[		CourseSectionEnum.SECTION_TYPE.value]
        self._title_topic       = attributes[		CourseSectionEnum.TITLE_TOPIC.value]
        self._meeting_pattern   = attributes[		CourseSectionEnum.MEETING_PATTERN.value]
        self._meetings          = attributes[		CourseSectionEnum.MEETINGS.value]
        self._instructor        = attributes[		CourseSectionEnum.INSTRUCTOR.value]
        self._room              = attributes[		CourseSectionEnum.ROOM.value]
        self._session           = attributes[		CourseSectionEnum.SESSION.value]
        self._campus            = attributes[		CourseSectionEnum.CAMPUS.value]
        self._inst_method       = attributes[		CourseSectionEnum.INST_METHOD.value]
        self._consent           = attributes[		CourseSectionEnum.CONSENT.value]
        self._credit_hours_min  = attributes[	    CourseSectionEnum.CREDIT_HOURS_MIN.value]
        self._credit_hours      = attributes[   	CourseSectionEnum.CREDIT_HOURS.value]
        self._grade_mode        = attributes[		CourseSectionEnum.GRADE_MODE.value]
        self._attributes        = attributes[		CourseSectionEnum.ATTRIBUTES.value]
        self._course_attributes = attributes[		CourseSectionEnum.COURSE_ATTRIBUTES.value]
        self._enrollment        = attributes[	    CourseSectionEnum.ENROLLMENT.value]
        self._max_enrollment    = attributes[	    CourseSectionEnum.MAX_ENROLLMENT.value]
        self._wait_cap          = attributes[	    CourseSectionEnum.WAIT_CAP.value]
        self._rm_cap_request    = attributes[	    CourseSectionEnum.RM_CAP_REQUEST.value]
        self._cross_listings    = attributes[		CourseSectionEnum.CROSS_LISTINGS.value]
        self._cross_list_max    = attributes[		CourseSectionEnum.CROSS_LIST_MAX.value]
        self._cross_list_wait_cap = attributes[	    CourseSectionEnum.CROSS_LIST_WAIT_CAP.value]
        self._link_to           = attributes[		CourseSectionEnum.LINK_TO.value]
        self._comments          = attributes[		CourseSectionEnum.COMMENTS.value]
        self._notes1            = attributes[		CourseSectionEnum.NOTES1.value]
        self._notes2            = attributes[		CourseSectionEnum.NOTES2.value]

        self._room_number = self._room.split()[-1]

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
    def room_number(self) -> str:
        return self._room_number

    @room_number.setter
    def room_number(self, value: str) -> None:
        self._room_number = value

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
