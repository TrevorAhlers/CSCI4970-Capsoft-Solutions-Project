from typing import Dict
from Model.Classroom import Classroom
from Model.CourseSection import CourseSection
import pandas as pd
import csv

#.......................................................................................................
def update_csv_with_room(input_file: str, output_file: str, sections: Dict[str, CourseSection]) -> None:
	"""
	Write to CSV with current CourseSection objs
	"""
	df = pd.read_csv(input_file, skiprows=2, header=0)
	# non NaN values... use empty strings
	df = df.fillna("")
	
	if "Room" in df.columns:
		df["Room"] = df["Room"].astype(str)
	else:
		df["Room"] = ""
	
	# update rooms as information allows
	for idx, row in df.iterrows():
		subject_code = str(row.get("Subject Code", "")).strip()
		catalog_number = str(row.get("Catalog Number", "")).strip()
		section_number = strip_decimal(str(row.get("Section #", "")).strip())
		key = f"{subject_code} {catalog_number}-{section_number}"
		
		if key in sections:
			rooms = sections[key].rooms
			# koin room numbers
			room_update_str = "; ".join(rooms)
			df.at[idx, "Room"] = room_update_str
	
	# write to csv
	df.to_csv(output_file, index=False, quoting=csv.QUOTE_ALL)

#.......................................................................................................
def strip_decimal(attribute: str) -> str:
	"""
	Removes any .0 values from numbers like 1.0
	"""
	if attribute.endswith(".0"):
		attribute = attribute[:-2]
		return attribute
	return attribute