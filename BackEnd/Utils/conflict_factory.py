from typing import Dict, List
from Model.Classroom import Classroom, ClassroomEnum
from Model.CourseSection import CourseSection, CourseSectionEnum, combine_section_info
from Model.Conflict import Conflict

TIME_BETWEEN_CLASSES = 5

def build_conflicts(sections: Dict[str, CourseSection], classrooms: Dict[str, Classroom]) -> List[Conflict]:

	output_conflicts = []
	conflict_exclusion = []
	
	for _, classroom in classrooms.items():
		classroom_conflicts = classroom.find_conflicts()
		for conflict_array in classroom_conflicts:
			conflict_cluster = []   # List[CourseSection]
			times = []              # [start, end]
			current_window = None   # span of conflict time
			
			# conflict_array format: [section_id, start_time, end_time]
			i = 0
			n = len(conflict_array)
			while i < n:
				section_id = conflict_array[i]
				exclusion = conflict_exclusions_generator(sections[section_id], sections)
				if exclusion not in conflict_exclusion:
					conflict_exclusion += exclusion
				if sections[section_id].crosslistings_cleaned:
					conflict_exclusion += sections[section_id].crosslistings_cleaned
					#print(section_id, "crosslist:",sections[section_id].crosslistings_cleaned)
				if section_id in conflict_exclusion:
					break
				start_time = conflict_array[i+1]
				end_time   = conflict_array[i+2]
				i += 3
				

				# New cluster
				if not conflict_cluster:
					conflict_cluster.append(sections[section_id])
					times.append([start_time, end_time])
					current_window = [start_time, end_time]
				else:
					# Overlap?
					if start_time <= current_window[1] + TIME_BETWEEN_CLASSES:
						conflict_cluster.append(sections[section_id])
						times.append([start_time, end_time])
						
						current_window[0] = min(current_window[0], start_time)
						current_window[1] = max(current_window[1], end_time)
					else:
						# Create Conflict obj
						add_conflict_if_unique(output_conflicts, conflict_cluster, times, [classroom.room])
						
						# New cluster
						conflict_cluster = [sections[section_id]]
						times = [[start_time, end_time]]
						current_window = [start_time, end_time]
			
			# If we have identified overlapping/conflicting time slots then they'll be in
			# the conflict cluster and we create a Conflict obj with all of them included.
			if conflict_cluster:
				add_conflict_if_unique(output_conflicts, conflict_cluster, times, [classroom.room])
		
		# We try to parse meeting times with their rooms. If we encounter uncertainty or failure
		# we create a conflict object.
		for sec_id, sec in sections.items():
			if sec.rooms == ['TBD']:
				continue
			meeting_times = sec.parsed_meetings

			try:
				warn_msg = sections[sec_id].warning

				# If there's a warning for the user, due to uncertainty for room/meetings
				# parsing, then we create a conflict object for them to ignore or fix.
				if warn_msg and (sec.rooms != ['TBD']):
					add_conflict_if_unique(output_conflicts, [sec], [], sec.rooms, warn_msg)

			# Worst case scenario where we fail to parse entirely and we pass the error onto the
			# user as a conflict object. Better than crashing for no reason...
			except ValueError as e:
				if (len(set(sec.rooms)) == 1) and (sec.rooms != ['TBD']):
					add_conflict_if_unique(output_conflicts, [sec], [], sec.rooms, str(e))

	output_conflicts = [
		conflict
		for conflict in output_conflicts
		if conflict.conflict_message or conflict.section_count >= 2
	]

	

	filtered_conflicts = [
		conflict
		for conflict in output_conflicts
		if conflict.section_count >= 2
	]
	output_conflicts = filtered_conflicts

	print(f"Built {len(output_conflicts)} Conflict objects.")
	return output_conflicts


def add_conflict_if_unique(output_conflicts: List[Conflict], conflict_cluster: List[CourseSection],
							times: List[List[int]], rooms: List[str], msg: str = "") -> None:
	
	# Canonical signature to compare all conflicts to detect duplicates
	conflict_entries = sorted((sec.id, t[0], t[1]) for sec, t in zip(conflict_cluster, times))
	rooms_signature = tuple(sorted(rooms))
	conflict_signature = (tuple(conflict_entries), rooms_signature)
	new_conflict = Conflict(conflict_cluster, times, rooms, msg)

	# Override the object's conflict id with our canonical signature
	new_conflict._id = conflict_signature

	if not any(existing._id == new_conflict._id for existing in output_conflicts):
		output_conflicts.append(new_conflict)

# Remote learning classes are still assigned to rooms. We just need to know which other 
# section its schedule mirrors. We can assign it to that matching section's room without 
# conflict. So we suppress the conflict here.
def conflict_exclusions_generator(remote_section: CourseSection, sections: Dict[str,CourseSection]):

	conflict_exclusion_list = []

	try:
		if 830 > int(remote_section.section) >= 820:
			if remote_section.id not in conflict_exclusion_list:
				conflict_exclusion_list.append(remote_section.id)

	except:
		print(f'remote_learning_conflict_avoidance: error')

	try:
		if remote_section.rooms == ['TBD']:
			conflict_exclusion_list.append(remote_section.id)

	except:
		print(f'remote_learning_conflict_avoidance: error')

	return conflict_exclusion_list