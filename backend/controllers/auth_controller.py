import traceback
import uuid
from logging import Logger

import bcrypt
from aiohttp.web_request import Request

from controllers.base_controller import BaseController
from helpers import Database, KeyGenerator
from models import User
from models.Reponse import Response


class AuthController(BaseController):
    def __init__(self, config: dict, logger: Logger, db: Database, key_generator: KeyGenerator):
        self.key_generator = key_generator
        super().__init__(config, logger, db)

    async def login(self, request: Request) -> Response:
        try:
            data = await request.post()

            username = data.get("username")
            password = data.get("password")

            user = await self._db.get_user_by_username(username=username)
            if not user:
                return Response(errors=["Некоректный логин или пароль"], status=400)

            if not bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
                return Response(errors=["Некоректный логин или пароль"], status=400)

            return Response(data={"id": user.id, "key": str(self.key_generator.key)})

        except Exception as e:
            self._logger.error(f"{e} {traceback.format_exc()}")
            return Response(errors=["Не авторизовать пользователя"], status=500)

    async def register(self, request: Request) -> Response:
        try:
            data = await request.post()

            username = data.get("username")
            password = data.get("password")
            image = data.get("image")

            if not all([username, password]):
                return Response(errors=["Имя пользователя и пароль обязательные поля"], status=400)

            if await self._db.is_username_taken(username=username):
                return Response(errors=["Имя пользователя занято"], status=409)

            id = str(uuid.uuid4())
            image = await self.save_file(user_id=id, file=image)
            password = self.hash_password(password=password)

            user = User(id=id, username=username, image=image, password=password)
            await self._db.insert(models=[user])
            return Response(data={"id": user.id, "key": str(self.key_generator.key)})

        except Exception as e:
            self._logger.error(f"{e} {traceback.format_exc()}")
            return Response(errors=["Не удалось зарегестрировать аккаунт"], status=500)

    @staticmethod
    def hash_password(password: str) -> str:
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password.decode('utf-8')
