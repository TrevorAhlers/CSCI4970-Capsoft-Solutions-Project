from typing import Dict, List
from Model.Classroom import Classroom, ClassroomEnum
from Model.CourseSection import CourseSection, CourseSectionEnum, combine_section_info
from Model.Conflict import Conflict

TIME_BETWEEN_CLASSES = 5

def build_conflicts(sections: Dict[str, CourseSection], classrooms: Dict[str, Classroom]) -> List[Conflict]:
	"""
    Builds a list of conflicts based on time, capacity, and parsing issues.

    This function combines time, capacity, and parsing conflicts into one list of Conflict objects.

    Args:
        sections (Dict[str, CourseSection]): A dictionary where keys are section IDs and values are CourseSection objects.
        classrooms (Dict[str, Classroom]): A dictionary where keys are classroom IDs and values are Classroom objects.

    Returns:
        List[Conflict]: A list of Conflict objects that represent detected conflicts.
    """
	"""
    Builds a list of conflicts based on time, capacity, and parsing issues.

    This function combines time, capacity, and parsing conflicts into one list of Conflict objects.

    Args:
        sections (Dict[str, CourseSection]): A dictionary where keys are section IDs and values are CourseSection objects.
        classrooms (Dict[str, Classroom]): A dictionary where keys are classroom IDs and values are Classroom objects.

    Returns:
        List[Conflict]: A list of Conflict objects that represent detected conflicts.
    """
	conflicts,time_count = build_time_conflicts(sections,classrooms)
	conflicts,capacity_count = build_capacity_conflicts(sections,classrooms,conflicts)
	conflicts,parse_count = build_parse_conflicts(sections,conflicts)
	print(f"conflict_factory.py: Built {len(conflicts)} Conflict objects.")
	print(f"conflict_factory.py: {time_count}/{len(conflicts)} were time conflicts.")
	print(f"conflict_factory.py: {capacity_count}/{len(conflicts)} were capacity conflicts.")
	print(f"conflict_factory.py: {parse_count}/{len(conflicts)} were parse conflicts.")
	return conflicts

def build_time_conflicts(sections: Dict[str, CourseSection], classrooms: Dict[str, Classroom]) -> List[Conflict]:
	"""
    Identifies and builds conflicts related to class times.

    This function checks for time overlaps between sections held in the same classroom, 
    considering a buffer time between class schedules.

    Args:
        sections (Dict[str, CourseSection]): A dictionary where keys are section IDs and values are CourseSection objects.
        classrooms (Dict[str, Classroom]): A dictionary where keys are classroom IDs and values are Classroom objects.

    Returns:
        List[Conflict]: A list of Conflict objects related to time conflicts.
    """
	"""
    Identifies and builds conflicts related to class times.

    This function checks for time overlaps between sections held in the same classroom, 
    considering a buffer time between class schedules.

    Args:
        sections (Dict[str, CourseSection]): A dictionary where keys are section IDs and values are CourseSection objects.
        classrooms (Dict[str, Classroom]): A dictionary where keys are classroom IDs and values are Classroom objects.

    Returns:
        List[Conflict]: A list of Conflict objects related to time conflicts.
    """

	output_conflicts = []
	conflict_exclusion = []
	
	for _, classroom in classrooms.items():
		classroom_conflicts = classroom.find_conflicts()

		# conflict_array: [section_id, start_time, end_time]
		for conflict_array in classroom_conflicts:
			conflict_cluster = []   # List[CourseSection]
			times = []              # [start, end]
			current_window = None   # span of conflict time
			
			i = 0
			n = len(conflict_array)
			while i < n:
				section_id = conflict_array[i]
				exclusion = conflict_exclusions_generator(sections[section_id], sections)
				if exclusion not in conflict_exclusion:
					conflict_exclusion += exclusion
				if sections[section_id].crosslistings_cleaned:
					for crosslisting in sections[section_id].crosslistings_cleaned:
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
					# Overlap? then add to conflict_cluster, add times and adjust conflict window
					if start_time <= current_window[1] + TIME_BETWEEN_CLASSES:
						conflict_cluster.append(sections[section_id])
						times.append([start_time, end_time])
						
						current_window[0] = min(current_window[0], start_time)
						current_window[1] = max(current_window[1], end_time)

					# No overlap? then create conflict object
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
				
				add_conflict_if_unique(output_conflicts, conflict_cluster, times, [classroom.room], "")

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

	return output_conflicts, len(output_conflicts)

def build_parse_conflicts(sections: Dict[str,CourseSection], output_conflicts: List[Conflict]) -> List[Conflict]:
	"""
    Identifies conflicts related to parsing meeting times or room assignments.

    This function checks for errors or uncertainties when parsing the room assignments and meeting times for each section.
    If any issues are found, a Conflict object is created.

    Args:
        sections (Dict[str, CourseSection]): A dictionary where keys are section IDs and values are CourseSection objects.
        output_conflicts (List[Conflict]): The list of existing conflicts to which new parse-related conflicts will be added.

    Returns:
        List[Conflict]: The updated list of Conflict objects, including any newly added parsing conflicts.
    """
	"""
    Identifies conflicts related to parsing meeting times or room assignments.

    This function checks for errors or uncertainties when parsing the room assignments and meeting times for each section.
    If any issues are found, a Conflict object is created.

    Args:
        sections (Dict[str, CourseSection]): A dictionary where keys are section IDs and values are CourseSection objects.
        output_conflicts (List[Conflict]): The list of existing conflicts to which new parse-related conflicts will be added.

    Returns:
        List[Conflict]: The updated list of Conflict objects, including any newly added parsing conflicts.
    """
	# We try to parse meeting times with their rooms. If we encounter uncertainty or failure
	# we create a conflict object.
	start_count = len(output_conflicts)
	for sec_id, section in sections.items():
		if section.rooms == ['TBD']:
			continue

		try:
			warn_msg = section.warning

			# If there's a warning for the user, due to uncertainty for room/meetings
			# parsing, then we create a conflict object for them to ignore or fix.
			if warn_msg and (section.rooms != ['TBD']):
				add_conflict_if_unique(output_conflicts, [section], [], section.rooms, warn_msg)

		# Worst case scenario where we fail to parse entirely and we pass the error onto the
		# user as a conflict object. Better than crashing for no reason...
		except ValueError as e:
			if (len(set(section.rooms)) == 1) and (section.rooms != ['TBD']):
				add_conflict_if_unique(output_conflicts, [section], [], section.rooms, str(e))
	return output_conflicts, len(output_conflicts) - start_count

