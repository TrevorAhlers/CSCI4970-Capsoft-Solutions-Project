#####################################################################################
# 	Classroom Object Instantiation
# 
#
#....................................................................................

import csv
import os
import pandas as pd
import re
from typing import Dict, List, Optional
from Model.Classroom import Classroom, ClassroomEnum
from Model.CourseSection import CourseSection, CourseSectionEnum

def build_classrooms(filename: str, sections: Dict[str,CourseSection]) -> Dict[str, Classroom]:

    classroom_keys = []

    df = pd.read_csv(filename, header=0)
    classrooms: Dict[str, Classroom] = {}

    for _, row in df.iterrows():
        row_data: Dict[str, str] = {}
        for enum_col in ClassroomEnum:
            if enum_col.value in df.columns:
                cell_value = row[enum_col.value]
                cell_str = str(cell_value) if pd.notna(cell_value) else ""
                row_data[enum_col.value] = cell_str

        room_num_str = row_data.get("Room Number", "")
        tokens = room_num_str.split()
        key = tokens[-1] if tokens else room_num_str
        key = "Peter Kiewit Institute " + key
        print("Class:", key)

        cl = Classroom(row_data)
        classroom_keys.append(cl.room)

        # Default object values
        if not cl.seats:
            cl.seats = "N/A"
        if not cl.computer_count:
            cl.computer_count = "N/A"
        if not cl.displays:
            cl.displays = "N/A"
        if not cl.info_and_connectivity:
            cl.info_and_connectivity = "N/A"

        classrooms[key] = cl
    
    for _,section in sections.items():
        for section_room in section.rooms:
            if section_room not in classroom_keys:
                row_data = {
                    "Room Number": section_room,
                    "Seats": "N/A",
                    "Displays": "N/A",
                    "Computer Count": "N/A",
                    "Information and Connectivity": "N/A"
                }
                classrooms[section_room] = Classroom(row_data)

    print(f"Built {len(classrooms)} Classroom objects.")
    

    return classrooms