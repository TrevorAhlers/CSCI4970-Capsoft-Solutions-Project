import pytest
from typing import List, Tuple

import sys
import os

# Add the 'BackEnd' directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Model.CourseSection import CourseSection, CourseSectionEnum
from Model.Classroom import Classroom, ClassroomEnum, parse_time, parse_meeting_line, make_int_str



@pytest.fixture
def sample_classroom():
    # Create a sample classroom with some attributes
    attributes = {
        ClassroomEnum.ROOM.value: "Peter Kiewit Institute 172",
        ClassroomEnum.SEATS.value: "30",
        ClassroomEnum.DISPLAYS.value: "2",
        ClassroomEnum.COMPUTER_COUNT.value: "10",
        ClassroomEnum.INFO_AND_CONNECTIVITY.value: "WiFi"
    }
    
    # Initialize the Classroom with the attributes dictionary
    return Classroom(attributes)

@pytest.fixture
def sample_course_section():
    # Create a sample course section with attributes
    attributes = {
        CourseSectionEnum.DEPARTMENT_CODE.value: 'UNO-AE',
        CourseSectionEnum.SUBJECT_CODE.value: 'CSCI',
        CourseSectionEnum.CATALOG_NUMBER.value: '4970',
        CourseSectionEnum.SECTION.value: '001',
        CourseSectionEnum.COURSE_TITLE.value: 'Capstone',
        CourseSectionEnum.SECTION_TYPE.value: 'Lecture',
        CourseSectionEnum.TITLE_TOPIC.value: 'None',
        CourseSectionEnum.MEETING_PATTERN.value: 'MW 3pm-4:15pm',
        CourseSectionEnum.INSTRUCTOR.value: 'Siy, Harvey (24904115) [Primary Instructor, Post, Print]',
        CourseSectionEnum.ROOM.value: 'Peter Kiewit Institute 248',
        CourseSectionEnum.SESSION.value: 'Regular Academic Session',
        CourseSectionEnum.CAMPUS.value: 'UNO Engineering',
        CourseSectionEnum.INST_METHOD.value: 'In Person',
        CourseSectionEnum.CONSENT.value: 'No Special Consent Required',
        CourseSectionEnum.CREDIT_HOURS_MIN.value: '3',
        CourseSectionEnum.CREDIT_HOURS.value: '3',
        CourseSectionEnum.GRADE_MODE.value: 'Graded',
        CourseSectionEnum.ATTRIBUTES.value: '',
        CourseSectionEnum.COURSE_ATTRIBUTES.value: '',
        CourseSectionEnum.ENROLLMENT.value: '42',
        CourseSectionEnum.MAX_ENROLLMENT.value: '40',
        CourseSectionEnum.WAIT_CAP.value: '99',
        CourseSectionEnum.RM_CAP_REQUEST.value: '40',
        CourseSectionEnum.CROSS_LISTINGS.value: '',
        CourseSectionEnum.CROSS_LIST_MAX.value: '',
        CourseSectionEnum.CROSS_LIST_WAIT_CAP.value: '',
        CourseSectionEnum.LINK_TO.value: '',
        CourseSectionEnum.COMMENTS.value: 'DONE, AMJ - PKI 248',
        CourseSectionEnum.NOTES1.value: 'PKI 248',
        CourseSectionEnum.NOTES2.value: ''
    }
    return CourseSection(attributes)


# Test for Classroom initialization
def test_classroom_initialization(sample_classroom):
    # Assert that the Classroom instance was initialized correctly

    cls_room = sample_classroom
    assert cls_room.room == "Peter Kiewit Institute 172"
    assert cls_room.seats == "30"
    assert cls_room.displays == "2"
    assert cls_room.computer_count == "10"
    assert cls_room.info_and_connectivity == "WiFi"
    
    # Assert that the sections list is empty at the beginning
    assert cls_room.sections == []
    
    # Assert that the minute schedule is correctly initialized (it should be a list of empty lists)
    assert len(cls_room._minute_schedule) == 7 * 1440  # 7 days * 1440 minutes
    assert all(isinstance(item, list) for item in cls_room._minute_schedule)
    
    # Assert that the assigned room status is correct (assuming this is initialized as [True] or similar in the constructor)
    assert cls_room._assigned == [True]  # or adjust based on your constructor logic


def test_parse_time():
    # Test valid time parsing
    assert parse_time('9am') == 540  # 9am is 540 minutes from midnight
    assert parse_time('10:30pm') == 1350  # 10:30pm is 1350 minutes from midnight
    assert parse_time('12pm') == 720  # 12pm is 720 minutes from midnight
    assert parse_time('3:15pm') == 915  # 3:15pm is 915 minutes from midnight

