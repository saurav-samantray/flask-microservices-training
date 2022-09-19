from werkzeug.exceptions import HTTPException

class ToDoAlreadyExists(HTTPException):
    def __init__(self, message="ToDo Item with the name already exists", code=400):
        self.message = message
        self.code = code
        super().__init__()

class ToDoDoesnNotExists(HTTPException):
    def __init__(self, message="ToDo Item with the id doesn't exists", code=400):
        self.message = message
        self.code = code
        super().__init__()