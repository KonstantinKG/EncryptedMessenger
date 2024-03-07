import json
from logging import Logger

import websockets


class WsClient:
    def __init__(self, config: dict, logger: Logger):
        self.config = config
        self.logger = logger

    async def send(self, event: str, data: dict, receivers: list):
        async with websockets.connect(self.config['websocket'], ping_timeout=60) as websocket:
            json_data = json.dumps(dict(type='send',  event=event, data=data, receivers=receivers), ensure_ascii=False)
            await websocket.send(json_data)
            await websocket.recv()
