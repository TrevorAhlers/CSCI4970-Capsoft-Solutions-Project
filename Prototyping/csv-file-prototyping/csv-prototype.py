import csv
import os
import pandas as pd
import re
from math import nan
def main():
    base_dir = os.path.dirname(__file__)
    csv_file = os.path.join(base_dir, 'Fall2022.csv')
    # Some columns are blank when they should have a header title. This dictionary maps certain column indices with desired default header values.
    default_names = {0: "Course Name", 1: "Term", 2: "Term Code", 3: "Department Code"}
    headers = get_headers(csv_file, defaults=default_names)
	
    print("Column headers:", headers)
    #get_MeetingPattern(csv_file)
    getCourseCodeAndCourseTitle(csv_file)

def get_headers(filename, defaults=None):
	with open(filename, newline='') as csvfile:
		reader = csv.reader(csvfile)
		# Skip first two rows
		next(reader)
		next(reader)
		headers = next(reader)
		if defaults is None:
			defaults = {}
		# Replace blank headers with a default from the dict or fallback to "ColumnX"
		return [defaults.get(i, f"Column{i+1}") if not h.strip() else h for i, h in enumerate(headers)]

def get_classroom(filename):
	with open(filename,newline='') as csvfile:
		

		reader = pd.read_csv(csvfile, header=6)

		reader = reader.to_string()
		regex_pattern = r"Peter Kiewit Institute [0-9]{3}"
		rooms = re.findall(regex_pattern, reader)
		print(rooms)
		
def get_MeetingPattern(filename):
	with open(filename,'r',newline='') as csvfile:

		reader = pd.read_csv(csvfile)
		
		result=[]
		regex_pattern2= r'(M|MW|TR|F|T|W|R|MWF|S|MR) ([0-9]{1,2}(:[0-9]{2})?[AaPp][Mm])\-([0-9]{1,2}(:[0-9]{2})?[AaPp][Mm])(; (M|MW|TR|F|T|W|R|S) ([0-9]{1,2}(:[0-9]{2})?[AaPp][Mm])\-([0-9]{1,2}(:[0-9]{2})?[AaPp][Mm]))?'
		reader = reader['Meeting Pattern'].apply(str)
		print(reader)
		for i in reader:
			result.append(i)

		meeting_patterns = []
	
		for i in result:
			if re.search(regex_pattern2,i):
				meeting_patterns.append(i)
		
		print(meeting_patterns)
		print(len(meeting_patterns))



def getCourseCodeAndCourseTitle(filename):
	with open(filename,'r',newline='') as csvfile:
		result=[]
		regex_pattern= r'[A-Z]'
		reader = pd.read_csv(csvfile)
		
		result2 = dict(reader)
		print(result2)

		for i in reader['Course'].apply(str):
			result.append(i)

		course_code = []
		for i in result:
			if re.search(regex_pattern,i):
				course_code.append(i)

		print(course_code)

		

		for i in reader['Course Title'].apply(str):
			result.append(i)

		course_title = []
		for i in result:
			if re.search(regex_pattern,i):
				course_title.append(i)

		print(course_title)

	
		

if __name__ == "__main__":
    main()