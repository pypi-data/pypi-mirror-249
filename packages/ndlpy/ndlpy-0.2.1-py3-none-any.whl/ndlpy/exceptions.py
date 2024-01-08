class ComputeError(Exception):
    """
    Exception raised for errors that occur during computation or processing in the application.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"ComputeError: {self.message}"
