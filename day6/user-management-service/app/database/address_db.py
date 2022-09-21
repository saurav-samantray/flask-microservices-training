from app.exceptions import AddressNotFoundException

def get_addresses(conn):
	results = conn.execute('SELECT * FROM address').fetchall()
	results = [dict(row) for row in results]
	return results

def create_address(conn, address):
	conn.execute('INSERT INTO address(address_line_1, city, state, pin) VALUES (?, ?, ?, ?)',(address.address_line_1, address.city, address.state, address.pin))

def get_address_details(conn, id):
	result = conn.execute('SELECT * FROM address where id = ?', (str(id))).fetchone()
	if result is None:
		raise AddressNotFoundException(f"Address with ID [{id}] not found in database", 404)
	return dict(result) if result != None else None

def update_address_details(conn, id, address):
	conn.execute('UPDATE user SET address_line_1 = ?, city = ?, state = ?, pin = ? where id = ?', (address.address_line_1, address.city, address.state, address.pin, str(id)))

def delete_address(conn, id):
	conn.execute('DELETE from address where id = ?', (str(id)))       