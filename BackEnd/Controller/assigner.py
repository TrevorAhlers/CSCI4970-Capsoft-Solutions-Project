import re
from typing import Dict
from Model.Classroom import Classroom, DAY_OFFSETS
from Model.CourseSection import CourseSection, combine_section_info
from typing import List, Tuple


def default_assignment(classrooms: Dict[str, Classroom], sections: Dict[str, CourseSection], logic: set[str]):
	"""
	Main entry point to the auto-assigner
	"""

	assign_sections_to_rooms(classrooms, sections)

	assigned_count1 = assigned_count2 = assigned_count3 = 0

	if "historical-dept" in logic:
		assigned_count1 = assign_via_frequency_map_department(classrooms, sections)
	if "historical" in logic:
		assigned_count2 = assign_via_frequency_map(classrooms, sections)
	if "predictive" in logic:
		assigned_count3 = assign_via_special_requirements(sections, classrooms)

	assigned_count = assigned_count1 + assigned_count2 + assigned_count3
	print(f'```````````````````````````')
	print(f'assigner.py: Automatically assigned {assigned_count}/{len(sections)} sections to rooms.')
	print(f'assigner.py: Total rooms assigned: {print_assignment_stats(sections)}/{len(sections)}.')
	print(f'assigned count 1: {assigned_count1}')
	print(f'assigned count 2: {assigned_count2}')
	print(f'assigned count 3: {assigned_count3}')
	print(f'===========================')
	return assigned_count


#...........................................................................................................
def assign_sections_to_rooms(classrooms: Dict[str, Classroom], sections: Dict[str, CourseSection]) -> None:
	"""
	Initial pass to attach known room assignments to classrooms and update their schedules from the CSV

	Missing rooms are auto-populated if unrecognized room numbers exist on the CSV
	"""

	for section_key, section_obj in sections.items():
		room_names = section_obj.rooms
		if not room_names or "To Be Announced" in room_names:
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

#...........................................................................................................
def department_match(classroom: Classroom, section: CourseSection):
	"""
	Returns True if the section's department matches the most common department for the room
	"""

	candidate_depts, dept_max = find_max_frequency_dept(classroom.department_counts)
	if candidate_depts:
		for dept in candidate_depts:
			if dept == section.subject_code:
				return True
	return False

#...........................................................................................................
def assign_via_frequency_map_department(classrooms: Dict[str, Classroom], sections: Dict[str, CourseSection]) -> int:
	"""
	Tries to assign sections based on their most-used rooms and department alignment
	"""
	assigned_count = 0
	for room_key, classroom in classrooms.items():
		room = classroom.room
		for section_key, section in sections.items():
			if section.rooms != ['To Be Announced']:
				continue
			if inherit_crosslisted_room(section, sections):
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

				print(f'Trying to assign {section.id} to {best_candidate_room}')
				if classroom_would_conflict(classrooms[best_candidate_room], section):
					best_candidate_rooms.pop(0)
					print(f'assigner.py: Could not assign {section.id} to {best_candidate_room}. Conflicts.')
					continue

				classrooms[best_candidate_room].add_course_section_object(section)
				if section.rooms == ['To Be Announced']:
					section.rooms = [best_candidate_room]
					section.room = room_str_maker(section)
				else:
					section.add_room(best_candidate_room)
					section.room = room_str_maker(section)
				assigned_count += 1
				print(f'assigner.py: Assigned {section.id} to room {room}. Method: department freq map')
				break

	return assigned_count

#...........................................................................................................
def assign_via_frequency_map(classrooms: Dict[str, Classroom], sections: Dict[str, CourseSection]) -> int:
	"""
	Assigns sections to rooms based only on past frequency of use, checking for conflicts
	"""
	assigned_count = 0
	for room_key, classroom in classrooms.items():
		room = classroom.room
		for section_key, section in sections.items():
			if section.rooms != ['To Be Announced']:
				continue
			if inherit_crosslisted_room(section, sections):
				continue
			if room not in section.room_freq:
				continue

			best_candidate_rooms, _ = find_max_frequency(section.room_freq)
			while best_candidate_rooms:
				best_candidate_room = best_candidate_rooms[0]
				if best_candidate_room not in classrooms:
					best_candidate_rooms.pop(0)
					continue

				print(f'Trying to assign {section.id} to {best_candidate_room}')
				if classroom_would_conflict(classrooms[best_candidate_room], section):
					best_candidate_rooms.pop(0)
					print(f'assigner.py: Could not assign {section.id} to {best_candidate_room}. Conflicts.')
					continue

				classrooms[best_candidate_room].add_course_section_object(section)
				if section.rooms == ['To Be Announced']:
					section.rooms = [best_candidate_room]
					section.room = room_str_maker(section)
				else:
					section.add_room(best_candidate_room)
					section.room = room_str_maker(section)
				assigned_count += 1
				print(f'assigner.py: Assigned {section.id} to room {room}. Method: freq map')
				break

	return assigned_count

