import traceback
import uuid
from logging import Logger

from aiohttp.web_request import Request
from dateutil.parser import parse

from controllers.base_controller import BaseController
from helpers import Database, WsClient
from models import Chat, Message, Member
from models.Reponse import Response


class ChatController(BaseController):
    def __init__(self, config: dict, logger: Logger, db: Database, ws_client: WsClient):
        self._ws_client = ws_client
        super().__init__(config, logger, db)

    async def get(self, request: Request) -> Response:
        try:
            user_id = request.headers.get("X-Auth")
            if not user_id:
                return Response(errors=["Войдите в аккаунт"], status=401)

            chat_id = request.query.get("chat_id")

            chat = await self._db.get_chat(id=chat_id, user_id=user_id)
            if not chat:
                return Response(errors=["Не удалось найти чат или вы не являетесь его участником"], status=403)

            return Response(data={
                "id": chat.id,
                "name": chat.name,
                "image": chat.image,
                "owner_id": chat.owner_id
            })

        except Exception as e:
            self._logger.error(f"{e} {traceback.format_exc()}")
            return Response(errors=["Не удалось запросить чат"], status=500)

    async def all(self, request: Request) -> Response:
        try:
            user_id = request.headers.get("X-Auth")
            if not user_id:
                return Response(errors=["Войдите в аккаунт"], status=401)

            page = int(request.query.get("page"))

            limit = 20
            offset = (page - 1) * limit
            total = await self._db.get_chats_count(user_id=user_id)
            pages = int(total / limit + (total % 1 if limit > 0 else 0))

            chats = await self._db.get_chats(user_id=user_id, offset=offset, limit=limit)
            return Response(data={
                "total": total,
                "pages": pages,
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
            return Response(errors=["Не удалось запросить пользователей"], status=500)

    async def add(self, request: Request) -> Response:
        try:
            user_id = request.headers.get("X-Auth")
            if not user_id:
                return Response(errors=["Войдите в аккаунт"], status=401)

            data = await request.post()
            name = data.get("name")
            image = data.get("image")
            members_ids = data.get("members")
            members_ids = members_ids.split(",") if members_ids else []

            if not name:
                return Response(errors=["Название чата обязательно"], status=400)

            id = str(uuid.uuid4())
            image = await self.save_file(user_id=id, file=image)

            members = [Member(chat_id=id, user_id=user_id)]
            for member_id in members_ids:
                members.append(Member(chat_id=id, user_id=member_id))

            chat = Chat(id=id, name=name, image=image, owner_id=user_id)
            await self._db.insert(models=[chat])
            await self._db.insert(models=members)

            return Response(data={
                "id": chat.id,
                "name": chat.name,
                "image": chat.image,
                "owner_id": chat.owner_id
            })

        except Exception as e:
            self._logger.error(f"{e} {traceback.format_exc()}")
            return Response(errors=["Не удалось создать чат"], status=500)

    async def update(self, request: Request) -> Response:
        try:
            user_id = request.headers.get("X-Auth")
            if not user_id:
                return Response(errors=["Войдите в аккаунт"], status=401)

            data = await request.post()
            chat_id = data.get("chat_id")
            name = data.get("name")
            image = data.get("image")

            chat = await self._db.get_chat(id=chat_id, user_id=user_id)
            if not chat:
                return Response(errors=["Не удалось найти чат"], status=404)

            if chat.owner_id != user_id:
                return Response(errors=["Вы не являетесь создателем чата"], status=403)

            image = await self.save_file(user_id=user_id, file=image)
            if image and chat.image != image:
                chat.image = image

            if name and chat.name != name:
                chat.name = name

            await self._db.update(model=chat)
            return Response(data={
                "id": chat.id,
                "name": chat.name,
                "image": chat.image,
                "owner_id": chat.owner_id
            })

        except Exception as e:
            self._logger.error(f"{e} {traceback.format_exc()}")
            return Response(errors=["Не удалось обновить чат"], status=500)

    async def delete(self, request: Request) -> Response:
        try:
            user_id = request.headers.get("X-Auth")
            if not user_id:
                return Response(errors=["Войдите в аккаунт"], status=401)

            chat_id = request.query.get("id")

            chat = await self._db.get_chat(id=chat_id, user_id=user_id)
            if not chat:
                return Response(errors=["Не удалось найти чат"], status=404)

            if chat.owner_id != user_id:
                return Response(errors=["Вы не являетесь создателем чата"], status=403)

            await self._db.delete(model=chat)
            return Response(data="Чат успешно удален")

        except Exception as e:
            self._logger.error(f"{e} {traceback.format_exc()}")
            return Response(errors=["Не удалось удалить чат"], status=500)

    async def members_all(self, request: Request) -> Response:
        try:

            user_id = request.headers.get("X-Auth")
            if not user_id:
                return Response(errors=["Войдите в аккаунт"], status=401)

            chat_id = request.query.get("chat_id")

            users = await self._db.get_chat_users(chat_id=chat_id)
            return Response(data=[
                {
                    "id": user.id,
                    "username": user.username,
                    "image": user.image
                }
                for user in users
            ])
        except Exception as e:
            self._logger.error(f"{e} {traceback.format_exc()}")
            return Response(errors=["Не удалось запросить пользователей"], status=500)

    async def members_add(self, request: Request) -> Response:
        try:
            user_id = request.headers.get("X-Auth")
            if not user_id:
                return Response(errors=["Войдите в аккаунт"], status=401)

            data = await request.post()

            chat_id = data.get("chat_id")
            members_ids = data.get("members")
            members_ids = members_ids.split(",") if members_ids else []

            chat = await self._db.get_chat(id=chat_id, user_id=user_id)
            if not chat:
                return Response(errors=["Не удалось найти чат"], status=404)

            if chat.owner_id != user_id:
                return Response(errors=["Вы не являетесь создателем чата"], status=403)

            members = []
            for member_id in members_ids:
                member = Member(chat_id=chat.id, user_id=member_id)
                members.append(member)

            await self._db.insert(models=members)
            return Response(data=[
                {
                    "chat_id": member.chat_id,
                    "user_id": member.user_id,
                } for member in members
            ])

        except Exception as e:
            self._logger.error(f"{e} {traceback.format_exc()}")
            return Response(errors=["Не удалось создать чат"], status=500)

    async def members_delete(self, request: Request) -> Response:
        try:
            user_id = request.headers.get("X-Auth")
            if not user_id:
                return Response(errors=["Войдите в аккаунт"], status=401)

            data = await request.json()
            chat_id = data.get("chat_id")
            members_ids = data.get("members")

            chat = await self._db.get_chat(id=chat_id, user_id=user_id)
            if not chat:
                return Response(errors=["Не удалось найти чат"], status=404)

            if chat.owner_id != user_id:
                return Response(errors=["Вы не являетесь создателем чата"], status=403)

            await self._db.delete_members(chat_id=chat_id, members=members_ids)
            return Response(data="Пользовател(ь/и) успешно удален(ы)")

        except Exception as e:
            self._logger.error(f"{e} {traceback.format_exc()}")
            return Response(errors=["Не удалось удалить пользователей"], status=500)

    async def messages_all(self, request: Request) -> Response:
        try:
            user_id = request.headers.get("X-Auth")
            if not user_id:
                return Response(errors=["Войдите в аккаунт"], status=401)

            chat_id = request.query.get("chat_id")
            users = await self._db.get_chat_users(chat_id=chat_id)
            if not any(filter(lambda x: x.id == user_id, users)):
                return Response(errors=["Вы не являетесь участником чата"], status=403)

            page = int(request.query.get("page"))

            limit = 20
            offset = (page - 1) * limit
            total = await self._db.get_chat_messages_count(chat_id=chat_id)
            pages = int(total / limit + (total % 1 if limit > 0 else 0))

            messages = await self._db.get_chat_messages(chat_id=chat_id, offset=offset, limit=limit)

            return Response(data={
                "total": total,
                "pages": pages,
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
            return Response(errors=["Не удалось запросить пользователей"], status=500)

    async def message_add(self, request: Request) -> Response:
        try:
            user_id = request.headers.get("X-Auth")
            if not user_id:
                return Response(errors=["Войдите в аккаунт"], status=401)

            data = await request.post()

            chat_id = data.get("chat_id")
            users = await self._db.get_chat_users(chat_id=chat_id)
            if not any(filter(lambda x: x.id == user_id, users)):
                return Response(errors=["Вы не являетесь участником чата"], status=403)

            content = data.get("content")
            file = await self.save_file(user_id, data.get("file"))
            relevance = parse(data.get("relevance"))

            if not content and not file:
                return Response(errors=["Одно из полей контент или файл должно быть заполнено"])

            message = Message(id=str(uuid.uuid4()), content=content, file=file, user_id=user_id, chat_id=chat_id,
                              relevance=relevance)
            await self._db.insert(models=[message])

            receivers = await self._db.get_chat_users_ids(chat_id=chat_id, except_user_id=user_id)
            data = {
                "id": message.id,
                "content": message.content,
                "file": message.file,
                "user_id": message.user_id,
                "chat_id": message.chat_id,
                "relevance": str(message.relevance)
            }

            await self._ws_client.send(event="message_added", data=data, receivers=receivers)
            return Response(data=data)

        except Exception as e:
            self._logger.error(f"{e} {traceback.format_exc()}")
            return Response(errors=["Не удалось создать сообщение"], status=500)