def test_parse_meeting_line():
    # Test meeting line parsing
    line = 'MW 3pm-4:15pm; F 8:30am-10:20am'
    result = parse_meeting_line(line)

    assert len(result) == 3
    assert result == [('M', 900, 975), ('W', 900, 975), ('F', 510, 620)]

def test_make_int_str():
    # Case 1: string that ends with '.0'
    assert make_int_str("123.0") == "123"
    
    # Case 2: string that doesn't end with '.0'
    assert make_int_str("123") == "123"
    
    # Case 3: empty string (no change expected)
    assert make_int_str("") == ""
    
    # Case 4: string that doesn't have '.0' at the end, but has other numbers
    assert make_int_str("100.1") == "100.1"
    
    # Case 5: string that has '.0' in the middle (no change expected)
    assert make_int_str("123.456.0") == "123.456"
    
    # Case 6: a string with '.0' at the end but with leading spaces
    assert make_int_str(" 123.0") == " 123"  # Leading space should be preserved


def test_add_course_section(sample_classroom):
    # Add a course section to the classroom
    course_id = 'CSCI 4070'
    room = 'Peter Kiewit Institute 172'
    start_slot = 600  # 10:00 AM
    end_slot = 660    # 11:00 AM
    
    # Before adding the course, check that the minute schedule is empty for these slots
    for minute in range(start_slot, end_slot):
        assert len(sample_classroom._minute_schedule[minute]) == 0

    # Add the course section
    sample_classroom.add_course_section(course_id, room, start_slot, end_slot)

    # Check that the course ID has been added to the minute schedule between 600 (10:00 AM) and 660 (11:00 AM)
    for minute in range(start_slot, end_slot):
        assert course_id in sample_classroom._minute_schedule[minute]

    # Also check that no other course IDs were added to those minutes (if the room is correct)
    # Assuming there's no conflict with other courses in this test.
    for minute in range(start_slot, end_slot):
        assert len(sample_classroom._minute_schedule[minute]) == 1  # Only 'CSCI 4070' should be present


def test_remove_course_section(sample_classroom):
    # Add a course section to the classroom
    course_id = 'CSCI 4070'
    room = 'Peter Kiewit Institute 172'
    start_slot = 600  # 10:00 AM
    end_slot = 660    # 11:00 AM

    # Add the course section
    sample_classroom.add_course_section(course_id, room, start_slot, end_slot)

    # Check that the course was added to the schedule before removal
    for minute in range(start_slot, end_slot):
        assert course_id in sample_classroom._minute_schedule[minute]

    # Now remove the course section
    sample_classroom.remove_course_section(course_id)

    # Check that the course has been removed from the schedule
    for minute in range(start_slot, end_slot):
        assert course_id not in sample_classroom._minute_schedule[minute]



def test_find_conflicts(sample_classroom):
    # Set up a 7-day minute schedule (7 * 1440 minutes)
    sample_classroom._minute_schedule = [[] for _ in range(7 * 1440)]

    # Define course intervals (Monday assumed as Day 0)
    schedules = {
        'CSCI 4050': (540, 600),   # 9:00 - 10:00
        'CSCI 4220': (590, 650),   # 9:50 - 10:50 — overlaps with 4050
        'CSCI 3970': (620, 680),   # 10:20 - 11:20 — overlaps with 4220
        'CSCI 3250': (660, 720),   # 11:00 - 12:00 — overlaps with 3970
        'CSCI 2690': (700, 760),   # 11:40 - 12:40 — overlaps with 3250
    }

    # Fill in the minute schedule
    for course, (start, end) in schedules.items():
        for minute in range(start, end):
            sample_classroom._minute_schedule[minute].append(course)

    # Run the conflict finder
    conflicts = sample_classroom.find_conflicts()

    # Define expected conflicts (sorted tuple of each pair, matching canonical form)
    expected_conflicts = [
        ('CSCI 4050', 540, 600, 'CSCI 4220', 590, 650),
        ('CSCI 4220', 590, 650, 'CSCI 3970', 620, 680),
        ('CSCI 3970', 620, 680, 'CSCI 3250', 660, 720),
        ('CSCI 3250', 660, 720, 'CSCI 2690', 700, 760),
    ]

    # Sort the tuples inside each conflict to match the canonical form
    def canonical(conflict):
        return tuple(sorted([
            (conflict[0], conflict[1], conflict[2]),
            (conflict[3], conflict[4], conflict[5])
        ]))

    actual_set = set(canonical(c) for c in conflicts)
    expected_set = set(canonical(c) for c in expected_conflicts)

    assert actual_set == expected_set
