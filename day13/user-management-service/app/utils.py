from .models.user import User

def create_admin_user(flask_bcrypt, db, user):
		existing_user = User.query.filter_by(email=user.email).first()
		if existing_user is not None:
			print(f"Admin User [{existing_user.email}] already exits. Skipping creation on startup")
			return
		user.password = flask_bcrypt.generate_password_hash(user.password).decode('utf-8')
		db.session.add(user)
		db.session.commit()
		print(f"Successfully Created admin user [{user.email}]")