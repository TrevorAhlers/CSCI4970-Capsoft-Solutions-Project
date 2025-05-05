import pytest

import sys
import os

# Add the 'BackEnd' directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Model.CourseSection import CourseSection, CourseSectionEnum
from Model.CourseSection import parse_rooms, parse_meetings, parse_time, extract_room_numbers, time_to_str, combine_section_info, parse_crosslistings



@pytest.fixture
def valid_course_data():
    """Fixture for valid course data."""
    return {
        CourseSectionEnum.DEPARTMENT_CODE.value: 'UNO-AE',
        CourseSectionEnum.SUBJECT_CODE.value: 'AREN',
        CourseSectionEnum.CATALOG_NUMBER.value: '1030',
        CourseSectionEnum.SECTION.value: '001',
        CourseSectionEnum.COURSE_TITLE.value: 'DESIGN AND SIMULATION STUDIO I',
        CourseSectionEnum.SECTION_TYPE.value: 'Lecture',
        CourseSectionEnum.TITLE_TOPIC.value: 'None',
        CourseSectionEnum.MEETING_PATTERN.value: 'MW 3pm-4:15pm',
        CourseSectionEnum.INSTRUCTOR.value: 'Shackelford, Todd (24904115) [Primary Instructor, Post, Print]',
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
        CourseSectionEnum.COMMENTS.value: 'DONE, AMJ - Peter Kiewit Institute 248',
        CourseSectionEnum.NOTES1.value: 'Peter Kiewit Institute 248',
        CourseSectionEnum.NOTES2.value: ''
    }

def test_course_section_initialization(valid_course_data):
    """Test if the CourseSection initializes correctly."""
    course_section = CourseSection(valid_course_data)
    
    assert course_section.department_code == 'UNO-AE'
    assert course_section.subject_code == 'AREN'
    assert course_section.catalog_number == '1030'
    assert course_section.section == '001'
    assert course_section.course_title == 'DESIGN AND SIMULATION STUDIO I'
    assert course_section.section_type == 'Lecture'
    assert course_section.title_topic == 'None'
    assert course_section.instructor == 'Shackelford, Todd (24904115) [Primary Instructor, Post, Print]'
    assert course_section.room == 'Peter Kiewit Institute 248'
    assert course_section.campus == 'UNO Engineering'
    assert course_section.inst_method == 'In Person'
    assert course_section.consent == 'No Special Consent Required'
    assert course_section.credit_hours_min == '3'
    assert course_section.credit_hours == '3'
    assert course_section.grade_mode == 'Graded'
    assert course_section.enrollment == '42'
    assert course_section.max_enrollment == '40'
    assert course_section.wait_cap == '99'
    assert course_section.warning == ""
    assert course_section.crosslistings_cleaned == []

def test_parse_rooms():
    """Test the parse_rooms function."""
    # Test case: multiple rooms
    assert parse_rooms('Peter Kiewit Institute 101; Peter Kiewit Institute 102') == ['Peter Kiewit Institute 101', 'Peter Kiewit Institute 102']
    
    # Test case: single room
    assert parse_rooms('Peter Kiewit Institute 101') == ['Peter Kiewit Institute 101']
    
    # Test case: 'Partially Online' should be excluded in multiple rooms
    assert parse_rooms('Peter Kiewit Institute 101; Partially Online') == ['Peter Kiewit Institute 101']
    
    # Test case: empty string should return an empty list
    assert parse_rooms('') == []

def test_parse_meetings():
    """Test the parse_meetings function."""
    meetings = parse_meetings('MWF 10am-11am; TR 1pm-2:30pm')
    assert len(meetings) == 5  # 5 meetings should be extracted
    assert meetings[0] == ('M', 600, 660)  # 'M' day, 10:00am-11:00am
    assert meetings[1] == ('W', 600, 660)
    assert meetings[2] == ('F', 600, 660)
    assert meetings[3] == ('T', 780, 870)
    assert meetings[4] == ('R', 780, 870)

