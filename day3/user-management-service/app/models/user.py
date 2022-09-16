from json import JSONEncoder
import json

class User:
    def __init__(self, name, email, age, password):
        self.name = name
        self.email = email
        self.age = age
        self.password = password
    
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)



# class UserEncoder(JSONEncoder):
#     def default(self, object):
#         if isinstance(object, User):
#             return object.__dict__

#         else:

#             # call base class implementation which takes care of

#             # raising exceptions for unsupported types

#             return json.JSONEncoder.default(self, object)