class Response:
    def __init__(self, data=None, errors: list or None = None, status: int = 200):
        self.data = data
        self.errors = errors
        self.status = status

    def out(self):
        return {"data": self.data} if self.data else {"errors": self.errors}
