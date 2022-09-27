import unittest
import datetime
import time
import app
import init_db

unittest.TestLoader.sortTestMethodsUsing = None

REGISTRATION_URL = '/api/register'
AUTH_URL = '/api/auth'
REFRESH_URL = '/api/refresh'
USERS_URL = '/api/users'

DB_NAME = 'user-management-UT.db'

class AuthTest(unittest.TestCase):
    def setUp(self):
        #Initializing Table Schema
        init_db.initialize(DB_NAME)
        self.app = app.app
        self.app.testing = True
        #Pointing to UT database. Can also be handled via environment config
        self.app.config['DATABASE_URI'] = DB_NAME
        self.app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(seconds=5)
        self.client = self.app.test_client()
        #Create a test user who's credential will be used for authentication
        self.client.post(REGISTRATION_URL, json = {"name": "test user", "email": "test@user.com", "age": 33, "password": "test"})
        #Generate auth token and save in a class level property
        auth_response = self.client.post(AUTH_URL, json={"email": "test@user.com", "password": "test"})
        print(f"Authentication Response: {auth_response.status_code}")
        self.access_token = auth_response.json['access_token']
        self.refresh_token = auth_response.json['refresh_token']
    

    def test_get_auth_success(self):
        auth_response = self.client.post(AUTH_URL, json={"email": "test@user.com", "password": "test"})
        self.assertEqual(auth_response.status_code, 200)

    def test_get_auth_invalid_email_error(self):
        auth_response = self.client.post(AUTH_URL, json={"email": "test2@user.com", "password": "test"})
        self.assertEqual(auth_response.status_code, 400)

    def test_get_auth_invalid_password_error(self):
        auth_response = self.client.post(AUTH_URL, json={"email": "test@user.com", "password": "test123"})
        self.assertEqual(auth_response.status_code, 401)

    def test_auth_expiry_error(self):
        auth_response = self.client.post(AUTH_URL, json={"email": "test@user.com", "password": "test"})
        auth_token = auth_response.json['access_token']
        time.sleep(6)
        users_response = self.client.get(USERS_URL, headers = {"Authorization": f"Bearer {auth_token}"})
        self.assertEqual(users_response.status_code, 401)                       

    def test_register_user_success(self):
        response = self.client.post(REGISTRATION_URL, json = {"name": "test user2", "email": "test2@user.com", "age": 33, "password": "test2"})
        print(f"API Response: {response.json}")
        self.assertEqual(response.status_code, 201)

    def test_register_duplicate_user_error(self):
        response = self.client.post(REGISTRATION_URL, json = {"name": "test user", "email": "test@user.com", "age": 33, "password": "test2"})
        self.assertEqual(response.status_code, 400)        


    def test_refresh_token_success(self):
        response = self.client.post(REFRESH_URL, headers = {"Authorization": f"Bearer {self.refresh_token}"})
        self.assertEqual(response.status_code, 200)
        auth_token = response.json['access_token']
        users_response = self.client.get(USERS_URL, headers = {"Authorization": f"Bearer {auth_token}"})
        self.assertEqual(users_response.status_code, 200)


    def test_get_user_detail(self):
        response = self.client.get(USERS_URL+"/1", headers = {"Authorization": f"Bearer {self.access_token}"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json.get("email"), "test@user.com")

    def test_update_user_detail(self):
        response = self.client.put(USERS_URL+"/1", json= {"name": "test user", "email": "test2@user.com", "age": 33, "password": "test"}, headers = {"Authorization": f"Bearer {self.access_token}"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json.get("email"), "test2@user.com")

    def test_delete_user_detail(self):
        delete_response = self.client.delete(USERS_URL+"/1", headers = {"Authorization": f"Bearer {self.access_token}"})
        self.assertEqual(delete_response.status_code, 200)
        get_response = self.client.get(USERS_URL, headers = {"Authorization": f"Bearer {self.access_token}"})
        self.assertEqual(len(get_response.json), 0)    

if __name__ == "__main__":
    unittest.main() 