def build_capacity_conflicts(sections: Dict[str,CourseSection], classrooms: Dict[str,Classroom], output_conflicts: List[Conflict]) -> List[Conflict]:
	"""
    Identifies conflicts related to class capacity.

    This function checks if the enrollment exceeds the room's maximum capacity. If it does, a Conflict object is created.

    Args:
        sections (Dict[str, CourseSection]): A dictionary where keys are section IDs and values are CourseSection objects.
        classrooms (Dict[str, Classroom]): A dictionary where keys are classroom IDs and values are Classroom objects.
        output_conflicts (List[Conflict]): The list of existing conflicts to which new capacity-related conflicts will be added.

    Returns:
        List[Conflict]: The updated list of Conflict objects, including any newly added capacity conflicts.
    """
	"""
    Identifies conflicts related to class capacity.

    This function checks if the enrollment exceeds the room's maximum capacity. If it does, a Conflict object is created.

    Args:
        sections (Dict[str, CourseSection]): A dictionary where keys are section IDs and values are CourseSection objects.
        classrooms (Dict[str, Classroom]): A dictionary where keys are classroom IDs and values are Classroom objects.
        output_conflicts (List[Conflict]): The list of existing conflicts to which new capacity-related conflicts will be added.

    Returns:
        List[Conflict]: The updated list of Conflict objects, including any newly added capacity conflicts.
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


def add_conflict_if_unique(output_conflicts: List[Conflict], conflict_cluster: List[CourseSection],
							times: List[List[int]], rooms: List[str], msg: str = "") -> List[Conflict]:
	"""
    Adds a new Conflict object to the list if it doesn't already exist.

    This function checks whether a conflict with the same signature already exists in the list of conflicts.
    If not, it adds the new Conflict object to the list.

    Args:
        output_conflicts (List[Conflict]): The list of existing Conflict objects.
        conflict_cluster (List[CourseSection]): The list of sections involved in the conflict.
        times (List[List[int]]): The list of start and end times for the conflict.
        rooms (List[str]): The list of rooms involved in the conflict.
        msg (str, optional): A message describing the conflict. Defaults to an empty string.

    Returns:
        List[Conflict]: The updated list of Conflict objects, including the newly added one if it was unique.
    """
	"""
    Adds a new Conflict object to the list if it doesn't already exist.

    This function checks whether a conflict with the same signature already exists in the list of conflicts.
    If not, it adds the new Conflict object to the list.

    Args:
        output_conflicts (List[Conflict]): The list of existing Conflict objects.
        conflict_cluster (List[CourseSection]): The list of sections involved in the conflict.
        times (List[List[int]]): The list of start and end times for the conflict.
        rooms (List[str]): The list of rooms involved in the conflict.
        msg (str, optional): A message describing the conflict. Defaults to an empty string.

    Returns:
        List[Conflict]: The updated list of Conflict objects, including the newly added one if it was unique.
    """
	
	# Canonical signature to compare all conflicts to detect duplicates
	conflict_entries = sorted((sec.id, t[0], t[1]) for sec, t in zip(conflict_cluster, times))
	rooms_signature = tuple(sorted(rooms))
	conflict_signature = (tuple(conflict_entries), rooms_signature, msg)
	new_conflict = Conflict(conflict_cluster, times, rooms, msg)

	# Override the object's conflict id with our canonical signature
	new_conflict._id = conflict_signature

	if not any(existing._id == new_conflict._id for existing in output_conflicts):
		output_conflicts.append(new_conflict)

	return output_conflicts

# Remote learning classes are still assigned to rooms. We just need to know which other 
# section its schedule mirrors. We can assign it to that matching section's room without 
# conflict. So we suppress the conflict here.
def conflict_exclusions_generator(remote_section: CourseSection, sections: Dict[str,CourseSection]) -> List:
	"""
    Generates a list of exclusions for remote learning sections.

    If a section is marked as remote or has conflicting attributes (such as 'TBD' for rooms), it will be excluded from conflict checks.

    Args:
        remote_section (CourseSection): The section that is remote or has conflict exclusions.
        sections (Dict[str, CourseSection]): A dictionary where keys are section IDs and values are CourseSection objects.

    Returns:
        List: A list of section IDs that should be excluded from conflict checks.
    """
	"""
    Generates a list of exclusions for remote learning sections.

    If a section is marked as remote or has conflicting attributes (such as 'TBD' for rooms), it will be excluded from conflict checks.

    Args:
        remote_section (CourseSection): The section that is remote or has conflict exclusions.
        sections (Dict[str, CourseSection]): A dictionary where keys are section IDs and values are CourseSection objects.

    Returns:
        List: A list of section IDs that should be excluded from conflict checks.
    """

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