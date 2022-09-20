import json
class Address:
    def __init__(self, address_line_1, city, state, pin):
        self.address_line_1 = address_line_1
        self.city = city
        self.state = state
        self.pin = pin

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

    @staticmethod
    def from_json(json_dct):
      return Address(json_dct['address_line_1'],
                    json_dct['city'],
                    json_dct['state'],
                    json_dct['pin'])        