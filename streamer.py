import asyncio
import json
import logging
import websockets

import aiohttp
from aiohttp import web
from datetime import datetime


logging.basicConfig()

STATE = dict()
USERS = set()

ORDER = ['x', 'y', 'z', 'trigger']


class Game:
        
        def __init__(self):
                self.before = datetime.now()

                self.FIELD = [0, 0, 0, 0, 0, 0, 0, 0]                                  
                self.SPEED = (10**6 - 10000)  
                self.DIRECTIONS = {"LEFT": -1, "RIGHT": 1}                                                                                                                           
                self.BALL_POSITION = 0

                self.DIRECTION = "RIGHT"
                
                self.trigger_state = 0

        def main_loop(self, trigger_state):
                # print(trigger_state, type(trigger_state))
                if trigger_state is not None:
                        trigger_state = int(trigger_state)
                
                now = datetime.now()
                td = now - self.before
                td = td.seconds * 10**6 + td.microseconds

                if td > self.SPEED:
                        try:
                                self.before = now

                                NEW_BALL_POSITION = self.BALL_POSITION + self.DIRECTIONS[self.DIRECTION]
                                if NEW_BALL_POSITION == 0 or NEW_BALL_POSITION == 7:
                                   if trigger_state == 1: 
                                        if self.DIRECTION == "RIGHT":
                                                self.DIRECTION = "LEFT"
                                        else:
                                                self.DIRECTION = "RIGHT"
                                if NEW_BALL_POSITION == -1 or NEW_BALL_POSITION == 8:
                                        print("game over")
                                        raise 

                                self.FIELD[NEW_BALL_POSITION] = 1
                                self.FIELD[self.BALL_POSITION] = 0
                                self.BALL_POSITION = NEW_BALL_POSITION
                                print(self.FIELD)


                        except IndexError:
                                if self.DIRECTION == "RIGHT":
                                        self.DIRECTION = "LEFT"
                                else:
                                        self.DIRECTION = "RIGHT"



game = Game()


async def notify_users():
    if USERS:       # asyncio.wait doesn't accept an empty list
        serialized_state = ';'.join(str(STATE.get(i, 0)) for i in ORDER)
        # print(serialized_state)
        trigger_state = STATE.get(ORDER[-1], 0)
        game.main_loop(trigger_state)
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
