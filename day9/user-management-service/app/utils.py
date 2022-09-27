from .database import get_db_connection, commit_and_close_db_connection
from .database.user_db import get_user_details_from_email
from .database import user_db

def create_admin_user(flask_bcrypt, user):
		conn = get_db_connection()
		existing_user = get_user_details_from_email(conn, user.email)
		if existing_user is not None:
			print(f"Admin User [{existing_user.email}] already exits. Skipping creation on startup")
			return
		user.password = flask_bcrypt.generate_password_hash(user.password).decode('utf-8')
		user_db.create_user(conn, user)
		commit_and_close_db_connection(conn)    
		print(f"Successfully Created admin user [{user.email}]")