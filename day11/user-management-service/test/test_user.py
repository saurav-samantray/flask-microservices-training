from email import header
import os
import unittest
import app
import server
import init_db

unittest.TestLoader.sortTestMethodsUsing = None

REGISTRATION_URL = '/api/register'
AUTH_URL = '/api/auth'
USERS_URL = '/api/users'

DB_NAME = 'user-management-UT.db';

class UserTest(unittest.TestCase):
    def setUp(self):
        #Initializing Table Schema
        init_db.initialize(DB_NAME)
        self.app = app.app
        self.app.testing = True
        #Pointing to UT database. Can also be handled via environment config
        self.app.config['DATABASE_URI'] = DB_NAME
        self.client = self.app.test_client()
        #Create a test user who's credential will be used for authentication
        registration_respone = self.client.post(REGISTRATION_URL, json = {"name": "test user", "email": "test@user.com", "age": 33, "password": "test"})
        print(f"Registration Response: {registration_respone.json}")
        #Generate auth token and save in a class level property
        auth_response = self.client.post(AUTH_URL, json={"email": "test@user.com", "password": "test"})
        self.access_token = auth_response.json['access_token']
    

    def test_get_users(self):
        response = self.client.get(USERS_URL, headers = {"Authorization": f"Bearer {self.access_token}"})
        self.assertEqual(response.status_code, 200)

    def test_create_user_success(self):
        response = self.client.post(USERS_URL, json = {"name": "new user", "email": "new@user.com", "age": 23, "password": "test"}, headers = {"Authorization": f"Bearer {self.access_token}"})
        print(f"API Response: {response.json}")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(response.json), 2)

    def test_create_user_error(self):
        response = self.client.post(USERS_URL, json = {"name": "new user", "email": "test@user.com", "age": 23, "password": "test"}, headers = {"Authorization": f"Bearer {self.access_token}"})
        self.assertEqual(response.status_code, 400)

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