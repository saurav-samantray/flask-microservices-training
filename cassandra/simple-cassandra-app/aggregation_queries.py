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

	##
	## Aggregation queries
	##
	sum_query = 'SELECT sum(age) as total_age FROM users'
	result = session.execute(sum_query)
	print("-----------------------------------------------------------------------------------------------------")
	print(f"Sum of all the ages: {result[0].total_age}")


	## Implement the COUNT, MAX, MIN and AVG query