import datetime
import os
import traceback
from logging import Logger

import aiofiles

from helpers import Database


class BaseController:
    def __init__(self, config: dict, logger: Logger, db: Database):
        self._config = config
        self._logger = logger
        self._db = db

    async def save_file(self, user_id, file):
        try:
            base_dir = self._config["base_dir"]
            save_directory = str(os.path.join(base_dir, self._config["files"], user_id))

            os.makedirs(save_directory, exist_ok=True)
            file_path = os.path.join(save_directory, file.filename)

            db_path = str(os.path.join(self._config["files"], user_id, file.filename))
            if os.path.exists(file_path):
                return db_path

            file_bytes = file.file.read()
            async with aiofiles.open(file_path, 'wb') as file:
                await file.write(file_bytes)

            return db_path
        except Exception as e:
            self._logger.error(f"{e} {traceback.format_exc()}")
            return None
