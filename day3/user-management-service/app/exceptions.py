from werkzeug.exceptions import HTTPException

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