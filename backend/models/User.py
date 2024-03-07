class User:
    PK = "id"
    TABLE = 'users'
    COLUMNS = ["id", "username", "image", "password"]
    UPDATE_COLUMNS = ["username", "image"]
    ON_CONFLICT = f"ON CONFLICT DO NOTHING"

    def __init__(
            self,
            id: int or None,
            username: str,
            image: str,
            password: str
    ):
        self.id = id
        self.username = username
        self.image = image
        self.password = password