#...........................................................................................................
def assign_via_special_requirements(sections: Dict[str, CourseSection],
									classrooms: Dict[str, Classroom]) -> int:
	def room_has_all_features(room: Classroom, required_keywords: List[str]) -> bool:
		text = f"{room.displays} {room.info_and_connectivity}".lower()
		return all(kw.lower() in text for kw in required_keywords)

	assigned_count = 0

	for section in sections.values():
		if section.rooms != ["To Be Announced"]:
			continue
		if inherit_crosslisted_room(section, sections):
			continue

		req_seats      = to_int(section.rm_cap_request) or to_int(section.max_enrollment) or to_int(section.enrollment)
		req_displays   = 1 if "projector" in section.attributes.lower() or "projector" in section.course_attributes.lower() else 0
		req_computers  = 1 if section.section_type.lower() in ("laboratory", "lab") else 0
		req_features   = ["hdmi"] if "hdmi" in section.comments.lower() else []

		candidates: List[Classroom] = []
		for room in classrooms.values():
			if to_int(room.seats) < req_seats: continue
			if to_int(room.displays) < req_displays: continue
			if to_int(room.computer_count) < req_computers: continue
			if not room_has_all_features(room, req_features): continue
			if classroom_would_conflict(room, section): continue
			candidates.append(room)

		candidates.sort(key=lambda r: to_int(r.seats) - req_seats)

		if candidates:
			commit_assignment(section, candidates[0])
			assigned_count += 1

	return assigned_count



#...........................................................................................................
def find_max_frequency(frequency_map: Dict[str, int]):
	"""
	Returns top 5 rooms with the highest frequency from the frequency map
	"""

	sorted_items = sorted(frequency_map.items(), key=lambda x: x[1], reverse=True)
	if sorted_items:
		top5_keys = [room for room, count in sorted_items[:5]]
		max_value = sorted_items[0][1]
		return top5_keys, max_value
	return None, 0


def find_max_frequency_dept(frequency_map: Dict[str, int]):
	"""
	Returns department(s) with the highest count from a frequency map
	"""
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

#...........................................................................................................
def room_str_maker(section: CourseSection):
	"""
	Returns a semicolon-separated string of room names assigned to a section
	"""

	room_update_str = ''
	for room_u in section.rooms:
		room_update_str += f'{room_u}; '
	room_update_str = room_update_str[:-2]
	return room_update_str

#...........................................................................................................
def print_assignment_stats(sections: Dict[str, CourseSection]) -> int:
	"""
	Counts how many sections have been assigned to a room
	"""
	count = 0
	for _, section in sections.items():
		if section.rooms != ['To Be Announced']:
			count += 1
	return count

#...........................................................................................................
def commit_assignment(section: CourseSection, classroom: Classroom | List[Classroom]):
	"""
	Adds room/rooms to a CourseSection obj
	"""

	if isinstance(classroom, list):
		for room in classroom:
			room.add_course_section_object(section)
			section.add_room(room.room)
	else:
		classroom.add_course_section_object(section)
		if section.rooms == ['To Be Announced']:
			section.rooms = [classroom.room]
		else:
			section.add_room(classroom.room)
	section.room = room_str_maker(section)

#...........................................................................................................
def to_int(x: str | int | None) -> int:
	if isinstance(x, int):
		return x
	if isinstance(x, str) and x.strip().isdigit():
		return int(x)
	return 0

#...........................................................................................................
def inherit_crosslisted_room(section: CourseSection, sections: Dict[str, CourseSection]) -> bool:
	"""
	If a room pending assignment has crosslistings... check them to see if they have room assignments

	If they do, then just assign current room to the same room
	"""

	if not section.crosslistings_cleaned:
		return False
	for cid in section.crosslistings_cleaned:
		if cid not in sections:
			continue
		linked = sections[cid]
		if linked.rooms and linked.rooms != ['To Be Announced']:
			section.rooms = linked.rooms.copy()
			section.room = room_str_maker(section)
			return True
	return False
#...........................................................................................................
def classroom_would_conflict(room: Classroom, section: CourseSection) -> bool:
	"""
	Determine time slot conflict before actually committing to the room schedule
	"""

	schedule = section.schedule
	section.update_meetings(schedule)
	new_intervals = []
	for _, _, d, start_min, end_min in schedule:
		if d in DAY_OFFSETS:
			day_offset = DAY_OFFSETS[d]
			start_slot = day_offset + start_min
			end_slot = day_offset + end_min
			new_intervals.append((start_slot, end_slot))

	existing = room.gather_intervals()
	for _, start1, end1 in existing:
		for start2, end2 in new_intervals:
			if start1 < end2 and start2 < end1:
				return True
	return False
