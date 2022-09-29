from app.exceptions import AddressNotFoundException
from .user_db import get_user_details

def get_addresses(conn, user_id):
	results = conn.execute('SELECT * FROM address where user_id = ?', (str(user_id),)).fetchall()
	results = [dict(row) for row in results]
	return results

def create_address(conn, address, user_id):
	get_user_details(conn, user_id)
	conn.execute('INSERT INTO address(address_line_1, city, state, pin, user_id) VALUES (?, ?, ?, ?, ?)',(address.address_line_1, address.city, address.state, address.pin, str(user_id)))

def get_address_details(conn, id, user_id):
	result = conn.execute('SELECT * FROM address where id = ? and user_id = ?', (str(id), str(user_id))).fetchone()
	if result is None:
		raise AddressNotFoundException(f"Address with ID [{id}] not found in database for user [{user_id}]", 404)
	return dict(result) if result != None else None

def update_address_details(conn, id, address, user_id):
	get_user_details(conn, user_id)
	conn.execute('UPDATE address SET address_line_1 = ?, city = ?, state = ?, pin = ? where id = ? and user_id = ? ', (address.address_line_1, address.city, address.state, address.pin, str(id), str(user_id)))

def delete_address(conn, id, user_id):
	get_user_details(conn, user_id)
	conn.execute('DELETE from address where id = ? and user_id = ?', (str(id, user_id)))       