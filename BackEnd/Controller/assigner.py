import re
from typing import Dict
from Model.Classroom import Classroom
from Model.CourseSection import CourseSection

global count

def default_assignment(classrooms: Dict[str, Classroom], sections: Dict[str, CourseSection]):
	"""
    Automatically assigns sections to classrooms based on predefined criteria.

    Args:
        classrooms (Dict[str, Classroom]): A dictionary of classroom objects indexed by room names.
        sections (Dict[str, CourseSection]): A dictionary of course sections indexed by section IDs.

    Returns:
        Tuple[Dict[str, Classroom], Dict[str, CourseSection]]: Updated dictionaries of classrooms and sections.
    """
	classrooms, sections = assign_sections_to_rooms(classrooms, sections)
	classrooms, sections, assigned_count = assign_via_frequency_map(classrooms, sections)
	print(f'```````````````````````````')
	print(f'assigner.py: Automatically assigned {assigned_count}/{len(sections)} sections to rooms.')
	print(f'assigner.py: Total rooms assigned: {print_assignment_stats(sections)}/{len(sections)}.')
	print(f'===========================')
	return classrooms, sections


def assign_sections_to_rooms(classrooms: Dict[str, Classroom], sections: Dict[str, CourseSection]):
	"""
    This function finds sections that have assigned rooms (assigned on the spreadsheet or through editing)
    and creates room objects (if they don't exist already) with default "None" data for all attributes.
    Then assigns sections to those rooms and generates a frequency map.

    Args:
        classrooms (Dict[str, Classroom]): A dictionary of classroom objects indexed by room names.
        sections (Dict[str, CourseSection]): A dictionary of course sections indexed by section IDs.

    Returns:
        Tuple[Dict[str, Classroom], Dict[str, CourseSection]]: Updated dictionaries of classrooms and sections.
    """

	# This function finds sections that have assigned rooms (assigned on the spreadsheet or through editing)
	# and creates room objects (if they don't exist already) with default "None" data for all attributes.
	# 
	# Assigned sections are added to each room's schedule via the add_course_section_object() function.
	# Then we generate our frequency map.
	for section_key, section_obj in sections.items():
		room_names = section_obj.rooms
			
		if (not room_names) or ("TBD" in room_names):
			continue  # Skip unassigned sections

		# Default info for a room if it hasn't already been built
		for room_name in room_names:
			if room_name not in classrooms.keys():
				row_data = {
					"Room Number": room_name,
					"Seats": "N/A",
					"Displays": "N/A",
					"Computer Count": "N/A",
					"Information and Connectivity": "N/A"
				}

				classrooms[room_name] = Classroom(row_data)
				classrooms[room_name].add_course_section_object(section_obj)

		for s_key in section_obj.room_freq.keys():
			if s_key not in classrooms.keys():
				row_data = {
					"Room Number": s_key,
					"Seats": "N/A",
					"Displays": "N/A",
					"Computer Count": "N/A",
					"Information and Connectivity": "N/A"
				}
				classrooms[s_key] = Classroom(row_data)
				classrooms[s_key].add_course_section_object(section_obj)
						

		# Add the course section's schedule to that classroom
			

	return classrooms, sections

def assign_via_frequency_map(classrooms: Dict[str, Classroom], sections: Dict[str, CourseSection]):
	"""
    Assigns course sections to classrooms using a frequency map. The frequency map is used to determine
    the best classroom for each section based on the room's availability and conflicts.

    Args:
        classrooms (Dict[str, Classroom]): A dictionary of classroom objects indexed by room names.
        sections (Dict[str, CourseSection]): A dictionary of course sections indexed by section IDs.

    Returns:
        Tuple[Dict[str, Classroom], Dict[str, CourseSection], int]: 
        Updated dictionaries of classrooms and sections, and the count of assigned sections.
    """
	assigned_count = 0
	for room_key, classroom in classrooms.items():
		room = classroom.room
		for section_key, section in sections.items():
			if section.rooms != ['TBD']:
				continue
			if room not in section.room_freq:
				continue

			best_candidate_rooms, _ = find_max_frequency(section.room_freq)

			while best_candidate_rooms:
				conflicts = None
				best_candidate_room = best_candidate_rooms[0]

				if best_candidate_room not in classrooms:
					best_candidate_rooms.pop(0)
					continue

				try:
					classrooms[best_candidate_room].add_course_section_object(section)
					conflicts = classrooms[best_candidate_room].find_conflicts()
				except:
					print(f'assigner.py: Failed to attempt candidate {best_candidate_room} assignment to {section.id}.')
					best_candidate_rooms.pop(0)
					continue

				if conflicts:
					classrooms[best_candidate_room].remove_course_section(section)
					best_candidate_rooms.pop(0)
					print(f'assigner.py: Could not assign {section.id} to {best_candidate_room}. Conflicts: {len(conflicts)}')
					continue

				if section.rooms == ['TBD']:
					section.rooms = [best_candidate_room]
					section.room = room_str_maker(section)
					assigned_count += 1
					print(f'assigner.py: Assigned {section.id} to room {room}. Method: freq map')
				else:
					section.add_room(best_candidate_room)
					section.room = room_str_maker(section)
					classrooms[best_candidate_room].add_course_section_object(section)
					assigned_count += 1
					print(f'assigner.py: Assigned {section.id} to room {room}. Method: freq map')
				break
	return classrooms, sections, assigned_count



def find_max_frequency(frequency_map: Dict[str, int]):		# use value from dict... (x[0], x[1]) same as (key, value)
	"""
    Finds the rooms with the highest frequency in the provided frequency map.

    Args:
        frequency_map (Dict[str, int]): A dictionary mapping room names to their respective frequencies.

    Returns:
        Tuple[List[str], int]: A list of room names with the highest frequency and the frequency value.
    """
	sorted_items = sorted(frequency_map.items(), key=lambda x: x[1], reverse=True)
	if sorted_items:
		top5_keys = [room for room, count in sorted_items[:5]]
		max_value = sorted_items[0][1]
		return top5_keys, max_value
	return None, 0

def room_str_maker(section):
	"""
    Generates a string representation of the rooms assigned to a section.

    Args:
        section (CourseSection): The course section whose rooms are being represented.

    Returns:
        str: A string of room names separated by semicolons.
    """
	room_update_str = ''
	for room_u in section.rooms:
		room_update_str += f'{room_u}; '
	room_update_str = room_update_str[:-2]
	return room_update_str

def print_assignment_stats(sections: Dict[str, CourseSection]):
	"""
    Prints statistics on the current assignments of sections to rooms.

    Args:
        sections (Dict[str, CourseSection]): A dictionary of course sections indexed by section IDs.

    Returns:
        int: The number of sections that have been successfully assigned to rooms.
    """
	count = 0
	for _,section in sections.items():
		if section.rooms != ['TBD']:
			count += 1
	return count