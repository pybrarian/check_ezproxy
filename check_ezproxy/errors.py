class ConfigError(Exception):
    def __init__(self, message=None):
        self.message = message

    def __str__(self):
        return ('There is an error in your configuration.'
                if self.message is None else self.message)
