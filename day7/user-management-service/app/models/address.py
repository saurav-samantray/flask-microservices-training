import json
class Address:
    def __init__(self, address_line_1, city, state, pin):
        self.address_line_1 = address_line_1
        self.city = city
        self.state = state
        self.pin = pin

    def to_json(self):
        return self.__dict__

    @staticmethod
    def from_json(json_dct):
      return Address(json_dct['address_line_1'],
                    json_dct['city'],
                    json_dct['state'],
                    json_dct['pin'])        