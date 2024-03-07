import traceback
from logging import Logger

from aiohttp.web_request import Request

from controllers.base_controller import BaseController
from helpers import Database
from models import User
from models.Reponse import Response


class UserController(BaseController):
    def __init__(self, config: dict, logger: Logger, db: Database):
        super().__init__(config, logger, db)

    async def get(self, request: Request) -> Response:
        try:

            user_id = request.headers.get("X-Auth")
            if not user_id:
                return Response(errors=["Войдите в аккаунт"], status=401)

            id = request.query.get("id")
            id = id if id else user_id

            user = await self._db.get_user(id=id)
            return Response(data={
                "id": user.id,
                "username": user.username,
                "image": user.image
            })
        except Exception as e:
            self._logger.error(f"{e} {traceback.format_exc()}")
            return Response(errors=["Не удалось запросить пользователя"], status=500)

    async def all(self, request: Request) -> Response:
        try:
            user_id = request.headers.get("X-Auth")
            if not user_id:
                return Response(errors=["Войдите в аккаунт"], status=401)

            page = int(request.query.get("page"))

            limit = 20
            offset = (page - 1) * limit
            total = await self._db.get_users_count()
            pages = int(total / limit + (total % 1 if limit > 0 else 0))

            users = await self._db.get_users(offset=offset, limit=limit)
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
            return Response(errors=["Не удалось запросить пользователей"], status=500)

    async def update(self, request: Request) -> Response:
        try:
            user_id = request.headers.get("X-Auth")
            if not user_id:
                return Response(errors=["Войдите в аккаунт"], status=401)

            data = await request.post()
            username = data.get("username")
            image = data.get("image")

            user = await self._db.get_user(id=user_id)
            if user.username != username:
                if await self._db.is_username_taken(username=username):
                    return Response(errors=["Имя пользователя занято"], status=409)
                user.username = username

            image = await self.save_file(user_id, image)
            if image and user.image != image:
                user.image = image

            await self._db.update(model=user)
            return Response(data="Пользователь удален успешно")
        except Exception as e:
            self._logger.error(f"{e} {traceback.format_exc()}")
            return Response(errors=["Не удалось удалить пользователя"], status=500)

    async def delete(self, request: Request) -> Response:
        try:
            user_id = request.headers.get("X-Auth")
            if not user_id:
                return Response(errors=["Войдите в аккаунт"], status=401)

            await self._db.delete(model=User(id=user_id, username=None, image=None, password=None))
            return Response(data="Пользователь удален успешно")
        except Exception as e:
            self._logger.error(f"{e} {traceback.format_exc()}")
            return Response(errors=["Не удалось удалить пользователя"], status=500)
