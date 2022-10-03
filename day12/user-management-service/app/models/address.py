from app import db
class Address(db.Model):
    __tablename__ = 'UMS_USER_ADDRESS'
    id = db.Column(db.Integer, primary_key=True)
    address_line_1 = db.Column(db.String(100))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    pin = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('UMS_USER.id'))

    def __init__(self, address_line_1, city, state, pin):
        self.address_line_1 = address_line_1
        self.city = city
        self.state = state
        self.pin = pin

    def to_json(self):
        return {
            'id': self.id,
            'address_line_1': self.address_line_1,
            'city': self.city,
            'state': self.state,
            'pin': self.pin,
            'user_id': self.user_id
        }

    @staticmethod
    def from_json(json_dct):
      return Address(json_dct['address_line_1'],
                    json_dct['city'],
                    json_dct['state'],
                    json_dct['pin'])        