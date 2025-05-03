import mysql.connector, json
from contextlib import contextmanager
from Model.User import User

DBconFIG = {
	'host': 'app-db-1.c6zkyqugocxt.us-east-1.rds.amazonaws.com',
	'user': 'capsoftdb',
	'password': 'csci4970',
	'database': 'maindb'
}

#...............................................
@contextmanager
def _con():
	"""
	Opens DB connection
	"""

	con = mysql.connector.connect(**DBconFIG)
	try:
		yield con
	finally:
		con.close()

#...............................................
def init_db():
	"""
	Creates the users table if needed
	"""

	with _con() as con:
		con.cursor().execute("""
			CREATE TABLE IF NOT EXISTS users(
				id  VARCHAR(255) PRIMARY KEY,
				obj JSON         NOT NULL
			)
		""")
		con.commit()

#...............................................
def dump(u: User) -> str:
	"""
	User object to JSON string for DB storage
	"""

	ws = {}
	if hasattr(u.workspace_state, 'to_json'):
		try:	ws = u.workspace_state.to_json()
		except Exception:	pass

	username, email = (u.user_id.split(':', 1) + [''])[:2]

	return json.dumps({
		"user_id":       username,
		"email":         email,
		"user_password": u.user_password,
		"workspace_state": ws
	})

#...............................................
def upsert(user: User):
	"""
	Inserts or updates a user row in the DB with the id
	"""

	with _con() as con:
		con.cursor().execute("""
			INSERT INTO users(id,obj)
			VALUES (%s,%s)
			ON DUPLICATE KEY UPDATE obj = VALUES(obj)
		""", (user.user_id, dump(user)))
		con.commit()

#...............................................
def fetch_one(uid: str) -> dict|None:
	"""
	Gets a user row from the DB by exact ID
	"""

	with _con() as con:
		cur = con.cursor()
		cur.execute("SELECT obj FROM users WHERE id = %s", (uid,))
		row = cur.fetchone()
		return json.loads(row[0]) if row else None

#...............................................
def get_by_username(username: str) -> dict|None:
	"""
	Returns user whose ID starts with the given username
	"""

	with _con() as con:
		cur = con.cursor()
		cur.execute("SELECT obj FROM users WHERE id LIKE %s LIMIT 1", (f"{username}:%",))
		row = cur.fetchone()
		return json.loads(row[0]) if row else None