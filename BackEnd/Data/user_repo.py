import mysql.connector, json
from contextlib import contextmanager
from Model.User import User

DB_CONFIG = {
	'host': 'app-db-1.c6zkyqugocxt.us-east-1.rds.amazonaws.com',
	'user': 'capsoftdb',
	'password': 'csci4970',
	'database': 'maindb'
}

@contextmanager
def _con():
	con = mysql.connector.connect(**DB_CONFIG)
	try:
		yield con
	finally:
		con.close()

def init_db():
	with _con() as con:
		con.cursor().execute("""
			CREATE TABLE IF NOT EXISTS users(
				id  VARCHAR(255) PRIMARY KEY,
				obj JSON         NOT NULL
			)
		""")
		con.commit()

def _dump(u: User) -> str:
	"""
	Create the JSON payload stored in the `obj` column.

	* id column (written elsewhere) is "username:email"
	* inside JSON we keep them separate:
	    { "user_id": "username",
	      "email"  : "username@example.com",
	      "user_password": "…",
	      "workspace_state": {...} }
	"""
	ws = {}
	if hasattr(u.workspace_state, 'to_json'):
		try:	ws = u.workspace_state.to_json()
		except Exception:	pass

	# split the id that came in as "username:email"
	username, email = (u.user_id.split(':', 1) + [''])[:2]

	return json.dumps({
		"user_id":       username,
		"email":         email,
		"user_password": u.user_password,
		"workspace_state": ws
	})

def upsert(user: User):
	with _con() as con:
		con.cursor().execute("""
			INSERT INTO users(id,obj)
			VALUES (%s,%s)
			ON DUPLICATE KEY UPDATE obj = VALUES(obj)
		""", (user.user_id, _dump(user)))
		con.commit()

def fetch_one(uid: str) -> dict|None:
	with _con() as con:
		cur = con.cursor()
		cur.execute("SELECT obj FROM users WHERE id = %s", (uid,))
		row = cur.fetchone()
		return json.loads(row[0]) if row else None

def get_by_username(username: str) -> dict|None:
	"""
	Return the JSON row whose id starts with 'username:'.
	If duplicates ever exist we return the first.
	"""
	with _con() as con:
		cur = con.cursor()
		cur.execute("SELECT obj FROM users WHERE id LIKE %s LIMIT 1", (f"{username}:%",))
		row = cur.fetchone()
		return json.loads(row[0]) if row else None