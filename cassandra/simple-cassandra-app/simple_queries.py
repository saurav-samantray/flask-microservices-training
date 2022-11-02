from cassandra.cluster import Cluster

if __name__ == "__main__":
	cluster = Cluster(['localhost'],port=9042)
	
	#Connecting to the cluster 
	session = cluster.connect()
	print("-----------------------------------------------------------------------------------------------------")
	print(f"Connected to Cassandra cluster: {session}")

	#Creating a new keyspace
	keyspace = 'user_management_service'
	session.execute(f"create keyspace IF NOT EXISTS {keyspace} with replication={{'class': 'SimpleStrategy', 'replication_factor' : 1}};")
	print("-----------------------------------------------------------------------------------------------------")
	print(f"New keyspace: {keyspace} created successfully")


	#Setting the session keyspace
	session.set_keyspace(keyspace)
	print("-----------------------------------------------------------------------------------------------------")
	print(f"Setting the session to keyspace: {keyspace}")

	#Creating a table
	created_table_query = '''
			CREATE TABLE IF NOT EXISTS users (
			email              text,
			first_name              text,
			last_name              text,
			age              smallint,
			birth_city              text,	
			birth_state              text,
			hobbies 	list<text>,
			created_datetime          timestamp,
			PRIMARY KEY ((birth_state , birth_city), email)
			);
		 '''
	session.execute(created_table_query)
	print("-----------------------------------------------------------------------------------------------------")
	print("New Table users created successfully")

	#Insert Records into a table
	record1 = '''
			INSERT INTO users (email, first_name, last_name, age, birth_city, birth_state, hobbies, created_datetime)
			VALUES ('saurav@gmail.com', 'Saurav', 'Samantray', 33, 'Bhubaneswar', 'Odisha', ['reading', 'cycling'], toUnixTimestamp(now())
			);
			  '''
	record2 = '''
			INSERT INTO users (email, first_name, last_name, age, birth_city, birth_state, hobbies, created_datetime)
			VALUES ('manish@gmail.com', 'Manish', 'M', 24, 'Bhubaneswar', 'Odisha', ['Hiking', 'Boxing'], toUnixTimestamp(now())
			);
			  '''
	record3 = '''
			INSERT INTO users (email, first_name, last_name, age, birth_city, birth_state, hobbies, created_datetime)
			VALUES ('krishna@gmail.com', 'krishna', 'P', 42, 'Patna', 'Bihar', ['Coding', 'Cricket'], toUnixTimestamp(now())
			);
			  '''		
	session.execute(record1)
	session.execute(record2)
	session.execute(record3)
	print("-----------------------------------------------------------------------------------------------------")
	print("Inserted new records")

	#Fetch all the records from a table
	print("-----------------------------------------------------------------------------------------------------")
	print("Fetching all the records present in [users] table")
	rows = session.execute('SELECT * FROM users')
	for row in rows:
		#Accessing each data element from row
		print(row.email,row.first_name,row.last_name,row.age,row.birth_city,row.birth_state,row.created_datetime)
	print("-----------------------------------------------------------------------------------------------------")
	
	#Filtering records/Prepared statement
	print("-----------------------------------------------------------------------------------------------------")
	print("Fetching all the records from user table using Bhubaneswar as birth_city")
	user_lookup_stmt = session.prepare("SELECT * FROM users WHERE birth_city=? ALLOW FILTERING")
	rows = session.execute(user_lookup_stmt, ['Bhubaneswar'])
	for row in rows:
		#Accessing each data element from row
		print(row.email,row.first_name,row.last_name,row.age,row.birth_city,row.birth_state,row.created_datetime)	
	print("-----------------------------------------------------------------------------------------------------")


	#Updating records
	print("-----------------------------------------------------------------------------------------------------")
	user_fetch_stmt = session.prepare("SELECT * from users WHERE birth_state=? AND birth_city=? AND email=?")
	result = session.execute(user_fetch_stmt, ['Odisha', 'Bhubaneswar', 'saurav@gmail.com'])
	print(f"User before update: {result[0]}")
	print("Updatting records")
	user_update_stmt = session.prepare("UPDATE users SET age=? WHERE birth_state=? AND birth_city=? AND email=?")
	rows = session.execute(user_update_stmt, [30, 'Odisha', 'Bhubaneswar', 'saurav@gmail.com'])	
	result = session.execute(user_fetch_stmt, ['Odisha', 'Bhubaneswar', 'saurav@gmail.com'])
	print(f"User after update: {result[0]}")
	print("-----------------------------------------------------------------------------------------------------")

	#Deleting record
	print("-----------------------------------------------------------------------------------------------------")
	user_fetch_stmt = session.prepare("SELECT * from users WHERE birth_state=? AND birth_city=? AND email=?")
	result = session.execute(user_fetch_stmt, ['Odisha', 'Bhubaneswar', 'saurav@gmail.com'])
	print(f"User before update: {result.current_rows}")
	print("Deleting records")
	user_update_stmt = session.prepare("DELETE FROM users WHERE birth_state=? AND birth_city=? AND email=?")
	rows = session.execute(user_update_stmt, ['Odisha', 'Bhubaneswar', 'saurav@gmail.com'])	
	result = session.execute(user_fetch_stmt, ['Odisha', 'Bhubaneswar', 'saurav@gmail.com'])
	print(f"User after update: {result.current_rows}")
	print("-----------------------------------------------------------------------------------------------------")	