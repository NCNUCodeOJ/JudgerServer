"""
define custom exception
"""
class CustomException(Exception):
    """
    custom exception base class
    """
    def __init__(self, message):
        super().__init__()
        self.message = message


class JudgeClientError(CustomException):
    """
    exception of judge client error
    """


class CompileError(CustomException):
    """
    exception of compile error
    """

class SPJCompileError(CustomException):
    """
    exception of spj compile error
    """
