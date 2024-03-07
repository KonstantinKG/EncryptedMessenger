import asyncio
import json
import logging.config
import os.path
import sys
import traceback
import websockets

from websockets.exceptions import ConnectionClosed

directory = os.path.dirname(__file__)
config = json.loads(open(os.path.join(directory, 'config.json'), 'r', encoding='utf-8').read())

logging.config.dictConfig(config=config["logger"])
logger = logging.getLogger(name=config["app"])

listeners = dict()
ids = dict()


async def handle_client(websocket, path):
    global listeners, groups
    try:
        while True:
            json_data = await websocket.recv()
            try:
                message = json.loads(json_data)
                type = message['type']
            except Exception as e:
                logger.error(f"Error with received message occurred {e} \nTRACEBACK: {traceback.format_exc()}")
                continue

            if type == 'send':
                data = {
                    "event": message['event'],
                    "data": message['data']
                }

                receivers = []
                for user_id in message['receivers']:
                    receiver = listeners.get(user_id)
                    if not receiver:
                        continue
                    receivers += receiver

                websockets.broadcast(receivers, json.dumps(data, ensure_ascii=False))
                await websocket.send("ok")

            if type == 'listen':
                user_id = message['user_id']
                if user_id not in listeners:
                    listeners[user_id] = []

                if websocket.id in ids:
                    continue

                ids[websocket.id] = user_id
                listeners[user_id].append(websocket)

    except ConnectionClosed:
        user_id = ids.pop(websocket.id, None)
        if user_id is not None:
            listeners[user_id].remove(websocket)
    except Exception as e:
        logger.error(f"Error occurred {e} \nTRACEBACK: {traceback.format_exc()}")


if __name__ == '__main__':
    logger.info(f"Running server on {config['host']}:{config['port']}")
    start_server = websockets.serve(handle_client, config['host'], config['port'], ping_timeout=None, ping_interval=None)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
