class ValidationException(Exception):
    def __init__(self, keyError: str, message: str):
        self.code = 400
        self.keyError = keyError 
        self.message = message

class AlreadyExistException(Exception):
    def __init__(self, keyError: str, message: str):
        self.code = 409
        self.keyError = keyError 
        self.message = message

class NotFoundException(Exception):
    def __init__(self, keyError: str, message: str):
        self.code = 404
        self.keyError = keyError 
        self.message = message

class UnAuthorizedException(Exception):
    def __init__(self, keyError: str, message: str):
        self.code = 401
        self.keyError = keyError 
        self.message = message

