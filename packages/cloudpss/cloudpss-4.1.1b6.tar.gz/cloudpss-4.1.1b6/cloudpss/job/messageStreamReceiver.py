import logging

import aiohttp
from aiohttp import WSMsgType

from cloudpss.utils.httpAsyncRequest import websocket_connect
from .jobReceiver import JobReceiver
import os
from urllib.parse import urlparse
import websocket
import pytz
import threading
import time

utc_tz = pytz.timezone("UTC")

from ..utils.IO import IO


class Message(object):
    def __init__(self, id, token):
        self.id = id
        self.token = token


class MessageStreamReceiver(JobReceiver):
    def __init__(self, job, dev=False):
        super().__init__()
        self.job = job
        self.dev = dev
        self.origin = os.environ.get("CLOUDPSS_API_URL", "https://cloudpss.net/")
        self.__hasOpen = False

    def __receive_legacy(self, id, fr0m):
        """
        同步方法读取消息流中的数据
        id: 消息流id
        fr0m: 从哪个位置开始读取，如果为0则从头开始读取
        on_open: 连接建立时的回调函数
        on_message: 收到消息时的回调函数
        on_error: 发生错误时的回调函数
        on_close: 连接关闭时的回调函数
        """
        if id is None:
            raise Exception("id is None")
        u = list(urlparse(self.origin))
        head = "wss" if u[0] == "https" else "ws"

        path = head + "://" + str(u[1]) + "/api/streams/id/" + id
        if fr0m is not None:
            path = path + "&from=" + str(fr0m)
        logging.info(f"receive data from websocket: {path}")
        ws = websocket.WebSocketApp(
            path,
            on_open=self.__on_open,
            on_message=self.__on_message_legacy,
            on_error=self.__on_error,
            on_close=self.__on_close,
        )

        return ws

    async def __receive(self, id, fr0m):
        """
        读取消息流中的数据
        id: 消息流id
        fr0m: 从哪个位置开始读取，如果为0则从头开始读取
        on_open: 连接建立时的回调函数
        on_message: 收到消息时的回调函数
        on_error: 发生错误时的回调函数
        on_close: 连接关闭时的回调函数
        """
        if id is None:
            raise Exception("id is None")
        u = list(urlparse(self.origin))
        head = "wss" if u[0] == "https" else "ws"

        path = head + "://" + str(u[1]) + "/api/streams/id/" + id
        if fr0m is not None:
            path = path + "&from=" + str(fr0m)
        logging.info(f"MessageStreamReceiver data from websocket: {path}")
        async for msg in websocket_connect(
            path,
            open_func=self.__on_open,
        ):
            if msg.type == WSMsgType.BINARY:
                decode = self.__on_message(msg.data)
                yield decode
            elif msg.type == WSMsgType.TEXT:
                decode = self.__on_message(msg.data)
                yield decode
            elif msg.type == WSMsgType.CLOSED:
                logging.debug("WebSocket连接已关闭")
                self.__on_close()
                
                break
            elif msg.type == WSMsgType.ERROR:
                logging.debug(f"WebSocket连接发生错误：{msg.data}")
                self.__on_error(msg.data)
                break
        self._status=1
    ###下面是兼容Receiver部分功能实现
    def __on_message_legacy(self,  *args, **kwargs):
        if len(args) == 1:
            message = args[0]
        else:
            message = args[1]
        return self.__on_message(message)

    def __on_message(self, message):
        data = IO.deserialize(message, "ubjson")
        msg = IO.deserialize(data["data"], "ubjson")
        self.messages.append(msg)
        if(msg['type']=='terminate'):
            self.close(self.ws)
        return msg


    def __on_error(self,  *args, **kwargs):
        logging.debug("MessageStreamReceiver error")
        msg = {
            "type": "log",
            "verb": "create",
            "version": 1,
            "data": {
                "level": "error",
                "content": "websocket error",
            },
        }
        self.messages.append(msg)

    def __on_close(self, *args, **kwargs):
        if len(args)>0:
            msg =args[2]
            if msg.startswith("CMS_NO_STREAM_ID:"):
                self._status = 1
                msg = {
                    "type": "log",
                    "version": 1,
                    "data": {
                        "level": "critical",
                        "content": "未找到任务的输出流，运行结果可能已被清理。",
                    },
                }
                self.messages.append(msg)
                return
        logging.debug("MessageStreamReceiver close")
        self._status = 1
        msg = {
            "type": "log",
            "verb": "create",
            "version": 1,
            "data": {
                "level": "info",
                "content": "websocket closed",
            },
        }
        self.messages.append(msg)

    
    def __on_open(self,ws, *args, **kwargs):
        self.ws = ws
        logging.debug(f"MessageStreamReceiver on_open")
        self._status = 0
        self.__hasOpen = True
        pass

    def close(self, ws):
        self._status = 1
        ws.close()

    @property
    def status(self):
        return self._status

    @property
    def end(self):
        return not self._status

    def connect_legacy(self):
        self._status = 1
        self.ws = self.__receive_legacy(
            self.job.output,
            None,
        )
        thread = threading.Thread(target=self.ws.run_forever, args=(None, None, 6, 3))
        thread.setDaemon(True)
        thread.start()
        while not self.__hasOpen:
            time.sleep(0.2)

    async def connect(self):
        self._status = 0
        self.receiver= self.__receive(
            self.job.output,
            None,
        )
        # asyncio.create_task(
        #     self.__receive(
        #         self.job.output,
        #         None
        #     )
        # )