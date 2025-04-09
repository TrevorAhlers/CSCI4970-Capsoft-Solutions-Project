import re
from typing import Dict
from Model.Classroom import Classroom
from Model.CourseSection import CourseSection

global count

def default_assignment(classrooms: Dict[str, Classroom], sections: Dict[str, CourseSection]):
	# All three of these operate on the same references
	# so there's no need to return classroom/section again.
	assign_sections_to_rooms(classrooms, sections)
	assigned_count1 = assign_via_frequency_map_department(classrooms, sections)
	assigned_count2 = assign_via_frequency_map(classrooms, sections)
	assigned_count = assigned_count1+assigned_count2
	print(f'```````````````````````````')
	print(f'assigner.py: Automatically assigned {assigned_count}/{len(sections)} sections to rooms.')
	print(f'assigner.py: Total rooms assigned: {print_assignment_stats(sections)}/{len(sections)}.')
	print(f'assigned count 1: {assigned_count1}')
	print(f'assigned count 2: {assigned_count2}')
	print(f'===========================')
	# You can return nothing or just the assigned count if desired
	return assigned_count


def assign_sections_to_rooms(classrooms: Dict[str, Classroom], sections: Dict[str, CourseSection]) -> None:
	for section_key, section_obj in sections.items():
		room_names = section_obj.rooms
		if not room_names or "TBD" in room_names:
			continue

		for room_name in room_names:
			if room_name not in classrooms:
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
			if s_key not in classrooms:
				row_data = {
					"Room Number": s_key,
					"Seats": "N/A",
					"Displays": "N/A",
					"Computer Count": "N/A",
					"Information and Connectivity": "N/A"
				}
				classrooms[s_key] = Classroom(row_data)
				classrooms[s_key].add_course_section_object(section_obj)

def department_match(classroom: Classroom, section: CourseSection):
	candidate_depts, dept_max = find_max_frequency_dept(classroom.department_counts)
	if candidate_depts:
		for dept in candidate_depts:
			if dept == section.subject_code:
				return True
	return False


def assign_via_frequency_map_department(classrooms: Dict[str, Classroom], sections: Dict[str, CourseSection]) -> int:
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
				best_candidate_room = best_candidate_rooms[0]
				if best_candidate_room not in classrooms:
					best_candidate_rooms.pop(0)
					continue
				
				if not department_match(classrooms[best_candidate_room], section):
					best_candidate_rooms.pop(0)
					continue
				

				try:
					classrooms[best_candidate_room].add_course_section_object(section)
					conflicts = classrooms[best_candidate_room].find_conflicts()
				except:
					print(f'assigner.py: Failed to assign {section.id} to {best_candidate_room}.')
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
				else:
					section.add_room(best_candidate_room)
					section.room = room_str_maker(section)
				assigned_count += 1
				print(f'assigner.py: Assigned {section.id} to room {room}. Method: department freq map')
				break

	return assigned_count


def assign_via_frequency_map(classrooms: Dict[str, Classroom], sections: Dict[str, CourseSection]) -> int:
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
				best_candidate_room = best_candidate_rooms[0]
				if best_candidate_room not in classrooms:
					best_candidate_rooms.pop(0)
					continue

				try:
					classrooms[best_candidate_room].add_course_section_object(section)
					conflicts = classrooms[best_candidate_room].find_conflicts()
				except:
					print(f'assigner.py: Failed to assign {section.id} to {best_candidate_room}.')
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
				else:
					section.add_room(best_candidate_room)
					section.room = room_str_maker(section)
				assigned_count += 1
				print(f'assigner.py: Assigned {section.id} to room {room}. Method: freq map')
				break

	return assigned_count


def find_max_frequency(frequency_map: Dict[str, int]):
	sorted_items = sorted(frequency_map.items(), key=lambda x: x[1], reverse=True)
	if sorted_items:
		top5_keys = [room for room, count in sorted_items[:5]]
		max_value = sorted_items[0][1]
		return top5_keys, max_value
	return None, 0

def find_max_frequency_dept(frequency_map: Dict[str, int]):
	max_solution = []
	sorted_items = sorted(frequency_map.items(), key=lambda x: x[1], reverse=True)
	if sorted_items:
		max_value = sorted_items[0][1]
		for room in sorted_items:
			if room[1] != max_value:
				break
			max_solution.append(room[0])
		return max_solution, max_value
	return None, 0

def room_str_maker(section: CourseSection):
	room_update_str = ''
	for room_u in section.rooms:
		room_update_str += f'{room_u}; '
	room_update_str = room_update_str[:-2]
	return room_update_str


def print_assignment_stats(sections: Dict[str, CourseSection]) -> int:
	count = 0
	for _, section in sections.items():
		if section.rooms != ['TBD']:
			count += 1
	return count
