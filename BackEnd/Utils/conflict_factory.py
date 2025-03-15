from typing import Dict, List
from Model.Classroom import Classroom, ClassroomEnum
from Model.CourseSection import CourseSection, CourseSectionEnum
from Model.Conflict import Conflict

TIME_BETWEEN_CLASSES = 5

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
				
				# New conflict cluster
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
						# Create Conflict object
						conflict_obj = Conflict(conflict_cluster, times)
						output_conflicts.append(conflict_obj)
						
						# Start a new cluster
						conflict_cluster = [sections[section_id]]
						times = [[start_time, end_time]]
						current_window = [start_time, end_time]
			
			# If any sections remain in the current cluster, create a Conflict object
			if conflict_cluster:
				conflict_obj = Conflict(conflict_cluster, times)
				output_conflicts.append(conflict_obj)
		
	print(f"Built {len(output_conflicts)} Conflict objects.")
	
	return output_conflicts
