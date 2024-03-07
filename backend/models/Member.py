class Member:
    TABLE = 'members'
    COLUMNS = ["chat_id", "user_id"]
    ON_CONFLICT = f"ON CONFLICT DO NOTHING"

    def __init__(
            self,
            chat_id: str,
            user_id: str,
    ):
        self.chat_id = chat_id
        self.user_id = user_id
