import traceback
from logging import Logger

from aiohttp.web_request import Request

from controllers.base_controller import BaseController
from helpers import Database
from models import User
from models.Reponse import Response


class SearchController(BaseController):
    def __init__(self, config: dict, logger: Logger, db: Database):
        super().__init__(config, logger, db)

    async def search_users(self, request: Request) -> Response:
        try:

            user_id = request.headers.get("X-Auth")
            if not user_id:
                return Response(errors=["Войдите в аккаунт"], status=401)

            page = int(request.query.get("page"))
            username = request.query.get("username")

            limit = 20
            offset = (page - 1) * limit
            total = await self._db.search_users_count(query=username)
            pages = int(total / limit + (total % 1 if limit > 0 else 0))

            users = await self._db.search_users(query=username, offset=offset, limit=limit)
            return Response(data={
                "total": pages,
                "current": page,
                "data": [
                    {
                        "id": user.id,
                        "username": user.username,
                        "image": user.image
                    } for user in users]
            })
        except Exception as e:
            self._logger.error(f"{e} {traceback.format_exc()}")
            return Response(errors=["Не удалось найти пользователей"], status=500)

    async def search_members(self, request: Request) -> Response:
        try:

            user_id = request.headers.get("X-Auth")
            if not user_id:
                return Response(errors=["Войдите в аккаунт"], status=401)

            page = int(request.query.get("page"))
            chat_id = request.query.get("chat_id")
            username = request.query.get("username")

            limit = 20
            offset = (page - 1) * limit
            total = await self._db.search_members_count(chat_id=chat_id, query=username)
            pages = int(total / limit + (total % 1 if limit > 0 else 0))

            users = await self._db.search_members(chat_id=chat_id, query=username, offset=offset, limit=limit)
            return Response(data={
                "total": pages,
                "current": page,
                "data": [
                    {
                        "id": user.id,
                        "username": user.username,
                        "image": user.image
                    } for user in users]
            })
        except Exception as e:
            self._logger.error(f"{e} {traceback.format_exc()}")
            return Response(errors=["Не удалось найти участников чата"], status=500)

    async def search_messages(self, request: Request) -> Response:
        try:

            user_id = request.headers.get("X-Auth")
            if not user_id:
                return Response(errors=["Войдите в аккаунт"], status=401)

            page = int(request.query.get("page"))
            chat_id = request.query.get("chat_id")
            content = request.query.get("content")

            limit = 20
            offset = (page - 1) * limit
            total = await self._db.search_messages_count(chat_id=chat_id, query=content)
            pages = int(total / limit + (total % 1 if limit > 0 else 0))

            messages = await self._db.search_messages(chat_id=chat_id, query=content, offset=offset, limit=limit)

            return Response(data={
                "total": pages,
                "current": page,
                "data": [
                    {
                        "id": message.id,
                        "content": message.content,
                        "file": message.file,
                        "user_id": message.user_id,
                        "relevance": str(message.relevance)
                    }
                    for message in messages]
            })
        except Exception as e:
            self._logger.error(f"{e} {traceback.format_exc()}")
            return Response(errors=["Не удалось найти сообщения"], status=500)

    async def search_chats(self, request: Request) -> Response:
        try:

            user_id = request.headers.get("X-Auth")
            if not user_id:
                return Response(errors=["Войдите в аккаунт"], status=401)

            page = int(request.query.get("page"))
            name = request.query.get("name")

            limit = 20
            offset = (page - 1) * limit
            total = await self._db.search_chats_count(query=name)
            pages = int(total / limit + (total % 1 if limit > 0 else 0))

            chats = await self._db.search_chats(query=name, offset=offset, limit=limit)
            return Response(data={
                "total": pages,
                "current": page,
                "data": [
                    {
                        "id": chat.id,
                        "name": chat.name,
                        "image": chat.image,
                        "owner_id": chat.owner_id
                    }
                    for chat in chats]
            })
        except Exception as e:
            self._logger.error(f"{e} {traceback.format_exc()}")
            return Response(errors=["Не удалось найти чаты"], status=500)
