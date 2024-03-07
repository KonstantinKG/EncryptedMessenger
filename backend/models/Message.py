from datetime import datetime


class Message:
    TABLE = 'messages'
    COLUMNS = ["id", "content", "file", "user_id", "chat_id"]
    ON_CONFLICT = f"ON CONFLICT DO NOTHING"

    def __init__(
            self,
            id: str,
            content: str,
            file: str,
            user_id: str,
            chat_id: str,
            relevance: datetime
    ):
        self.id = id
        self.content = content
        self.file = file
        self.user_id = user_id
        self.chat_id = chat_id
        self.relevance = relevance
