import asyncpg
from logging import Logger
from asyncpg import Connection
from models import User, Member, Chat, Message


class Database:
    def __init__(self, config: dict, logger: Logger):
        self._config = config
        self._logger = logger
        self._pool = None

    async def create_connection(self) -> Connection:
        return await asyncpg.connect(
            user=self._config['connection']['user'],
            host=self._config['connection']['host'],
            port=self._config['connection']['port'],
            database=self._config['connection']['database'],
            password=self._config['connection']['password']
        )

    async def insert(self, models: list):
        model_type = type(models[0])
        column_names = ', '.join(model_type.COLUMNS)
        placeholders = ', '.join(['$' + str(i) for i in range(1, len(model_type.COLUMNS) + 1)])
        query = f'''INSERT INTO {self._config['connection']['schema']}.{model_type.TABLE} ({column_names}) VALUES ({placeholders}) {model_type.ON_CONFLICT};'''
        data = [[model.__dict__.get(col) for col in model_type.COLUMNS] for model in models]

        conn = await self.create_connection()
        await conn.executemany(query, data)

    async def update(self, model):
        placeholders = ', '.join([f"{col} = ${i+1}" for i, col in enumerate(model.UPDATE_COLUMNS)])
        query = f'''UPDATE {model.TABLE} SET {placeholders} WHERE {model.PK} = '{model.__dict__.get(model.PK)}';'''
        data = [model.__dict__.get(col) for col in model.UPDATE_COLUMNS]

        conn = await self.create_connection()
        await conn.execute(query, *data)

    async def is_username_taken(self, username: str):
        query = f'''SELECT id FROM {User.TABLE} WHERE username='{username}';'''
        conn = await self.create_connection()
        row = await conn.fetchrow(query)
        return row

    async def get_user(self, id: str) -> User or None:
        query = f'''SELECT * FROM {User.TABLE} WHERE id='{id}';'''
        conn = await self.create_connection()
        row = await conn.fetchrow(query)
        return self.build_user(row)

    async def get_users(self, offset: int, limit: int) -> User or None:
        query = f'''SELECT * FROM {User.TABLE} OFFSET {offset} LIMIT {limit};'''
        conn = await self.create_connection()
        rows = await conn.fetch(query)
        return [self.build_user(row) for row in rows]

    async def get_users_count(self) -> User or None:
        query = f'''SELECT count(*) FROM {User.TABLE};'''
        conn = await self.create_connection()
        row = await conn.fetchrow(query)
        return row[0]

    async def get_chat_users(self, chat_id: str) -> list[User]:
        query = f'''
            SELECT 
                s.id,
                s.username,
                s.image,
                s.password
            FROM {Member.TABLE} m
            INNER JOIN {User.TABLE} s ON m.user_id=s.id
            WHERE chat_id='{chat_id}';
        '''
        conn = await self.create_connection()
        rows = await conn.fetch(query)
        return [self.build_user(row) for row in rows]

    async def get_chat_users_ids(self, chat_id: str, except_user_id: str) -> list[str]:
        query = f'''
            SELECT user_id FROM {Member.TABLE} m WHERE m.chat_id='{chat_id}' AND m.user_id != '{except_user_id}';
        '''
        conn = await self.create_connection()
        rows = await conn.fetch(query)
        return [row[0] for row in rows]

    async def get_user_by_username(self, username: str) -> User or None:
        query = f'''SELECT * FROM {User.TABLE} WHERE username='{username}';'''
        conn = await self.create_connection()
        row = await conn.fetchrow(query)
        return self.build_user(row)

    async def delete(self, model):
        query = f'''DELETE FROM {model.TABLE} WHERE id='{model.__dict__.get(model.PK)}';'''
        conn = await self.create_connection()
        await conn.execute(query)

    async def get_chat(self, id: str, user_id: str) -> User or None:
        query = f'''
            SELECT
                c.id,
                c.name,
                c.image,
                c.owner_id
            FROM {Member.TABLE} m
            INNER JOIN {Chat.TABLE} c ON c.id = m.chat_id
            WHERE m.user_id='{user_id}' AND c.id = '{id}';
        '''
        conn = await self.create_connection()
        row = await conn.fetchrow(query)
        return self.build_chat(row)

    async def get_chats(self, user_id: str, offset: int, limit: int) -> list[Chat]:
        query = f'''
            SELECT
                c.id,
                c.name,
                c.image,
                c.owner_id
            FROM {Member.TABLE} m
            INNER JOIN {Chat.TABLE} c ON c.id = m.chat_id
            WHERE m.user_id='{user_id}'
            ORDER BY relevance DESC 
            OFFSET {offset}
            LIMIT {limit};
        '''
        conn = await self.create_connection()
        rows = await conn.fetch(query)
        return [self.build_chat(row) for row in rows]

    async def get_chats_count(self, user_id: str) -> int:
        query = f'''
            SELECT count(*) FROM {Member.TABLE} m
            INNER JOIN {Chat.TABLE} c ON c.id = m.chat_id
            WHERE m.user_id='{user_id}';
        '''
        conn = await self.create_connection()
        row = await conn.fetchrow(query)
        return row[0]

    async def get_chat_messages(self, chat_id: str, offset: int, limit: int) -> list[Message]:
        query = f'''
            SELECT
                id,
                content,
                file,
                user_id,
                chat_id,
                relevance
            FROM {Message.TABLE} m
            WHERE m.chat_id='{chat_id}'
            ORDER BY relevance DESC
            OFFSET {offset}
            LIMIT {limit};
        '''
        conn = await self.create_connection()
        rows = await conn.fetch(query)
        return [self.build_message(row) for row in rows]

    async def get_chat_messages_count(self, chat_id) -> int:
        query = f'''SELECT count(*) FROM {Message.TABLE} m WHERE m.chat_id='{chat_id}';'''
        conn = await self.create_connection()
        row = await conn.fetchrow(query)
        return row[0]

    async def search_users(self, query: str, offset: int, limit: int) -> list[User]:
        query = f'''
            SELECT * FROM {User.TABLE} 
            WHERE username ilike '%{query}%'
            OFFSET {offset}
            LIMIT {limit};
        '''
        conn = await self.create_connection()
        rows = await conn.fetch(query)
        return [self.build_user(row) for row in rows]

    async def search_users_count(self, query: str) -> int:
        query = f'''SELECT count(*) FROM {User.TABLE} WHERE username ilike '%{query}%';'''
        conn = await self.create_connection()
        row = await conn.fetchrow(query)
        return row[0]

    async def search_chats(self, query: str, offset: int, limit: int) -> list[Chat]:
        query = f'''
            SELECT * FROM {Chat.TABLE}
            WHERE name ilike '%{query}%'
            OFFSET {offset}
            LIMIT {limit};
        '''
        conn = await self.create_connection()
        rows = await conn.fetch(query)
        return [self.build_chat(row) for row in rows]

    async def search_chats_count(self, query: str) -> int:
        query = f'''SELECT count(*) FROM {Chat.TABLE} WHERE name ilike '%{query}%';'''
        conn = await self.create_connection()
        row = await conn.fetchrow(query)
        return row[0]

    async def search_messages(self, chat_id: str, query: str, offset: int, limit: int) -> list[Message]:
        query = f'''
            SELECT
                id,
                content,
                file,
                user_id,
                chat_id,
                relevance 
            FROM {Message.TABLE}
            WHERE chat_id = '{chat_id}' AND content ilike '%{query}%'
            ORDER BY relevance DESC 
            OFFSET {offset}
            LIMIT {limit};
        '''
        conn = await self.create_connection()
        rows = await conn.fetch(query)
        return [self.build_message(row) for row in rows]

    async def search_messages_count(self, chat_id: str, query: str) -> int:
        query = f'''SELECT count(*) FROM {Message.TABLE} WHERE chat_id = '{chat_id}' AND content ilike '%{query}%';'''
        conn = await self.create_connection()
        row = await conn.fetchrow(query)
        return row[0]

    async def search_members(self, chat_id: str, query: str, offset: int, limit: int) -> list[User]:
        query = f'''
            SELECT
                u.id,
                u.username,
                u.image,
                u.password
            FROM {Member.TABLE} m
            INNER JOIN {User.TABLE} u ON m.user_id = u.id
            WHERE m.chat_id = '{chat_id}' AND username ilike '%{query}%'
            OFFSET {offset}
            LIMIT {limit};
        '''
        conn = await self.create_connection()
        rows = await conn.fetch(query)
        return [self.build_user(row) for row in rows]

    async def search_members_count(self, chat_id: str, query: str) -> int:
        query = f'''
            SELECT count(*) FROM {Member.TABLE} m
            INNER JOIN {User.TABLE} u ON m.user_id = u.id
            WHERE m.chat_id = '{chat_id}' AND username ilike '%{query}%';
        '''
        conn = await self.create_connection()
        row = await conn.fetchrow(query)
        return row[0]

    @staticmethod
    def build_user(row):
        if row is None:
            return

        return (User(
            id=row[0],
            username=row[1],
            image=row[2],
            password=row[3],
        ))

    @staticmethod
    def build_chat(row):
        if row is None:
            return

        return (Chat(
            id=row[0],
            name=row[1],
            image=row[2],
            owner_id=row[3],
        ))

    @staticmethod
    def build_message(row):
        if row is None:
            return

        return (Message(
            id=row[0],
            content=row[1],
            file=row[2],
            user_id=row[3],
            chat_id=row[4],
            relevance=row[5]
        ))
