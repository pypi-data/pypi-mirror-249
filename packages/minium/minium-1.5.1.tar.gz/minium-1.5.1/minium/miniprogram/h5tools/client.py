# -*-coding: utf-8 -*-
'''
Author: gavinggu gavinggu@tencent.com
Date: 2023-09-04 11:07:50
LastEditors: yopofeng yopofeng@tencent.com
LastEditTime: 2023-10-18 10:41:34
FilePath: /py-minium/minium/miniprogram/h5tools/client.py
Description: h5 通信模块
'''
import logging
import json
from websockets.sync.client import connect

logger = logging.getLogger("minium")


class CDPClient:

    _request_id = 0

    def __init__(self, websocket_debug_url):
        self.websocket_debug_url = websocket_debug_url
        self.websocket = None

    def _send(self, message):
        self.websocket.send(json.dumps(message))

    def _receive(self):
        return json.loads(self.websocket.recv())

    def connect(self):
        self.websocket = connect(self.websocket_debug_url)

    def send_command(self, method, params=None):
        type(self)._request_id += 1
        message = {
            'id': type(self)._request_id,
            'method': method,
            'params': params or {},
        }
        self._send(message)

        while True:
            response_data = self._receive()
            if 'id' in response_data and response_data['id'] == type(self)._request_id:
                return response_data

    def disconnect(self):
        if self.websocket:
            self.websocket.close()

# new client
from wechat_mp_inspector import AndroidConfig, AndroidDriver
class AndroidClient:
    CACHE = {}
    driver: AndroidDriver = None
    def __init__(self, config: dict) -> None:
        self.inspector = None
        self.page = None
        key = f"{config.device['serial']}-{config.appid}" if config.appid else f"{config.device['serial']}"
        if key in AndroidClient.CACHE:
            self.driver = AndroidClient.CACHE[key]
        else:
            self.driver = AndroidDriver(AndroidConfig(config.device, logger_level=logging.DEBUG))
            AndroidClient.CACHE[key] = self.driver

    def inspect(self, debugger_url: str, enable_list=[]):
        pages = self.driver.get_pages()
        for page in pages:
            if page.webSocketDebuggerUrl.split("/")[-1] == debugger_url.split("/")[-1]:
                self.page = page
                break
        if not self.page:
            logger.warning(f"driver无法获取 {debugger_url} 的page实例")
            raise RuntimeError(f"driver无法获取 {debugger_url} 的page实例")
        inspector = self.driver.inspector_session(self.page)
        for e in enable_list:
            inspector.send_command(e)
        return inspector
        


