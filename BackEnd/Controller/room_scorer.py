#####################################################################################
# 	Room Scorer
#
#	Assigns scores to rooms for each course-section, so we know historically which
#	assignments have worked in the past, and how often.
#
#....................................................................................

import os
import pandas as pd
from typing import Dict, List, Optional
from Model.CourseSection import CourseSection, CourseSectionEnum

float_headers = [
	"Section #",
	"Credit Hrs Min",
	"Credit Hrs",
	"Enrollment",
	"Maximum Enrollment",
	"Wait Cap",
	"Rm Cap Request",
	"Cross-list Maximum",
	"Cross-list Wait Cap",
	"Cross-list Rm Cap Request",
]

def split_rooms(room):
	if not isinstance(room, str):
		room = str(room) if pd.notna(room) else ""
	if ';' in room:
		return [r for r in room.split("; ") if r != 'Partially Online']
	return [room] if room else []



import os
import pandas as pd
from typing import Dict, List

def split_rooms(room):
	if not isinstance(room, str):
		room = str(room) if pd.notna(room) else ""
	if ';' in room:
		return [r for r in room.split('; ') if r != 'Partially Online']
	return [room] if room else []


def map_assignment_freq(filenames: List[str]) -> Dict[str, Dict[str, int]]:
	output_map: Dict[str, Dict[str, int]] = {}

	for filename in filenames:
		base_dir = os.path.dirname(__file__)
		input_csv_file = os.path.join(os.path.dirname(base_dir), 'Files', filename)
		df = pd.read_csv(input_csv_file, skiprows=2, header=0)

		for _, row in df.iterrows():
			subj = str(row.get("Subject Code", ""))
			num = str(row.get("Catalog Number", ""))
			section_str = make_int_str(str(row.get("Section #", "")))
			key = f"{subj} {num}-{section_str}"

			ss_room = row.get("Room", "")
			rooms = split_rooms(ss_room)

			if key not in output_map:
				output_map[key] = {}

			for room in rooms:
				if "Peter Kiewit Institute" in room:
					freq = output_map[key].get(room, 0)
					output_map[key][room] = freq + 1

	return output_map



def make_int_str(attribute: str) -> str:
	return attribute[:-2] if attribute.endswith(".0") else attribute