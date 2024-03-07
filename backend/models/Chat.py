class Chat:
    PK = "id"
    TABLE = 'chats'
    COLUMNS = ["id", "name", "image", "owner_id"]
    UPDATE_COLUMNS = ["name", "image"]
    ON_CONFLICT = f"ON CONFLICT DO NOTHING"

    def __init__(
            self,
            id: str,
            name: str,
            image: str,
            owner_id: str
    ):
        self.id = id
        self.name = name
        self.image = image
        self.owner_id = owner_id