def test_parse_time():
    """Test the parse_time function."""
    assert parse_time('10am') == 600  # 10:00 AM -> 600 minutes
    assert parse_time('3:15pm') == 915  # 3:15 PM -> 915 minutes
    assert parse_time('12pm') == 720  # 12:00 PM -> 720 minutes

def test_extract_room_numbers():
    """Test extract_room_numbers function."""
    
    # Test 1: Empty list
    rooms = []
    expected = []
    assert extract_room_numbers(rooms) == expected
    
    # Test 2: Rooms with valid room numbers
    rooms = ["Peter Kiewit Institute 101", "Meeting Peter Kiewit Institute 202", "Lab 303"]
    expected = ["101", "202", "303"]
    assert extract_room_numbers(rooms) == expected
    
    # Test 3: Rooms with no room numbers
    rooms = ["Conference Hall", "Peter Kiewit Institute", "ASH"]
    expected = ["To Be Announced", "To Be Announced", "To Be Announced"]
    assert extract_room_numbers(rooms) == expected
    
    # Test 4: Mixed rooms with and without numbers
    rooms = ["Peter Kiewit Institute 10A", "No Number Peter Kiewit Institute", "Peter Kiewit Institute 205"]
    expected = ["10", "To Be Announced", "205"]
    assert extract_room_numbers(rooms) == expected
    
    # Test 5: Rooms where numbers are part of a word or not present
    rooms = ["Peter Kiewit Institute 101A", "PKI102", "ServerLab", "123xyz"]
    expected = ["101", "102", "To Be Announced", "123"]
    assert extract_room_numbers(rooms) == expected
    
    # Test 6: Edge Case - Peter Kiewit Institute numbers with leading zeros
    rooms = ["Peter Kiewit Institute 007", "Peter Kiewit Institute 001", "Lab 004"]
    expected = ["007", "001", "004"]
    assert extract_room_numbers(rooms) == expected

    # Test 7: Peter Kiewit Institute numbers with only a single digit
    rooms = ["Peter Kiewit Institute 1", "Peter Kiewit Institute 2", "Peter Kiewit Institute 3"]
    expected = ["1", "2", "3"]
    assert extract_room_numbers(rooms) == expected

def test_time_to_str():
    # Test 1: Midnight (0 minutes)
    assert time_to_str(0) == "12:00am"
    
    # Test 2: Noon (720 minutes)
    assert time_to_str(720) == "12:00pm"
    
    # Test 3: 1:00am (60 minutes)
    assert time_to_str(60) == "1:00am"
    
    # Test 4: 1:00pm (780 minutes)
    assert time_to_str(780) == "1:00pm"
    
    # Test 5: 3:30pm (930 minutes)
    assert time_to_str(930) == "3:30pm"
    
    # Test 6: 11:59am (719 minutes)
    assert time_to_str(719) == "11:59am"
    
    # Test 7: 12:01pm (721 minutes)
    assert time_to_str(721) == "12:01pm"
    
    # Test 8: 8:15pm (1215 minutes)
    assert time_to_str(1215) == "8:15pm"
    
    # Test 9: 11:00pm (1380 minutes)
    assert time_to_str(1380) == "11:00pm"

    # Test 10: 7:05am (425 minutes)
    assert time_to_str(425) == "7:05am"

    # Test 11: 12:30pm (750 minutes)
    assert time_to_str(750) == "12:30pm"

    # Test 12: 8:30pm (1230 minutes)
    assert time_to_str(1230) == "8:30pm"


# Test cases for combine_section_info
def test_combine_section_info_single_room():
    result, warning = combine_section_info(
        "CSCI4970", [("M", 900, 1030), ("W", 900, 1030)], ["Peter Kiewit Institute 101"])
    assert result == [
        ("CSCI4970", "Peter Kiewit Institute 101", "M", 900, 1030),
        ("CSCI4970", "Peter Kiewit Institute 101", "W", 900, 1030)
    ]
    assert warning == ""

