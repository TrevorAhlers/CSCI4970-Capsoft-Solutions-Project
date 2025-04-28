# Data/assignment_file_repo.py
import pickle, mysql.connector
from contextlib import contextmanager
from Model.AssignmentFile import AssignmentFile

DB_CONFIG = {
	'host':     'app-db-1.c6zkyqugocxt.us-east-1.rds.amazonaws.com',
	'user':     'capsoftdb',
	'password': 'csci4970',
	'database': 'maindb'
}

@contextmanager
def get_con():
	con = mysql.connector.connect(**DB_CONFIG)
	try:	yield con
	finally:	con.close()

def init_db():
	with get_con() as con:
		con.cursor().execute("""
			CREATE TABLE IF NOT EXISTS assignment_files(
				filename VARCHAR(255) PRIMARY KEY,
				obj      LONGBLOB      NOT NULL
			)
		""")
		con.commit()

def save(af: AssignmentFile):
	with get_con() as con:
		con.cursor().execute("""
			INSERT INTO assignment_files(filename,obj)
			VALUES (%s,%s)
			ON DUPLICATE KEY UPDATE obj = VALUES(obj)
		""", (af._filename, pickle.dumps(af)))
		con.commit()

def list_assignment_files():
	with get_con() as con:
		cur = con.cursor()
		cur.execute("SELECT filename FROM assignment_files ORDER BY filename")
		return cur.fetchall()
