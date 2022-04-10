class InvalidCommand(Exception):
    def __init__(self, command):
        self.message = f'Invalid command: {command}'

        super().__init__(self.message)

    def __str__(self):
        return self.message


class InvalidArgument(Exception):
    def __init__(self, argument):
        self.message = f'Invalid argument: {argument}'

        super().__init__(self.message)

    def __str__(self):
        return self.message


class TooManyArguments(Exception):
    def __init__(self):
        self.message = 'Too many arguments'

        super().__init__(self.message)

    def __str__(self):
        return self.message


class MissingArguments(Exception):
    def __init__(self, message):
        self.message = f'Missing argument(s): {message}'

        super().__init__(self.message)

    def __str__(self):
        return self.message

