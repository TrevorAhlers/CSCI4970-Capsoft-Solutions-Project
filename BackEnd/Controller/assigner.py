import re
from typing import Dict
from Model.Classroom import Classroom
from Model.CourseSection import CourseSection


def assign_sections_to_rooms(classrooms: Dict[str, Classroom], sections: Dict[str, CourseSection]):

    for section_key, section_obj in sections.items():
        room_names = section_obj.room_numbers
        if (not room_names) or ("TBD" in room_names):
            continue  # if there's no room specified at all, skip

		# Default info for a room if it hasn't already been built. (We are searching for the keys)
        for room_name in room_names:
            if room_name not in classrooms:
                row_data = {
                    "Room Number": room_name,
                    "Seats": "None",
                    "Displays": "None",
                    "Computer Count": "None",
                    "Information and Connectivity": "None"
                }
                classrooms[room_name[0]] = Classroom(row_data)

		# Now add the course section's schedule to that classroom
            classrooms[room_name[0]].add_course_section_object(section_obj)