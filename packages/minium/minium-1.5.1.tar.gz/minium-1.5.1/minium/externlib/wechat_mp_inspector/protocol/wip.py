'''
Author: yopofeng yopofeng@tencent.com
Date: 2023-09-11 19:42:21
LastEditors: yopofeng yopofeng@tencent.com
LastEditTime: 2023-11-13 10:56:08
FilePath: /wechat-mp-inspector/wechat_mp_inspector/protocol/wip.py
Description: 定义webkit的远程调试会话
'''
from typing import Any, Tuple, Union, Callable
import json

from wechat_mp_inspector.command import CommandType, Commands
from ..logger import logger
from pymobiledevice3.lockdown_service_provider import LockdownServiceProvider
from wechat_mp_inspector.connection.baseconn import BaseEvent
from wechat_mp_inspector.connection.lockdownconn import OPEN_TIMEOUT
from wechat_mp_inspector.event import BaseEvent
from .baseprotocol import BaseProtocol, CommandType, BaseEvent, Command, AsyncCommand
from .basewebkit import WebkitInspectorProtocol, EventType, WIP
from .protocolcommand import ProtocolCommand
from ..connection.baseconn import BaseConnection
from ..connection.lockdownconn import LockdownConnection
from .basesession import BaseSession, BaseWebkitSession
import threading


class WIPConnection(LockdownConnection):
    def __init__(self, lockdown: LockdownServiceProvider, loop=None, timeout=None):
        super(WIPConnection, self).__init__(lockdown, loop, timeout)
        self.ignore_method = set()
        self.logger = logger.getChild(f"Conn{self._id[-4:]}")
        self.protocol = WebkitInspectorProtocol()

    def _handle_response(self, ret_json) -> Tuple[str, Any]:
        req_id = None
        if "id" in ret_json:  # response
            req_id = ret_json["id"]
            if "error" in ret_json:
                err_msg = ret_json["error"].get("message", "")
                return req_id, Exception(err_msg)
        return req_id, ret_json

    def _handle_event(self, ret_json):
        """处理通知事件

        :param Object ret_json: 消息体
        :return None or BaseEvent: 事件
        """
        return self.protocol.parse_event(ret_json)

class WIPSession(BaseWebkitSession):
    """页面会话"""
    protocol: WebkitInspectorProtocol
    def __init__(self, connection: WIPConnection, id_, page):
        """
        :param wechat_mp_inspector.driver.iosdriver.IOSDriver driver: 
        :param str id_: 会话id
        :param _type_ page: _description_
        """
        super(WIPSession, self).__init__(id_, connection)
        self.appid_ = page.appid_
        self.pageid_ = page.id_
        self.protocol = connection.protocol

    def send_command(self, command: str or ProtocolCommand or CommandType, params: dict = None, *, sync=True, **kwargs):
        """发送命令, 并等待回复"""
        cmd = self._gen_command(command, params, sync=sync, **kwargs)
        return self.connection.send_command(cmd, session_id=self.id_, app_id = self.appid_, page_id=self.pageid_)

    def on(self, event: str or BaseEvent, callback: Callable):
        """监听事件"""
        return self.connection.on(event, callback)
    
    def remove_listener(self, event: str or BaseEvent, callback: Callable):
        return self.connection.remove_listener(event, callback)

    def remove_all_listeners(self):
        return self.connection.remove_all_listeners()
    
    def close(self):
        self.connection.close()