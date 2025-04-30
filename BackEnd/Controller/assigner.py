import re
from typing import Dict
from Model.Classroom import Classroom
from Model.CourseSection import CourseSection, combine_section_info
from typing import List, Tuple

global count

def default_assignment(classrooms: Dict[str, Classroom], sections: Dict[str, CourseSection]):
	# All three of these operate on the same references
	# so there's no need to return classroom/section again.
	assign_sections_to_rooms(classrooms, sections)
	assigned_count1 = assign_via_frequency_map_department(classrooms, sections)
	assigned_count2 = assign_via_frequency_map(classrooms, sections)
	assigned_count3 = assign_via_special_requirements(sections, classrooms)
	assigned_count = assigned_count1+assigned_count2+assigned_count3
	print(f'```````````````````````````')
	print(f'assigner.py: Automatically assigned {assigned_count}/{len(sections)} sections to rooms.')
	print(f'assigner.py: Total rooms assigned: {print_assignment_stats(sections)}/{len(sections)}.')
	print(f'assigned count 1: {assigned_count1}')
	print(f'assigned count 2: {assigned_count2}')
	print(f'assigned count 3: {assigned_count3}')
	print(f'===========================')
	
	return assigned_count


def assign_sections_to_rooms(classrooms: Dict[str, Classroom], sections: Dict[str, CourseSection]) -> None:
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
			if section.rooms != ['To Be Announced']:
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


def assign_via_frequency_map(classrooms: Dict[str, Classroom], sections: Dict[str, CourseSection]) -> int:
	assigned_count = 0
	for room_key, classroom in classrooms.items():
		room = classroom.room
		for section_key, section in sections.items():
			if section.rooms != ['To Be Announced']:
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

def assign_via_special_requirements(sections: Dict[str, CourseSection],
									classrooms: Dict[str, Classroom]) -> int:
	"""
	Assign remaining unassigned course sections to available classrooms using a conservative strategy.

	Only assigns a section to a classroom if:
		- The classroom meets or exceeds all of the section's known requirements (seats, displays, computers, connectivity, etc.)
		- Assigning the section to that classroom causes no scheduling conflicts
	It will try to find a single suitable room for each unassigned section. If none is found and the section can be split across multiple rooms, it will attempt a multi-room assignment (all chosen rooms must be free and meet requirements).
	Sections that cannot be safely assigned will remain unassigned.
	"""

	def room_has_all_features(room: Classroom, required_keywords: List[str]) -> bool:
		# Return True if every keyword is found in the room’s connectivity / display text.
		text = f"{room.displays} {room.info_and_connectivity}".lower()
		return all(kw.lower() in text for kw in required_keywords)

	assigned_count = 0

	for section in sections.values():
		if section.rooms != ["To Be Announced"]:
			continue

		# ------------  derive requirements  ----------------
		req_seats      = to_int(section.rm_cap_request) \
							or to_int(section.max_enrollment) \
							or to_int(section.enrollment)

		req_displays   = 1 if "projector" in section.attributes.lower() \
							or "projector" in section.course_attributes.lower() else 0

		req_computers  = 1 if section.section_type.lower() in ("laboratory", "lab") else 0

		# keyword parsing
		req_features   = []
		if "hdmi" in section.comments.lower():
			req_features.append("hdmi")

		# ------------  gather viable single-room candidates  ------------
		candidates: List[Classroom] = []
		for room in classrooms.values():
			if to_int(room.seats)            < req_seats:     continue
			if to_int(room.displays)         < req_displays:  continue
			if to_int(room.computer_count)   < req_computers: continue
			if not room_has_all_features(room, req_features):  continue
			if room.find_conflicts():                    continue
			candidates.append(room)

		# small-first fit (lowest surplus seats) to avoid hogging big rooms
		candidates.sort(key=lambda r: to_int(r.seats) - req_seats)

		if candidates:
			commit_assignment(section, [candidates[0]])
			assigned_count += 1
			continue

		# conservative two-room fallback
		if getattr(section, "allows_multi_room", False):
			free_pairs: List[Tuple[Classroom, Classroom]] = []
			for i, r1 in enumerate(classrooms.values()):
				for r2 in list(classrooms.values())[i + 1:]:
					if r1 == r2:continue
					if r1.find_conflicts() or r2.find_conflicts():continue
					if to_int(r1.seats) + to_int(r2.seats) < req_seats:continue
					if not (room_has_all_features(r1, req_features) and
							room_has_all_features(r2, req_features)):continue
					free_pairs.append((r1, r2))
			if free_pairs:
				# pick the best pair of rooms
				best = min(free_pairs,
							key=lambda p: (to_int(p[0].seats) + to_int(p[1].seats)) - req_seats)
				commit_assignment(section, list(best))
				assigned_count += 1

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
		if section.rooms != ['To Be Announced']:
			count += 1
	return count

def commit_assignment(section: CourseSection, classroom: Classroom):
	classroom.add_course_section_object(section)
	if section.rooms == ['To Be Announced']:
		section.rooms = [classroom.room]
	else:
		section.add_room(classroom.room)
	section.room = room_str_maker(section)

def room_has_all_features(room: Classroom, needed: set[str]) -> bool:
	if not needed:
		return True
	room_text = f"{room.displays} {room.info_and_connectivity}".lower()
	return all(feature.lower() in room_text for feature in needed)

def to_int(x: str | int | None) -> int:
	if isinstance(x, int):
		return x
	if isinstance(x, str) and x.strip().isdigit():
		return int(x)
	return 0