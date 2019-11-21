import asyncio
import json
import logging
import websockets

import aiohttp
from aiohttp import web


logging.basicConfig()

STATE = dict()
USERS = set()

ORDER = ['x', 'y', 'z', 'trigger']

async def notify_users():
    if USERS:       # asyncio.wait doesn't accept an empty list
        serialized_state = ';'.join(str(STATE.get(i, 0)) for i in ORDER)
        print(serialized_state)
        await asyncio.wait([user.send_str(serialized_state) for user in USERS])


async def websocket_handler(request):
    websocket = web.WebSocketResponse()
    print('connected')
    await websocket.prepare(request)

    USERS.add(websocket)
    try:
        async for msg in websocket:
            if msg.type == aiohttp.WSMsgType.TEXT:
                # print(msg.data)
                STATE.update(json.loads(msg.data))
                await notify_users()
    finally:
        USERS.remove(websocket)

    return websocket

def game():
    """return position of the ball"""
    return


async def hello(request):
    with open('./index.html') as file:
        html_data = file.read()

    return web.Response(text=html_data, content_type='text/html')


app = web.Application()
app.add_routes([
    web.get('/', hello),
    web.get('/ws', websocket_handler)
])

web.run_app(app)
