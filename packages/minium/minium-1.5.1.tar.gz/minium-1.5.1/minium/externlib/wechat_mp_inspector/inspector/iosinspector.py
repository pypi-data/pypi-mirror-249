'''
Author: yopofeng yopofeng@tencent.com
Date: 2023-09-21 17:32:32
LastEditors: yopofeng yopofeng@tencent.com
LastEditTime: 2023-10-11 11:53:29
FilePath: /wechat-mp-inspector/wechat_mp_inspector/inspector/iosinspector.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import asyncio
from typing import Callable
from ..logger import logger
from ..utils import AsyncCallback
from ..protocol.protocolcommand import ProtocolCommand
from ..protocol.wip import WIPSession, WIP, CommandType, BaseEvent, Command, AsyncCommand, BaseSession
from .baseinspector import BaseInspector
from ..connection.baseconn import BaseConnection

class IOSInspectorSession(BaseInspector, BaseConnection):
    """target base"""
    _session: WIPSession
    DEFAULT_COMMAND_TIMEOUT = 10
    def __init__(self, session: WIPSession, target_id: str) -> None:
        BaseInspector.__init__(self, session)
        BaseConnection.__init__(self)
        self._target_id = target_id
        self._session.on("Target.dispatchMessageFromTarget", self._dispatch_message_from_target)
        self._session.on("Target.didCommitProvisionalTarget", self._did_commit_provisional_target)
        # init default domain
        enable_list = [
            "Runtime.enable",
        ]
        self._session.connection.await_(asyncio.gather(*[
           self._session.connection._get_aysnc_msg_return(self.send_command(cmd, sync=False))  for cmd in enable_list
        ]))

    @property
    def id(self):
        return f"{self._session.appid_}:{self._session.pageid_}:{self._target_id}"

    @classmethod
    async def create(cls, session: WIPSession):
        callback = AsyncCallback()
        session.on("Target.targetCreated", callback)
        session.on("Target.targetInfoChanged", callback)
        await session.connection._forward_indicate_web_view(session.appid_, session.pageid_, True)
        await session.connection._forward_indicate_web_view(session.appid_, session.pageid_, False)
        await session.connection.setup_inspector_socket(session.id_, session.appid_, session.pageid_)
        await callback._waiter
        target_info: WIP.Target.TargetInfo = callback.get_result().targetInfo  # event.params
        target_id = target_info.targetId
        logger.info(f'Created: {target_id}')
        target = cls(session, target_id)
        return target
    
    def _dispatch_message_from_target(self, event: WIP.Target.dispatchMessageFromTarget):
        if event.targetId != self._target_id:  # ignore
            return
        self._on_message(event.message)

    def _did_commit_provisional_target(self, event: WIP.Target.didCommitProvisionalTarget):
        self._target_id = event.newTargetId
        logger.info(f'Created: {self._target_id}')
    
    def send_command(self, command: str or ProtocolCommand or CommandType, params: dict = None, *, sync=True, max_timeout=None, **kwargs):
        """发送命令, 并等待回复
        
        ❕❕❕不能在子线程中使用(asyncio的一堆问题...)
        """
        if max_timeout is None:
            max_timeout = self.default_command_timeout
        cmd = self._session._gen_command(command, params, sync=sync, max_timeout=max_timeout, **kwargs)
        return BaseConnection.send_command(self, cmd)

    def _safely_send(self, cmd: CommandType, **extend):
        """真实发送消息的方法"""
        target_cmd = self._session.protocol.protocol.Target.sendMessageToTarget(message=cmd.dumps(), targetId=self._target_id)
        if isinstance(cmd, Command):
            extend.update({
                "sync": True,
                "max_timeout": cmd.max_timeout
            })
        else:
            extend.update({
                "sync": False
            })
        return self._session.send_command(target_cmd, **extend)

    def _handle_response(self, ret_json):
        # 同一个协议
        return self._session.connection._handle_response(ret_json)

    def _handle_event(self, ret_json) -> BaseEvent:
        # 同一个协议
        return self._session.connection._handle_event(ret_json)

    def close(self):
        self._session.close()