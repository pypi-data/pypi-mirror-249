'''
Author: yopofeng yopofeng@tencent.com
Date: 2023-09-11 17:08:57
LastEditors: yopofeng yopofeng@tencent.com
LastEditTime: 2023-11-13 10:53:21
FilePath: /wechat-mp-inspector/wechat_mp_inspector/session/basesession.py
Description: 类websocket的会话实现, 支持发送消息以及监听回调
'''
import abc
from typing import Tuple, Dict, Any, List, Callable
import time
from enum import Enum
import threading
from ..logger import logger
from ..emitter import MyEventEmitter
from ..utils import json2obj, Object, ProcessSafeEventLoop, AsyncCondition, AsyncCallback
from ..command import CommandType, Command, AsyncCommand
from ..event import BaseEvent
from asyncio.coroutines import iscoroutine
import asyncio
import json

class AbstractConnection(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def send_command(self, data: dict or CommandType): pass

    @abc.abstractmethod
    def on(self, event: str or BaseEvent, callback: Callable): pass


class BaseConnection(AbstractConnection):
    """
    子类通过
    1. 调用`_on_message`实现回包消息处理
    2. 调用`send`和`send_async`实现同步和异步命令发送
    
    3. `on`可监听事件
    """
    def __init__(self, loop: asyncio.AbstractEventLoop=None) -> None:
        self._id = str(id(self))
        self.logger = logger.getChild(f"Conn{self._id[-4:]}")

        self._ee = MyEventEmitter()
        self._msg_lock = threading.Condition()  # 信息锁
        self._sync_wait_map = {}  # 同步消息kv表, id -> result
        self._async_msg_map: Dict[str or int, AsyncCommand] = {}  # 异步命令kv表, id -> AsyncCommand
        self._method_wait_map = {}  # 等待命令kv表, method -> result
        self._observers: Dict[str, List[Callable]] = {}  # 监听表, method -> handler(callback function)
        # event loop 用来处理on message回调中的异步函数
        if loop:
            self._event_loop = ProcessSafeEventLoop(loop)
        else:
            self._event_loop = ProcessSafeEventLoop()
            # events._set_running_loop(self._event_loop.loop)

        
    def _on_message(self, message):
        """接收json like会包信息, 尽量不要有阻塞操作"""
        self.logger.debug("RECV < %.510s" % message)
        ret_json = json2obj(message)
        if not ret_json:
            return
        req_id, result = self.handle_message(ret_json)
        if req_id:
            if req_id in self._sync_wait_map:
                self._sync_wait_map[req_id] = result
                self._notify()
            else:
                self._handle_async_msg(req_id, result)
                self._notify()
        elif isinstance(result, BaseEvent):
            if result.event_name in self._method_wait_map:
                self._method_wait_map[result.event_name] = result
                self._notify()
            else:
                self.notify(result)

    def send(self, cmd: Command, **extend):
        # 同步发送消息，函数会阻塞
        with cmd:
            self._sync_wait_map[cmd.id] = None  # 该ID未有返回message
            self._safely_send(cmd, **extend)
            return self._receive_response(cmd)

    def send_async(
        self, cmd: AsyncCommand, ignore_response=False, **extend
    ) -> str:
        if not ignore_response:
            self._async_msg_map[cmd.id] = cmd
        try:
            self._safely_send(cmd, **extend)
        except ConnectionAbortedError:
            if not ignore_response:
                self._async_msg_map.pop(cmd.id)
            del cmd
            raise
        return cmd.id

    def create_async_callback_task(self, callback, *args):
        # self.logger.warn("create_async_callback_task: %s" % callback.__name__)
        async def _callback(*_args):
            # self.logger.warn("@async call %s" % callback.__name__)
            ret = callback(*_args)
            if iscoroutine(ret):
                return await ret
            return ret
        if isinstance(callback, AsyncCallback):
            return self._event_loop.run_coroutine(callback.set_result(args))
        self._event_loop.run_coroutine(_callback(*args))

    def notify(self, event: BaseEvent):
        """通知事件

        :param BaseEvent event: 事件
        """
        if event.event_name in self._observers:
            for callback in self._observers[event.event_name]:
                self.create_async_callback_task(callback, event.params)
        else:
            return

    def _notify(self):
        self._msg_lock.acquire()
        self._msg_lock.notify_all()  # 全部唤醒，让其自己决定是否需要重新wait
        self._msg_lock.release()

    def _wait(self, cmd: Command):
        """等待命令"""
        stime = time.time()
        self._msg_lock.acquire()
        ret = self._msg_lock.wait(cmd.max_timeout)  # 如果是因为其他命令的返回触发了notify，需要重新等待
        self._msg_lock.release()
        etime = time.time()
        if etime - stime >= cmd.max_timeout:
            cmd.max_timeout = 0
        else:
            cmd.max_timeout = cmd.max_timeout - (etime - stime)  # 剩余要等待的时间
        return ret

    
    def _check_conn_exception(self, cmd: Command):
        """检查链接异常状态, 决定命令是否继续[等待]

        :param Command cmd: 指令
        """
        pass
    
    def _receive_response(self, cmd: Command):
        # 等待接收到message的通知
        while cmd.max_timeout > 0:
            if (
                cmd.id in self._sync_wait_map
                and self._sync_wait_map[cmd.id] is not None
            ):  # 不等待就获取到数据了, 这个recv太快了吧
                self.logger.info("🚀🚀🚀🚀🚀🚀🚀火速获取到返回导致处理不过来🚀🚀🚀🚀🚀🚀🚀")
                response = self._sync_wait_map.pop(cmd.id)
                if isinstance(response, Exception):
                    raise response
                return response
            self._wait(cmd)

            if (
                cmd.id in self._sync_wait_map
                and self._sync_wait_map[cmd.id] is not None
            ):  # 获取到了数据
                response = self._sync_wait_map.pop(cmd.id)
                if isinstance(response, Exception):
                    raise response
                return response
            try:
                self._check_conn_exception(cmd)
            except:
                if cmd.id in self._sync_wait_map:
                    del self._sync_wait_map[cmd.id]
                raise
            if cmd.max_timeout > 0:  # 线程是被其他消息唤醒，重新等待
                self.logger.debug("rewait for %s" % cmd.id)
                continue
            else:
                if cmd.id in self._sync_wait_map:
                    del self._sync_wait_map[cmd.id]
                # test_link(self._url)  # 出现超时的情况, 尝试另外建立链接看看是不是inspector问题
                if cmd.reason and isinstance(cmd.reason, ConnectionAbortedError):
                    raise TimeoutError(
                        f"[{cmd.id}][{cmd.desc}] command timeout cause by {cmd.reason}"
                    )
                raise TimeoutError(
                    f"[{cmd.id}][{cmd.desc}] receive from remote timeout"
                )

    def _handle_async_msg(self, req_id, ret_json):
        """处理异步指令"""
        self.logger.info(
            "received async msg: %s%s",
            req_id,
            "" if req_id in self._async_msg_map else ", maybe command ignore response",
        )
        if ret_json is None:
            self.logger.warning("async msg[%s] response is None" % req_id)
        if self._ee.emit(req_id, ret_json):  # 有监听回调
            if req_id in self._async_msg_map:
                self._async_msg_map.pop(req_id)
        elif req_id in self._async_msg_map:  # 是这个实例发出的指令
            self._async_msg_map[req_id].result = ret_json

    def get_aysnc_msg_return(self, msg_id=None):
        if not msg_id:
            self.logger.warning(
                "Can't get msg without msg_id, you can get msg_id when calling send_async()"
            )
            return None
        if msg_id in self._async_msg_map and isinstance(self._async_msg_map[msg_id], AsyncCommand):
            response = self._async_msg_map[msg_id].result
            if response is not None:
                self._async_msg_map.pop(msg_id)
            if isinstance(response, Exception):
                raise response
            return response
        return None

    def handle_message(self, ret_json) -> Tuple[str, Any]:
        req_id, result = self._handle_response(ret_json)
        if not req_id:
            result = self._handle_event(ret_json)
        return req_id, result

    def on(self, event: str or BaseEvent, callback: Callable or AsyncCallback):
        """监听事件

        :param str event: 事件名
        :param function callback: 回调函数
        """
        if not callable(callback) and not isinstance(callback, AsyncCallback):
            raise TypeError(
                "callback[type %s] is not a callable object" % type(callback)
            )
        if isinstance(event, BaseEvent):
            event = event.event_name
        if event not in self._observers:
            self._observers[event] = []
        if callback not in self._observers[event]:
            self._observers[event].append(callback)

    def remove_listener(self, event, callback):
        """移除监听事件

        :param str event: 事件名
        :param function callback: 回调函数
        """
        if event in self._observers.keys():
            if callback is None:  # remove all callback
                del self._observers[event]
            elif callback in self._observers[event]:
                self._observers[event].remove(callback)
        else:
            self.logger.debug("remove key which is not in observers")

    def remove_all_listeners(self):
        try:
            obs_list = [x for x in self._observers.keys()]
            for obs in obs_list:
                del self._observers[obs]
        except Exception as e:
            raise KeyError(e)

    def send_command(self, cmd: CommandType, **extend):
        if isinstance(cmd, Command):
            return self.send(cmd, **extend)
        return self.send_async(cmd, **extend)

    @abc.abstractclassmethod
    def _safely_send(self, cmd: CommandType, **extend):
        """真实发送消息的方法"""
        pass

    @abc.abstractmethod
    def _handle_response(self, ret_json) -> Tuple[str, Any]: ...

    @abc.abstractmethod
    def _handle_event(self, ret_json) -> BaseEvent: ...

class BaseAsyncConnection(BaseConnection):
    def __init__(self, loop: asyncio.AbstractEventLoop = None) -> None:
        super().__init__(loop)
        self._async_msg_lock = AsyncCondition()

    # connection中有在主线程使用了async接口的情况下, send_command不能有非async阻塞操作
    # _receive_response中等待和通知接口需要进行异步重构

    @abc.abstractmethod
    def await_(self, awaitable): ...

    def _wait(self, cmd: Command):
        """重构试用异步等待"""
        return self.await_(self._async_wait(cmd))

    def _notify(self):
        """重构使用异步通知"""
        return self._event_loop.run_coroutine(self._async_notify())
    
    async def _async_wait(self, cmd: Command):
        stime = time.time()
        await self._async_msg_lock.acquire()
        ret = await self._async_msg_lock.wait(timeout=cmd.max_timeout)
        self._async_msg_lock.release()
        etime = time.time()
        if etime - stime >= cmd.max_timeout:
            cmd.max_timeout = 0
        else:
            cmd.max_timeout = cmd.max_timeout - (etime - stime)  # 剩余要等待的时间
        return ret
    
    async def _async_notify(self):
        await self._async_msg_lock.acquire()
        self._async_msg_lock.notify_all()
        self._async_msg_lock.release()

    async def _get_aysnc_msg_return(self, msg_id=None, timeout=Command.max_timeout):
        """等待异步消息返回

        :param str msg_id: 消息id, defaults to None
        :param int timeout: 最长等待时间, defaults to Command.max_timeout
        :raises response: 消息错误
        :return any: 消息结果
        """
        if not msg_id:
            self.logger.warning(
                "Can't get msg without msg_id, you can get msg_id when calling send_async()"
            )
            return None
        if msg_id in self._async_msg_map and isinstance(self._async_msg_map[msg_id], AsyncCommand):
            acmd = self._async_msg_map[msg_id]
            response = acmd.result
            if response is not None:  # 有结果
                self._async_msg_map.pop(msg_id)
            elif timeout >= 0:
                cmd = Command(acmd.method, acmd.params, max_timeout=timeout)
                while cmd.max_timeout > 0:
                    await self._async_wait(cmd)
                    if acmd.result is not None:
                        response = acmd.result
                        if acmd.id in self._async_msg_map:
                            self._async_msg_map.pop(msg_id)
                        break
            if isinstance(response, Exception):
                raise response
            return response
        return None

    def get_aysnc_msg_return(self, msg_id=None, timeout=Command.max_timeout):
        return self._event_loop.run_coroutine(self._get_aysnc_msg_return(msg_id, timeout)).result()

class STATE(Enum):
    CLOSE = 1  # 链接关闭
    OPEN = 2  # 链接连通
    PEDING = 3  # 链接连接中
    RECONNECTING = 4  # 重新链接中
    INIT = 5
