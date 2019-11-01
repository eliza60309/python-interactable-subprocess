# credits: https://websockets.readthedocs.io/
# sincere admiration and gratitude to the author of the source above

import asyncio
import websockets

async def echo(websocket, path):
    async for message in websocket:
        await websocket.send(message + ' hi')

start_server = websockets.serve(echo, "localhost", 5566)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()