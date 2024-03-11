import asyncio
import json
import logging.config
import os
import sys

import aiohttp_cors
from aiohttp import web
from aiohttp_swagger import setup_swagger

from controllers import AuthController, UserController, ChatController, SearchController
from helpers import Database, WsClient

with open("config.json", 'r', encoding='utf-8') as file:
    config = json.load(file)

base_dir = os.path.dirname(__file__)
config["base_dir"] = os.path.join(base_dir, "../")

logging.config.dictConfig(config=config["logger"])
logger = logging.getLogger(name=config["app"])

database = Database(config=config, logger=logger)

ws_client = WsClient(config=config, logger=logger)

auth_controller = AuthController(
    config=config,
    logger=logger,
    db=database
)

user_controller = UserController(
    config=config,
    logger=logger,
    db=database
)

chat_controller = ChatController(
    config=config,
    logger=logger,
    db=database,
    ws_client=ws_client
)

search_controller = SearchController(
    config=config,
    logger=logger,
    db=database
)

app = web.Application()


async def get(request):
    response = await user_controller.get(request=request)
    return web.json_response(response.out(), status=response.status)


async def all(request):
    response = await user_controller.all(request=request)
    return web.json_response(response.out(), status=response.status)


async def update(request):
    response = await user_controller.update(request=request)
    return web.json_response(response.out(), status=response.status)


async def delete(request):
    response = await user_controller.delete(request=request)
    return web.json_response(response.out(), status=response.status)


async def login(request):
    response = await auth_controller.login(request=request)
    return web.json_response(response.out(), status=response.status)


async def register(request):
    response = await auth_controller.register(request=request)
    return web.json_response(response.out(), status=response.status)


async def chat_get(request):
    response = await chat_controller.get(request=request)
    return web.json_response(response.out(), status=response.status)


async def chat_all(request):
    response = await chat_controller.all(request=request)
    return web.json_response(response.out(), status=response.status)


async def chat_add(request):
    response = await chat_controller.add(request=request)
    return web.json_response(response.out(), status=response.status)


async def chat_update(request):
    response = await chat_controller.update(request=request)
    return web.json_response(response.out(), status=response.status)


async def chat_delete(request):
    response = await chat_controller.delete(request=request)
    return web.json_response(response.out(), status=response.status)


async def chat_members_all(request):
    response = await chat_controller.members_all(request=request)
    return web.json_response(response.out(), status=response.status)


async def chat_members_add(request):
    response = await chat_controller.members_add(request=request)
    return web.json_response(response.out(), status=response.status)


async def chat_messages_all(request):
    response = await chat_controller.messages_all(request=request)
    return web.json_response(response.out(), status=response.status)


async def chat_messages_add(request):
    response = await chat_controller.message_add(request=request)
    return web.json_response(response.out(), status=response.status)


async def search_users(request):
    response = await search_controller.search_users(request=request)
    return web.json_response(response.out(), status=response.status)


async def search_members(request):
    response = await search_controller.search_members(request=request)
    return web.json_response(response.out(), status=response.status)


async def search_chats(request):
    response = await search_controller.search_chats(request=request)
    return web.json_response(response.out(), status=response.status)


async def search_messages(request):
    response = await search_controller.search_messages(request=request)
    return web.json_response(response.out(), status=response.status)


app.router.add_get('/get', get)
app.router.add_get('/all', all)
app.router.add_put('/update', update)
app.router.add_delete('/delete', delete)
app.router.add_post('/login', login)
app.router.add_post('/register', register)

app.router.add_get('/chat/get', chat_get)
app.router.add_get('/chat/all', chat_all)
app.router.add_post('/chat/add', chat_add)
app.router.add_put('/chat/update', chat_update)
app.router.add_delete('/chat/delete', chat_delete)
app.router.add_get('/chat/members/all', chat_members_all)
app.router.add_post('/chat/members/add', chat_members_add)
app.router.add_get('/chat/messages/all', chat_messages_all)
app.router.add_post('/chat/messages/add', chat_messages_add)

app.router.add_get('/search/users', search_users)
app.router.add_get('/search/members', search_members)
app.router.add_get('/search/chats', search_chats)
app.router.add_get('/search/messages', search_messages)

setup_swagger(app, swagger_url="/api/documentation", swagger_from_file="swagger.yaml", ui_version=3)

cors = aiohttp_cors.setup(
    app=app,
    defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
    })

for route in list(app.router.routes()):
    cors.add(route)

if __name__ == '__main__':
    if (
            sys.version_info[0] == 3
            and sys.version_info[1] >= 8
            and sys.platform.startswith("win")
    ):
        policy = asyncio.WindowsSelectorEventLoopPolicy()
        asyncio.set_event_loop_policy(policy)

    logger.info(f"Running server on {config['host']}:{config['port']}")
    web.run_app(
        app=app,
        host=config['host'],
        port=config['port']
    )
