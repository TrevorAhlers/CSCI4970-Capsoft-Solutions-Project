import csv
import os

def remove_top_rows(csv_file):
	with open(csv_file, newline='') as infile:
		rows = list(csv.reader(infile))
	# Get cell A1 and A2 (first cell of row 1 and row 2)
	cell_a1 = rows[0][0] if rows and rows[0] else ""
	cell_a2 = rows[1][0] if len(rows) > 1 and rows[1] else ""
	# Write back the file starting from row 3
	with open(csv_file, 'w', newline='') as outfile:
		writer = csv.writer(outfile)
		writer.writerows(rows[2:])
	return cell_a1, cell_a2

def get_headers(filename, defaults=None):
	with open(filename, newline='') as csvfile:
		reader = csv.reader(csvfile)
		headers = next(reader)
		if defaults is None:
			defaults = {}
		return [defaults.get(i, f"Column{i+1}") if not h.strip() else h for i, h in enumerate(headers)]

def main():
	base_dir = os.path.dirname(__file__)
	csv_file = os.path.join(base_dir, 'Fall2022.csv')
	# Remove top two rows and extract A1 and A2
	a1, a2 = remove_top_rows(csv_file)
	print("Cell A1:", a1)
	print("Cell A2:", a2)
	
	default_names = {0: "Course Name", 1: "Term", 2: "Term Code", 3: "Department Code"}
	headers = get_headers(csv_file, defaults=default_names)
	print("Column headers:", headers)

if __name__ == "__main__":
	main()
