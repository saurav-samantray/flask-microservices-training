from werkzeug.exceptions import HTTPException

class InvalidUserPayload(HTTPException):
    def __init__(self, message="User payload has invalid input", code=400):
        self.message = message
        self.code = code
        super().__init__()

class UserExistsException(HTTPException):
    def __init__(self, message="User already exists in the DB", code=400):
        self.message = message
        self.code = code
        super().__init__()

class UserNotFoundException(HTTPException):
    def __init__(self, message="User not found in the DB", code=400):
        self.message = message
        self.code = code
        super().__init__()



class InvalidAddressPayload(HTTPException):
    def __init__(self, message="Address payload has invalid input", code=400):
        self.message = message
        self.code = code
        super().__init__()

class AddressNotFoundException(HTTPException):
    def __init__(self, message="Address not found in the DB", code=400):
        self.message = message
        self.code = code
        super().__init__()   