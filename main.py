import subprocesswithfd
import asyncio
import websockets
import threading

async def wshandler(websocket, path):
    process = subprocesswithfd.subprocesswithfd(["a.exe"], stdin = True, stdout = True)
    asyncio.ensure_future(reader(process.stdout, websocket))
    async for message in websocket:
        process.stdin.write(message + "\n")
    process.end()
    print("main done")


async def reader(readfd, sendfd):
    assert callable(readfd.read)
    assert callable(readfd.is_alive)
    assert callable(sendfd.send)
    while True:
        try: 
            await asyncio.sleep(0.1)
            string = readfd.read()
            if string != None and string != "":
                await sendfd.send(string)
        except:
            return



start_server = websockets.serve(wshandler, "localhost", 5566)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