def test_combine_section_info_equal_rooms_and_times():
    result, warning = combine_section_info(
        "CSCI4970", [("M", 900, 1030), ("W", 900, 1030)], ["Peter Kiewit Institute 101", "Peter Kiewit Institute 102"])
    assert result == [
        ("CSCI4970", "Peter Kiewit Institute 101", "M", 900, 1030),
        ("CSCI4970", "Peter Kiewit Institute 102", "W", 900, 1030)
    ]
    assert warning == ""

def test_combine_section_info_two_rooms_one_meeting():
    result, warning = combine_section_info(
        "CSCI4970", [("M", 900, 1030)], ["Peter Kiewit Institute 101", "Peter Kiewit Institute 102"])
    assert result == [
        ("CSCI4970", "Peter Kiewit Institute 101", "M", 900, 1030),
        ("CSCI4970", "Peter Kiewit Institute 102", "M", 900, 1030)
    ]
    assert warning == ""

def test_combine_section_info_two_rooms_multiple_meetings():
    result, warning = combine_section_info(
        "CSCI4970", [("M", 900, 1030), ("W", 900, 1030), ("F", 1000, 1130)], ["Peter Kiewit Institute 101", "Peter Kiewit Institute 102"])
    assert result == [
        ("CSCI4970", "Peter Kiewit Institute 101", "M", 900, 1030),
        ("CSCI4970", "Peter Kiewit Institute 102", "W", 900, 1030),
        ("CSCI4970", "Peter Kiewit Institute 102", "F", 1000, 1130)
    ]
    assert warning == ""

# def test_combine_section_info_more_rooms_than_meeting_times():
#     result, warning = combine_section_info(
#         "CSCI4970", [("M", 900, 1030), ("W", 900, 1030), ("T", 900, 1030), ("F", 900, 1030)], ["Peter Kiewit Institute 101", "Peter Kiewit Institute 102", "Peter Kiewit Institute 103"])
#     assert result == [("CSCI4970", "Peter Kiewit Institute 101", "M", 900, 1030), ("CSCI4970", "Peter Kiewit Institute 101", "W", 900, 1030),
#         ("CSCI4970", "Peter Kiewit Institute 102", "T", 900, 1030),
#         ("CSCI4970", "Peter Kiewit Institute 103", "F", 900, 1030)]
#     assert warning == "Condition 2b triggered: 3+ rooms and 4+ meeting times. Make sure CSCI4970 has correct meeting times with each room it uses. Unable to determine automatically."

def test_combine_section_info_more_meeting_times_than_rooms():
    result, warning = combine_section_info(
        "CSCI4970", [("M", 900, 1030), ("W", 900, 1030), ("F", 900, 1030)], ["Peter Kiewit Institute 101", "Peter Kiewit Institute 102"])
    assert result == [
        ("CSCI4970", "Peter Kiewit Institute 101", "M", 900, 1030),
        ("CSCI4970", "Peter Kiewit Institute 102", "W", 900, 1030),
        ("CSCI4970", "Peter Kiewit Institute 102", "F", 900, 1030)
    ]
    assert warning == ""


def test_parse_crosslistings():
    # Example input text with various course listings
    text = """
    CSCI 1010-001, MATH 2200-002, ENGR 3050-003, CSCI 3050-004, MATH-3300-005,
    ENGR 4400-006, CSCI-4999-007, MATH 2220-008
    """
    
    # Expected section IDs based on the above input
    expected = [
        'CSCI 1010-1',
        'MATH 2200-2',
        'ENGR 3050-3',
        'CSCI 3050-4',
        'MATH-3300-5',
        'ENGR 4400-6',
        'CSCI-4999-7',
        'MATH 2220-8'
    ]
    
    # Call the function to parse the crosslistings
    result = parse_crosslistings(text)
    
    # Assert that the result matches the expected list of section IDs
    assert result == expected