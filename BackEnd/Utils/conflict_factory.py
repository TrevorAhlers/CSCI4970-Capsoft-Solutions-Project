from typing import Dict, List
from Model.Classroom import Classroom, ClassroomEnum
from Model.CourseSection import CourseSection, CourseSectionEnum, combine_section_info
from Model.Conflict import Conflict

TIME_BETWEEN_CLASSES = 5

def add_conflict_if_unique(output_conflicts: List[Conflict], conflict_cluster: List[CourseSection],
	times: List[List], rooms: List[str], msg: str = "") -> None:
	
	new_conflict = Conflict(conflict_cluster, times, rooms, msg)
	if not any(existing.id == new_conflict._id for existing in output_conflicts):
		output_conflicts.append(new_conflict)

def build_conflicts(sections: Dict[str, CourseSection], classrooms: Dict[str, Classroom]) -> List[Conflict]:
	output_conflicts = []
	
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
			meeting_times = sec.parsed_meetings

			try:
				combined, warn_msg = combine_section_info(sec_id, meeting_times, sec.rooms)

				# If there's a warning for the user, due to uncertainty for room/meetings
				# parsing, then we create a conflict object for them to ignore or fix.
				if warn_msg:
					add_conflict_if_unique(output_conflicts, [sec], [], sec.rooms, warn_msg)

			# Worst case scenario where we fail to parse entirely and we pass the error onto the
			# user as a conflict object. Better than crashing for no reason...
			except ValueError as e:
				add_conflict_if_unique(output_conflicts, [sec], [], sec.rooms, str(e))

	print(f"Built {len(output_conflicts)} Conflict objects.")
	
	return output_conflicts
