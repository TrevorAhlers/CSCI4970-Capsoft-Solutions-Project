import mysql.connector
import json

def create_user_table_if_not_exists(host: str, user: str, password: str, database: str) -> None:
	db = mysql.connector.connect(
		host=host,
		user=user,
		password=password,
		database=database
	)
	cursor = db.cursor()

	create_table_query = """
	CREATE TABLE IF NOT EXISTS users (
		user_id VARCHAR(255) PRIMARY KEY,
		user_password VARCHAR(255) NOT NULL,
		workspace_state JSON
	)
	"""
	cursor.execute(create_table_query)
	db.commit()
	cursor.close()
	db.close()


def insert_or_update_user(
	host: str,
	user: str,
	password: str,
	database: str,
	user_id: str,
	user_password: str,
	workspace_state_obj
) -> None:
	db = mysql.connector.connect(
		host=host,
		user=user,
		password=password,
		database=database
	)
	cursor = db.cursor()

	workspace_state_json = json.dumps(workspace_state_obj)

	insert_query = """
	INSERT INTO users (user_id, user_password, workspace_state)
	VALUES (%s, %s, CAST(%s AS JSON))
	ON DUPLICATE KEY UPDATE
		user_password = VALUES(user_password),
		workspace_state = VALUES(workspace_state)
	"""
	cursor.execute(insert_query, (user_id, user_password, workspace_state_json))
	db.commit()
	cursor.close()
	db.close()


def get_user_from_db(host: str, user: str, password: str, database: str, user_id: str):
	db = mysql.connector.connect(
		host=host,
		user=user,
		password=password,
		database=database
	)
	cursor = db.cursor(dictionary=True)

	query = "SELECT user_id, user_password FROM users WHERE user_id = %s"
	cursor.execute(query, (user_id,))
	result = cursor.fetchone()

	cursor.close()
	db.close()

	return result
