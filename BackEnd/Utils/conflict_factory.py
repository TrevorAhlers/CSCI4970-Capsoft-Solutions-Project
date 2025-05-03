from typing import Dict, List
from Model.Classroom import Classroom, ClassroomEnum
from Model.CourseSection import CourseSection, CourseSectionEnum, combine_section_info
from Model.Conflict import Conflict

TIME_BETWEEN_CLASSES = 5

#............................................................................................................
def build_conflicts(sections: Dict[str, CourseSection], classrooms: Dict[str, Classroom]) -> List[Conflict]:
	"""
	Entry point... Builds a full list of conflicts using the individual strategies
	"""

	conflicts,time_count = build_time_conflicts(sections,classrooms)
	conflicts,capacity_count = build_capacity_conflicts(sections,classrooms,conflicts)
	conflicts,parse_count = build_parse_conflicts(sections,conflicts)
	print(f"conflict_factory.py: Built {len(conflicts)} Conflict objects.")
	print(f"conflict_factory.py: {time_count}/{len(conflicts)} were time conflicts.")
	print(f"conflict_factory.py: {capacity_count}/{len(conflicts)} were capacity conflicts.")
	print(f"conflict_factory.py: {parse_count}/{len(conflicts)} were parse conflicts.")
	return conflicts

#............................................................................................................
def build_time_conflicts(sections: Dict[str, CourseSection],classrooms: Dict[str, Classroom]) -> List[Conflict]:
	"""
	Creates conflicts when CourseSection objs overlap in time within the same room and aren't crosslisted
	"""

	output_conflicts: List[Conflict] = []

	for classroom in classrooms.values():

		# minute–level overlaps for this room
		for overlap in classroom.find_conflicts():

			conflict_cluster: List[CourseSection] = []
			times: List[List[int]]                = []
			win_start = win_end = None

			i = 0
			while i < len(overlap):
				sec_id, start, end = overlap[i], overlap[i + 1], overlap[i + 2]
				i += 3

				# ignore only *remote-learning* exclusions
				if sec_id in conflict_exclusions_generator(
						sections[sec_id], sections):
					continue

				sec = sections[sec_id]

				if not conflict_cluster:
					conflict_cluster.append(sec)
					times.append([start, end])
					win_start, win_end = start, end
				elif start <= win_end + TIME_BETWEEN_CLASSES:
					conflict_cluster.append(sec)
					times.append([start, end])
					win_start = min(win_start, start)
					win_end   = max(win_end,   end)
				else:
					add_conflict_if_unique(output_conflicts,
											conflict_cluster, times,
											[classroom.room])
					conflict_cluster = [sec]
					times            = [[start, end]]
					win_start, win_end = start, end

			# flush remainder
			if conflict_cluster:
				add_conflict_if_unique(output_conflicts,
										conflict_cluster, times,
										[classroom.room])


	def same_crosslist_group(cluster: List[CourseSection]) -> bool:
		first = cluster[0]
		group = set(first.crosslistings_cleaned)
		return all(s.id in group for s in cluster)

	filtered = [
		c for c in output_conflicts
		if (c.conflict_message or c.section_count >= 2)
		and not same_crosslist_group(c.sections)
	]
	return filtered, len(filtered)

#............................................................................................................
def build_parse_conflicts(sections: Dict[str,CourseSection], output_conflicts: List[Conflict]) -> List[Conflict]:
	"""
	Creates conflicts when meeting time and room parsing is ambiguous or fails entirely

	This lets the user know to review the potentially problematic assignment
	"""

	start_count = len(output_conflicts)
	for sec_id, section in sections.items():
		if section.rooms == ['To Be Announced']:
			continue

		try:
			warn_msg = section.warning

			# If there's a warning for the user, due to uncertainty for room/meetings
			# parsing, then we create a conflict object for them to ignore or fix.
			if warn_msg and (section.rooms != ['To Be Announced']):
				add_conflict_if_unique(output_conflicts, [section], [], section.rooms, warn_msg)

		# Worst case scenario where we fail to parse entirely and we pass the error onto the
		# user as a conflict object. Better than crashing for no reason...
		except ValueError as e:
			if (len(set(section.rooms)) == 1) and (section.rooms != ['To Be Announced']):
				add_conflict_if_unique(output_conflicts, [section], [], section.rooms, str(e))
	return output_conflicts, len(output_conflicts) - start_count

#............................................................................................................
def build_capacity_conflicts(sections: Dict[str,CourseSection], classrooms: Dict[str,Classroom], output_conflicts: List[Conflict]) -> List[Conflict]:
	"""
	Creates conflicts when enrollment exceeds max enrollment
	"""

	start_count = len(output_conflicts)
	for _,section in sections.items():
		enrollment = 0
		max_enrollment = 0
		try:
			enrollment = int(section.enrollment)
			max_enrollment = int(section.max_enrollment)
			if enrollment > max_enrollment:
				msg = f'{section.id}: Maximum enrollment of {max_enrollment} exceeded by current enrollment of {enrollment}.'
				output_conflicts = add_conflict_if_unique(output_conflicts, [section], [], section.rooms, msg)
		except:
			if enrollment and max_enrollment:
				print(f'conflict_factory.py: enrollment ({section.enrollment}) / max_enrollment ({section.max_enrollment}) couldn\'t be parsed to int for {section.id}.')
			elif section.id:
				msg = f'{section.id}: Invalid Enrollment Count and/or Maximum Enrollment. Please verify room can meet class capacity.'
				add_conflict_if_unique(output_conflicts, [section], [], section.rooms, msg)
				#print(f'conflict_factory.py: enrollment / max_enrollment couldn\'t be parsed to int for {section.id}.')
			else:
				print(f'conflict_factory.py: enrollment / max_enrollment couldn\'t be parsed to int.')
			continue
	return output_conflicts, len(output_conflicts) - start_count

#............................................................................................................
def add_conflict_if_unique(output_conflicts: List[Conflict],conflict_cluster: List[CourseSection],times: List[List[int]],rooms: List[str],msg: str = "") -> List[Conflict]:
	"""
	Adds a new conflict object only if no matching signature already exists
	"""

	# signature ignores minute values -> no duplicates across days
	id_signature      = tuple(sorted(sec.id for sec in conflict_cluster))
	rooms_signature   = tuple(sorted(rooms))
	conflict_key      = (id_signature, rooms_signature, msg)

	# look for an existing conflict with same signature
	for existing in output_conflicts:
		if getattr(existing, "_id", None) == conflict_key:
			# merge additional time ranges
			existing.times.extend(times)
			return output_conflicts

	# create new conflict object
	new_conflict = Conflict(conflict_cluster, times.copy(), rooms, msg)
	new_conflict._id = conflict_key
	output_conflicts.append(new_conflict)
	return output_conflicts

#............................................................................................................
def conflict_exclusions_generator(remote_section: CourseSection, sections: Dict[str,CourseSection]) -> List:
	"""
	Returns section IDs that should be excluded from conflict checks based on remote-learning or room TBA
	"""

	conflict_exclusion_list = []

	try:
		if 830 > int(remote_section.section) >= 820:
			if remote_section.id not in conflict_exclusion_list:
				conflict_exclusion_list.append(remote_section.id)

	except:
		print(f'remote_learning_conflict_avoidance: error')

	try:
		if remote_section.rooms == ['To Be Announced']:
			conflict_exclusion_list.append(remote_section.id)

	except:
		print(f'remote_learning_conflict_avoidance: error')

	return conflict_exclusion_list