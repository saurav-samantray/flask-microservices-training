from ..models.user import User
from app.exceptions import UserNotFoundException

def get_users(conn):
	results = conn.execute('SELECT id, name, email, age, created, role FROM user').fetchall()
	results = [dict(row) for row in results]
	return results

def create_user(conn, user):
	conn.execute('INSERT INTO user(name, email, age, password, role) VALUES (?, ?, ?, ?, ?)',
		(user.name, user.email, user.age, user.password, user.role))
	return get_user_details_from_email(conn, user.email)

def get_user_details(conn, id):
	result = conn.execute('SELECT id, name, email, age, created, role FROM user where id = ?', (str(id),)).fetchone()
	if result is None:
		raise UserNotFoundException(f"User with ID [{id}] not found in database", 404)
	return dict(result)

def get_user_details_from_email(conn, email):
	result = conn.execute('SELECT id, name, email, age, password, created, role FROM user where email = ?', (email,)).fetchone()
	return User.from_json(dict(result)) if result != None else None	

def update_user_details(conn, id, user):
	conn.execute('UPDATE user SET name = ?, email = ?, age = ?, password = ?, role = ? where id = ?', 
		(user.name, user.email, user.age, user.password, user.role, str(id)))

def delete_user(conn, id):
	conn.execute('DELETE from user where id = ?', (str(id)))

def delete_all_users(conn):
	conn.execute('DELETE from user')	