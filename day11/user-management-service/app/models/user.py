from app import db
from sqlalchemy.orm import relationship

class User(db.Model):
    __tablename__ = 'UMS_USER'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    age = db.Column(db.Integer)
    password = db.Column(db.String(100))
    role = db.Column(db.String(50))
    addresses = relationship('Address', cascade='all, delete')
    
    def __init__(self, id, name, email, age, password, role):
        self.id = id
        self.name = name
        self.email = email
        self.age = age
        self.password = password   
        self.role = role     
    
    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'age': self.age,
            'role': self.role,
            'addresses': [address.to_json() for address in self.addresses]
        }

    @staticmethod
    def from_json(json_dct):
      return User(
        json_dct.get('id'), 
        json_dct['name'], 
        json_dct['email'], 
        json_dct['age'], 
        json_dct['password'],
        json_dct.get('role') if json_dct.get('role') is not None else 'USER')