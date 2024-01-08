'''
Author: yopofeng yopofeng@tencent.com
Date: 2023-09-22 18:52:16
LastEditors: yopofeng yopofeng@tencent.com
LastEditTime: 2023-11-13 10:54:59
FilePath: /wechat-mp-inspector/wechat_mp_inspector/protocol/basesession.py
Description: 定义协议session
'''
import abc
import typing
import threading
from .baseprotocol import BaseProtocol, CommandType, BaseEvent, Command, AsyncCommand
from .protocolcommand import ProtocolCommand
from ..connection.baseconn import BaseConnection
from ..command import CommandType
from ..event import BaseEvent
from ..logger import logger

class BaseSession(metaclass=abc.ABCMeta):
    id_: str
    @abc.abstractmethod
    def send_command(self, data: dict or CommandType): pass

    @abc.abstractmethod
    def on(self, event: str or BaseEvent, callback: typing.Callable): pass

    @abc.abstractmethod
    def close(self): ...

    @abc.abstractmethod
    def remove_listener(self, event: str or BaseEvent, callback: typing.Callable): ...

    @abc.abstractmethod
    def remove_all_listeners(self): ...


class BaseWebkitSession(BaseSession):
    protocol: BaseProtocol
    def __init__(self, session_id: str, connection: BaseConnection) -> None:
        self.id_ = session_id
        self._id = str(id(self))
        self._msg_id_lock = threading.Lock()
        self._msg_id = 1
        self.connection = connection
        self.logger = getattr(connection, "logger", logger)
        # connection采用单实例模式, 使用链接的id可以避免id重复问题
        self._use_conn_id = hasattr(self.connection, "get_command_id")

    def get_command_id(self):
        """生成命令id

        :return int: 唯一的命令id
        """
        if self._use_conn_id:
            return self.connection.get_command_id()
        with self._msg_id_lock:
            self._msg_id += 1
            return self._msg_id
        
    def _gen_command(self, command: str or ProtocolCommand or CommandType, params: dict=None, max_timeout=None, sync=True, ignore_response=False) -> CommandType:
        cmd = None
        if sync:
            if isinstance(command, Command):
                cmd = command
            elif isinstance(command, AsyncCommand):
                cmd = Command(command.method, command.params, desc=command.desc, max_timeout=max_timeout)
            elif isinstance(command, ProtocolCommand):
                cmd = Command(command._method, command._arguments, max_timeout=max_timeout)
        else:
            if isinstance(command, AsyncCommand):
                cmd = command
            elif isinstance(command, Command):
                cmd = AsyncCommand(command.method, command.params, desc=command.desc, ignore_response=ignore_response)
                del command  # 删除监听函数
            elif isinstance(command, ProtocolCommand):
                cmd = AsyncCommand(command._method, command._arguments, ignore_response=ignore_response)
        if cmd is None:
            try:
                cmd = self.protocol.get_command(command, params, sync=sync, max_timeout=max_timeout, ignore_response=ignore_response)
            except TypeError as te:
                self.logger.warning(str(te), exc_info=True)
                # 兜底 #
                if sync:
                    cmd = Command(command, params, max_timeout=max_timeout)
                else:
                    cmd = AsyncCommand(command, params, ignore_response=ignore_response)
        if not cmd.id:
            cmd.id = self.get_command_id()
        cmd.conn_id = self._id
        return cmd
