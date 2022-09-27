from flask_restful import Resource

class UsersSearchApi(Resource):
	decorators = []	#Add appropriate decorators
	def get(self):
		pass #Add logic to give full user details if accesed by a user with valid token else return just name and email

# Uncomment the below line by adding a valid url mapping for the user search API
#restful_api.add_resource(UsersSearchApi, '<valid-mapping>')