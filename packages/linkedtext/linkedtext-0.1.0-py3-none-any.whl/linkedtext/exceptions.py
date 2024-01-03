"""
Exceptions
"""


class EmptyString(Exception):
    def __init__(self, message: str = None):
        if message is None:
            self.message = 'Empty string.'
        else:
            self.message = message
        super().__init__(self.message)


class FileNotFound(Exception):
    def __init__(self, message: str = None):
        if message is None:
            self.message = 'File not Found!'
        else:
            self.message = message
        super().__init__(self.message)


class ArgumentError(Exception):
    def __init__(self, argument_error: str = None):
        if argument_error is not None:
            self.message = f'Bad argument, use the `{argument_error}` parameter for the content you are using.'
        else:
            self.message = 'No argument given.'
        super().__init__(self.message)
