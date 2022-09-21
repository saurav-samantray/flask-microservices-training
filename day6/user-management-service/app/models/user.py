from json import JSONEncoder
import json

class User:
    def __init__(self, name, email, age, password):
        self.name = name
        self.email = email
        self.age = age
        self.password = password
    
    def to_json(self):
        return self.__dict__

    @staticmethod
    def from_json(json_dct):
      return User(json_dct['name'],
                    json_dct['email'],
                    json_dct['age'],
                    json_dct['password'])