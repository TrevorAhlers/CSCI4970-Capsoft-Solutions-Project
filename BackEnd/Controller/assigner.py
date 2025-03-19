import re
from typing import Dict
from Model.Classroom import Classroom
from Model.CourseSection import CourseSection



def default_assignment(classrooms: Dict[str, Classroom], sections: Dict[str, CourseSection]):
	classrooms, sections = assign_sections_to_rooms(classrooms, sections)
	classrooms, sections = assign_via_frequency_map(classrooms, sections)
	return classrooms, sections


def assign_sections_to_rooms(classrooms: Dict[str, Classroom], sections: Dict[str, CourseSection]):

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

	for room_key,classroom in classrooms.items():
		room = classroom.room
		# section freq map example - Dict['Peter Kiewit Institute 276': 1]
		for section_key,section in sections.items():
			if (room not in section.room_freq.keys()):
				continue
			if (section.rooms != ['TBD']):
				continue
			# find best candidate room
			best_candidate_rooms, count = find_max_frequency(section.room_freq)
			print("best_candidate_rooms",best_candidate_rooms)

			#print("best_candidate_rooms",best_candidate_rooms)

			while (best_candidate_rooms):
				conflicts = None
				for best_candidate_room in best_candidate_rooms:
					if best_candidate_room not in classrooms:
						best_candidate_rooms.pop(0)
						continue
					try:
						conflicts = classrooms[best_candidate_room].find_conflicts()
					except:
						print(f'Failed to attempt candidate {best_candidate_room} assignment to {section.id}.')
						pass
					
					if conflicts:
						best_candidate_rooms.pop(0)
						print(f'Could not assign {section.id} to {best_candidate_room}. Conflicts: {len(conflicts)}')
						continue
					elif (section.rooms != ['TBD']):
						best_candidate_rooms.pop(0)
						continue
					else:
						print(f'Assigned {section.id} to room {room}. Method: freq map')
						if section.rooms == ['TBD']:
							section.rooms = [best_candidate_room]
							section.room = room_str_maker(section)
						else:
							classroom.add_course_section_object(section)
							section.add_room(best_candidate_room)
							section.room = room_str_maker(section)
						best_candidate_rooms.pop(0)
	return classrooms, sections


def find_max_frequency(frequency_map: Dict[str, int]):      # use value from dict... (x[0], x[1]) same as (key, value)
	sorted_items = sorted(frequency_map.items(), key=lambda x: x[1], reverse=True)
	if sorted_items:
		top5_keys = [room for room, count in sorted_items[:5]]
		max_value = sorted_items[0][1]
		return top5_keys, max_value
	return None, 0

def room_str_maker(section):
	room_update_str = ''
	for room_u in section.rooms:
		room_update_str += f'{room_u}; '
	room_update_str = room_update_str[:-2]
	return room_update_str