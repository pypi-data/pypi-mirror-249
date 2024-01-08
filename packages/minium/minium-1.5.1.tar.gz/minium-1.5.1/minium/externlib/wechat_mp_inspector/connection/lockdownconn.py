'''
Author: yopofeng yopofeng@tencent.com
Date: 2023-09-22 16:06:05
LastEditors: yopofeng yopofeng@tencent.com
LastEditTime: 2023-10-16 16:48:08
FilePath: /wechat-mp-inspector/wechat_mp_inspector/connection/lockdownconn.py
Description: 定义通过lockdown连接的webinspector链接
'''
from typing import Mapping, Tuple, Any, Dict
import json
import time
from dataclasses import dataclass
from pymobiledevice3.lockdown_service_provider import LockdownServiceProvider
from pymobiledevice3.services.webinspector import WebinspectorService

from wechat_mp_inspector.command import Command, CommandType, AsyncCommand
from ..command import CommandType, Command, BaseCommand
from .baseconn import BaseAsyncConnection, BaseEvent, STATE
from ..pages.safaripage import BasePage, Page
from ..utils import json2obj, Object, cost_debug, AsyncCondition
from ..event import BaseEvent
from ..logger import logger


OPEN_TIMEOUT = 30  # 链接超时时间


@dataclass
class SocketCommandExtend:
    session_id: str
    app_id: str
    page_id: str


class LockdownConnection(WebinspectorService, BaseAsyncConnection):
    INSTANCES: Dict[str, 'LockdownConnection'] = {}  # 控制生成单实例
    _state = STATE.CLOSE  # 默认链接状态close
    
    _unique_id = None

    def __new__(
        cls, lockdown: LockdownServiceProvider, loop=None, timeout=None
    ):
        unique_id = lockdown.udid
        INSTANCES = cls.INSTANCES
        if unique_id in INSTANCES:
            inst = INSTANCES[unique_id]
            if inst._state != STATE.CLOSE:
                return inst  # 使用旧的实例
            # 缓存的实例没有链接
            inst.destroy()
            INSTANCES[unique_id] = inst  # 不改变实例, 直接重新init
            return inst
        inst = object.__new__(cls)
        inst._unique_id = unique_id
        INSTANCES[unique_id] = inst
        return inst

    def __init__(self, lockdown: LockdownServiceProvider, loop=None, timeout=None):
        if self._state != STATE.CLOSE:  # 有已经链接的实例
            return
        BaseAsyncConnection.__init__(self, loop=loop)
        # ❕❕❕WebinspectorService中的异步调用基本为call_soon, 不能跨线程调用
        WebinspectorService.__init__(self, lockdown, loop)
        self.connect(timeout or OPEN_TIMEOUT)
        self._state = STATE.OPEN
        while not self.connected_application:
            # 等待连接到webinspectord服务等app, 证明服务已经注册好
            self.flush_input()
        self._is_close_on_my_own = False  # 链接是自己主动断开的, 主要标记是否进行链接重连

    def destroy(self):
        self._state = STATE.CLOSE
        if self._unique_id in self.__class__.INSTANCES:
            self.__class__.INSTANCES.pop(self._unique_id)
        if self._is_close_on_my_own:
            self.logger.debug("already destroy")
            return
        self._is_close_on_my_own = True
        self.close()

    # ⬇️⬇️⬇️ 以下是重构方法
    async def _forward_indicate_web_view(self, app_id: str, page_id: int, enable: bool):
        # 纯fix
        await self._send_message('_rpc_forwardIndicateWebView:', {
            'WIRApplicationIdentifierKey': app_id,
            'WIRPageIdentifierKey': page_id,
            'WIRIndicateEnabledKey': enable,
        })

    async def _forward_socket_data(self, session_id: str, app_id: str, page_id: int, data: Mapping or str):
        _data = data.encode() if isinstance(data, str) else json.dumps(data).encode()
        await self._send_message('_rpc_forwardSocketData:', {
            'WIRApplicationIdentifierKey': app_id,
            'WIRPageIdentifierKey': page_id,
            'WIRSessionIdentifierKey': session_id,
            'WIRSocketDataKey': _data,
        })

    def _handle_application_sent_listing(self, arg):
        """重构该方法生产新的page实例"""
        appid_ = arg['WIRApplicationIdentifierKey']
        if appid_ in self.application_pages:
            for id_, page in arg['WIRListingKey'].items():
                page["appid_"] = appid_
                if id_ in self.application_pages[appid_]:
                    self.application_pages[appid_][id_].update(page)
                else:
                    self.application_pages[appid_][id_] = Page.from_page_dictionary(page)
        else:
            pages = {}
            for id_, page in arg['WIRListingKey'].items():
                pages[id_] = Page.from_page_dictionary(page)
            self.application_pages[appid_] = pages

    def _handle_application_sent_data(self, arg):
        """处理回包信息"""
        message = arg['WIRMessageDataKey']
        self._on_message(message)

    def _check_conn_exception(self, cmd: Command):
        if self._is_close_on_my_own:
            raise ConnectionAbortedError("close by myself")
        elif self._state == STATE.CLOSE:
            if cmd.id in self._sync_wait_map:
                del self._sync_wait_map[cmd.id]
            if cmd.reason:
                raise cmd.reason
            raise ConnectionAbortedError("connection closed")

    # ⬆️⬆️⬆️ 以上是重构方法
    
    # lockdown connection使用了异步接口, send_command不能有非async阻塞操作
    # _receive_response中等待和通知接口需要进行异步重构

    def _safely_send(self, cmd: CommandType, **extend):
        kwargs = {}
        for i in ("session_id", "app_id", "page_id"):
            if i not in extend:
                raise RuntimeError(f"socket command miss {i}")
            else:
                kwargs[i] = extend[i]
        kwargs["data"] = cmd.dumps()
        self.logger.debug("SEND > %.510s" % json.dumps(kwargs))
        return self.await_(self.send_socket_data(**kwargs))
    

