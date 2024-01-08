'''
Author: yopofeng yopofeng@tencent.com
Date: 2023-10-11 11:52:33
LastEditors: yopofeng yopofeng@tencent.com
LastEditTime: 2023-10-31 20:52:07
FilePath: /wechat-mp-inspector/wechat_mp_inspector/inspector/wxainspector.py
Description: 安卓小程序wxa service线程inspector和各种页面类型的inspector
'''
import time
import typing
from dataclasses import dataclass
from ..protocol.cdp import CDPSession, ChromeInspectorProtocol
from .baseinspector import BaseInspector
from .androidinspector import AndroidInspector
from ..connection.baseconn import BaseConnection
from ..logger import logger
from ..utils import Callback, Object
from ..exception import *
from ..pages.basepage import *
if typing.TYPE_CHECKING:
    from ..pages.chromepage import *
    from ..pages.safaripage import *

__all__ = [
    'WxaInspector',
    'MainServiceInspector',
    'AppserviceInspector',
    'SkylineInspector',
    'WebviewInspector',
    'H5Inspector'
]

class Runtime(object):
    TMP = set()
    domain = ChromeInspectorProtocol.protocol.Runtime
    def __init__(self, session: CDPSession, ) -> None:
        self.session = session
        if session.connection.id not in Runtime.TMP:
            self._test_pong()
            Runtime.TMP.add(session.connection.id)
            
    def _test_pong(self):
        """5s一次来自inpector的pong信息"""
        _id = self.session.send_command(
            self.domain.addBinding(name="test_pong"), sync=False
        )
        self.session.connection._ee.once(
            _id,
            lambda *args: self.session.send_command(self.domain.evaluate(expression="""setInterval(function(){typeof test_pong !== "undefined" && test_pong(new Date().toString().slice(0, 24))}, 5000)"""), sync=False)
        )

    def add_binding(self, name):
        return self.session.send_command(
            self.domain.addBinding(name=name)
        )

    def discard_console(self):
        """
        Runtime.discardConsoleEntries
        异步即可
        """
        self.session.connection.ignore_method.add("Runtime.consoleAPICalled")
        return self.session.send_command(
            self.domain.discardConsoleEntries(),
            sync=False,
            ignore_response=True
        )

    def disable(self):
        """Runtime.disable"""
        return self.session.send_command(self.domain.disable())

    def enable(self):
        """Runtime.enable"""
        return self.session.send_command(self.domain.enable())
    
    def evaluate(
        self,
        expression: str,
        contextId=None,
        uniqueContextId=None,
        timeout=None,
        returnByValue=True,
        **kwargs
    ):
        cmd = self.domain.evaluate(expression=expression, includeCommandLineAPI=True, returnByValue=returnByValue, **kwargs)
        if uniqueContextId:
            cmd.uniqueContextId = uniqueContextId
        elif contextId:
            cmd.contextId = contextId
        return self.session.send_command(cmd, max_timeout=timeout).result.result.value

    
    def on(self, event, callback: Callback = None) -> Callback:
        if callback is None:
            _callback = Callback()
        elif isinstance(callback, Callback):
            _callback = callback
        else:
            _callback = Callback(callback)
        self.session.on("Runtime." + event, _callback.callback)
        return _callback

