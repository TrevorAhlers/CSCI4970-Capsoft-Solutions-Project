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

def build_classrooms(filename: str) -> Dict[str, Classroom]:
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

        cl = Classroom(row_data)
        if not cl.seats:
            cl.seats = "N/A"
        if not cl.computer_count:
            cl.computer_count = "N/A"
        if not cl.displays:
            cl.displays = "N/A"
        if not cl.info_and_connectivity:
            cl.info_and_connectivity = "N/A"
        classrooms[key] = cl

    print(f"Built {len(classrooms)} Classroom objects.")

    return classrooms