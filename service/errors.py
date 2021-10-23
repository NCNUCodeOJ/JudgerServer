class CustomException(Exception):
    def __init__(self, message):
        super().__init__()
        self.message = message


class JudgeClientError(CustomException):
    pass


class CompileError(CustomException):
    pass

class SPJCompileError(CustomException):
    pass