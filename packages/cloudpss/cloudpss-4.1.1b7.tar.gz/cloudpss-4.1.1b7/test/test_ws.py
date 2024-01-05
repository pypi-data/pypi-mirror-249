from aiohttp import ClientSession, WSMsgType
import asyncio
import time
# ws://10.101.10.45/api/streams/token/fe943635-0dc9-40c8-8a27-39d02af66894

    
class WebsocketClient():
    message = []
    _status=0
    # __init__(self):
    def on_close(self):
        time.sleep(0.5)
        self._status = 1
        print("close")
    def on_error(self):
        self._status = 1
        print("error")
    def on_open(self):
        self._status = 0
        print("open")
    # websocket
    async def websocket_connect(self,url):
        
        # session = await ClientSession()
        # ws = await session.ws_connect(url)

        async with ClientSession() as session:
            async with session.ws_connect(url) as ws:
                self.on_open()
                async for msg in ws:
                    # print(msg.type)
                    if msg.type == WSMsgType.BINARY:
                        self.message.append(msg)
                    if msg.type == WSMsgType.TEXT:
                        self.message.append(msg)
                    elif msg.type == WSMsgType.CLOSED:
                        self.on_error()
                        break
                    elif msg.type == WSMsgType.ERROR:
                        self.on_close(msg.data)
                        break
        self._status=1
    def count(self):
        # await asyncio.sleep(0.1)
        # while self._status == 0:
        #     await asyncio.sleep(0.5)
        print(len(self.message))
        return self._status
        
    async def create(self):
       asyncio.create_task(self.websocket_connect('ws://10.101.10.45/api/streams/id/726dfbfa-dee4-4266-89f9-c6e18d8cc72b'))
       
async def main():
    ws=WebsocketClient()
    task=await ws.create()
    # task= ws.websocket_connect('ws://10.101.10.45/api/streams/id/6f6ce77c-48a1-4043-8549-1eb72a1a45c7')
    # print(task)
    # await ws.count()
    while ws.count() == 0:
        # time.sleep(0.5)
        await asyncio.sleep(0.5)
    # task_list=[asyncio.create_task(ws.count())]
    # await asyncio.wait(task_list)
    # print(x[0].pop().result())
if __name__ == '__main__':
    
    asyncio.run(main())