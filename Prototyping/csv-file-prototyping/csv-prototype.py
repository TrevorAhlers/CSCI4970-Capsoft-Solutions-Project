import csv
import os

def main():
    base_dir = os.path.dirname(__file__)
    csv_file = os.path.join(base_dir, 'Fall2022.csv')
    # Some columns are blank when they should have a header title. This dictionary maps certain column indices with desired default header values.
    default_names = {0: "Course Name", 1: "Term", 2: "Term Code", 3: "Department Code"}
    headers = get_headers(csv_file, defaults=default_names)
    print("Column headers:", headers)

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

if __name__ == "__main__":
    main()