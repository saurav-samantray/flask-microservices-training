from app.exceptions import UserNotFoundException

def get_users(conn):
	results = conn.execute('SELECT id, name, email, age, created FROM user').fetchall()
	results = [dict(row) for row in results]
	return results

def create_users(conn, user):
	conn.execute('INSERT INTO user(name, email, age, password) VALUES (?, ?, ?, ?)',(user.name, user.email, user.age, user.password))

def get_user_details(conn, id):
	result = conn.execute('SELECT id, name, email, age, created FROM user where id = ?', (str(id))).fetchone()
	if result is None:
		raise UserNotFoundException(f"User with ID [{id}] not found in database", 404)
	return dict(result) if result != None else None

def update_user_details(conn, id, user):
	conn.execute('UPDATE user SET name = ?, email = ?, age = ?, password = ? where id = ?', (user.name, user.email, user.age, user.password, str(id)))

def delete_user(conn, id):
	conn.execute('DELETE from user where id = ?', (str(id)))        