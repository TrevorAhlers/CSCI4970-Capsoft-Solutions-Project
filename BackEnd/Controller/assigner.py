import re
from typing import Dict
from Model.Classroom import Classroom
from Model.CourseSection import CourseSection


def assign_sections_to_rooms(classrooms: Dict[str, Classroom], sections: Dict[str, CourseSection]):

    for section_key, section_obj in sections.items():
        room_name = section_obj.room_number
        if not room_name:
            continue  # if there's no room specified at all, skip

		# Default info for a room if it hasn't already been built.
        if room_name not in classrooms:
            row_data = {
                "Room Number": room_name,
                "Seats": "None",
                "Displays": "None",
                "Computer Count": "None",
                "Information and Connectivity": "None"
			}
            classrooms[room_name] = Classroom(row_data)

		# Now add the course section's schedule to that classroom
        classrooms[room_name].add_course_section_object(section_obj)