class WxaInspector(AndroidInspector):
    CONTEXT = {}  # session.connection.id -> context_map[name -> (context_id, context_unique_id)]
    CONTEXT_NAME = ()
    context_created_callback = None
    logger = logger.getChild("WxaService")

    @classmethod
    def listenContextCreated(cls, session: CDPSession):
        cls.logger.info("start listen context created")
        runtime = Runtime(session)

        def executionContextCreated(context_info: ChromeInspectorProtocol.protocol.Runtime.executionContextCreated):
            cls.logger.info(f"context info: {context_info}")
            cls.CONTEXT[session.connection.id][context_info.context.name] = (
                context_info.context.id,
                context_info.context.uniqueId,
            )

        runtime.discard_console()
        # enable只有第一次执行会回调现有的context内容, 先disable
        runtime.disable()
        cls.CONTEXT[session.connection.id] = {}
        cls.context_created_callback = runtime.on(
            "executionContextCreated", executionContextCreated
        )
        runtime.enable()

    def __init__(self, session: CDPSession) -> None:
        super().__init__(session)
        self.runtime = Runtime(session)
        self.context_id = None
        self.context_unique_id = None
        if session.connection.id in WxaInspector.CONTEXT:  # 已经建立了监听等操作
            context_map = WxaInspector.CONTEXT[session.connection.id]
            for context_name in self.__class__.CONTEXT_NAME:
                if context_name in context_map:
                    self.context_id, self.context_unique_id = context_map[context_name]
            if not self.inited:  # context还没有创建, 注册监听
                self.logger.warning(
                    "%s context not init, listen them"
                    % (" or ".join(self.__class__.CONTEXT_NAME))
                )
                self.context_created_callback = self.runtime.on(
                    "executionContextCreated", self.onContextCreated
                )
        else:
            self.context_created_callback = self.runtime.on(
                "executionContextCreated", self.onContextCreated
            )
            WxaInspector.listenContextCreated(session)

    @property
    def inited(self):
        return bool(self.context_id or self.context_unique_id)

    def ensure_init(self):
        if not self.inited:
            self.logger.warning(
                "%s context not init" % (" or ".join(self.__class__.CONTEXT_NAME))
            )
            return False
        return True
    
    def wait_init(self, timeout=0):
        if self.inited:
            return True
        if not self.context_created_callback:
            self.logger.warning("not listened")
            return False
        stime = time.time()
        while self.context_created_callback.acquire(
            max(timeout - (time.time() - stime), 0)
        ):
            if self.inited:
                return True
        return False
    
    @property
    def is_connecting(self):
        try:
            return self.evaluate(
                "typeof __wxConfig__ !== 'undefined' ? true: false", timeout=5
            )
        except TimeoutError:
            self.logger.warning(f"WxaServiceDriver thread maybe disconnected: [{self._session.connection._url}]")
            return False

    def onContextCreated(self, context_info: ChromeInspectorProtocol.protocol.Runtime.executionContextCreated):
        if context_info.context.name in self.__class__.CONTEXT_NAME:
            self.context_id = context_info.context.id
            self.context_unique_id = context_info.context.uniqueId

    def evaluate(self, expression: str, timeout=None, **kwargs):
        if not self.ensure_init():
            return
        return self.runtime.evaluate(
            expression, self.context_id, self.context_unique_id, timeout, **kwargs
        )


class MainServiceInspector(WxaInspector):
    CONTEXT_NAME = ("MainContext",)

    def __init__(self, session: CDPSession or WxaInspector) -> None:
        if isinstance(session, WxaInspector):
            super().__init__(session._session)
        else:
            super().__init__(session)
        if not self.context_id:
            self.context_id = 1  # 主context默认id == 1


class CurrentPage(Object):
    route: str = ''
    webviewId: str = ''
    renderer: str = ''
    exparserNodeId: str = ''
    url: str = ''

class AppserviceInspector(WxaInspector):
    CONTEXT_NAME = ("SubContext-2",)

    def __init__(self, session: CDPSession or WxaInspector) -> None:
        if isinstance(session, WxaInspector):
            super().__init__(session._session)
        else:
            super().__init__(session)

    def _get_current_page(self) -> CurrentPage:
        js = """(function(){
        var i = getCurrentPages().pop()
        return {
            "route": i.route,
            "webviewId": i.__wxWebviewId__,
            "renderer": i.renderer,
            "exparserNodeId": i.__wxExparserNodeId__
        }})()"""
        try:
            return CurrentPage(**self.evaluate(js))
        except Exception as e:
            if str(e) == "uniqueContextId not found":
                raise UniqueContextIdNotFound(str(e))
            raise

    @property
    def current_page(self):
        return self._get_current_page()


class SkylineInspector(WxaInspector):
    CONTEXT_NAME = ("SubContext-3", "app_sub_render")

    def __init__(self, session: CDPSession or WxaInspector) -> None:
        if isinstance(session, WxaInspector):
            super().__init__(session._session)
        else:
            super().__init__(session)


class PageInspector(AndroidInspector):
    def __init__(self, session: CDPSession) -> None:
        super().__init__(session)
        self.runtime = Runtime(session)

    def evaluate(self, expression, **kwargs):
        return self.runtime.evaluate(expression, **kwargs)

class WebviewInspector(PageInspector):
    """小程序的webview页面"""
    def __init__(self, session: CDPSession, page: 'ChromeWebViewPage' or 'SafariWebViewPage'=None) -> None:
        super().__init__(session)
        self.page = page
        self._is_webview = None

    @property
    def is_webview(self):
        """是否是web-view页面"""
        if self._is_webview is None:
            self._is_webview = self.runtime.evaluate(
                """document.querySelector("wx-web-view") ? true : false"""
            )
        return self._is_webview
    
class H5Inspector(PageInspector):
    """普通h5"""
    def __init__(self, session: CDPSession, page: 'ChromeNormalPage' or 'SafariNormalPage'=None) -> None:
        super().__init__(session)
        self.page = page
        self.runtime = Runtime(session)

    @property
    def hidden(self):
        return self.runtime.evaluate("document.hidden")