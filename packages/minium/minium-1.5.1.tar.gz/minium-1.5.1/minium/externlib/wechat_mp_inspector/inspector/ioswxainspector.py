'''
Author: yopofeng yopofeng@tencent.com
Date: 2023-10-31 20:52:17
LastEditors: yopofeng yopofeng@tencent.com
LastEditTime: 2023-11-10 17:36:05
FilePath: /wechat-mp-inspector/wechat_mp_inspector/inspector/ioswxainspector.py
Description: ios小程序wxa service线程inspector和各种页面类型的inspector
'''
from typing import Union
import re
from wechat_mp_inspector.protocol.wip import WIPSession
from .iosinspector import IOSInspectorSession
from ..protocol.wip import WebkitInspectorProtocol
from ..pages.safaripage import *

RunTimeDomain = WebkitInspectorProtocol.protocol.Runtime

class WxaInspector(IOSInspectorSession):
    CONTEXT_NAME = ()
    APPID_REG = r"Appid\[\w+\]"

    @classmethod
    def check_type(cls, title: str) -> Union['MainServiceInspector', 'AppserviceInspector', 'SkylineInspector']:
        """根据title判断类型

        :param str title: page.title
        """
        # title like:
        # MiniProgram[WeApp]_VMType[MainVM]_VMId[0]_ContextType[MainContext]_ContextId[0]_Appid[wx3eb9cfc5787d5458]_NickName[MiniTest云测试平台]_AppVersion[Debug]_PubVersion[3.2.0]
        for type_ in (MainServiceInspector, AppserviceInspector, SkylineInspector):
            for context_name in type_.CONTEXT_NAME:
                if title.find(context_name) >= 0:
                    return type_
                
    @classmethod
    async def create(cls, session: WIPSession, page: SafariAppServicePage):
        type_ = cls.check_type(page.title)
        inst: WxaInspector = await super(WxaInspector, type_).create(session)
        inst.appid = re.search(WxaInspector.APPID_REG, page.title)
        if inst.appid:
            inst.appid = inst.appid.group(0)
        return inst
                
    def __init__(self, session: WIPSession, target_id: str) -> None:
        super().__init__(session, target_id)
        self.appid = None

    def evaluate(self, expression: str, timeout=None, returnByValue=True, **kwargs):
        cmd = RunTimeDomain.evaluate(expression=expression, includeCommandLineAPI=True, returnByValue=returnByValue, **kwargs)
        
        return self.send_command(
            cmd,
            max_timeout=timeout
        ).result.result.value

class MainServiceInspector(WxaInspector):
    CONTEXT_NAME = ("ContextId[0]",)

class AppserviceInspector(WxaInspector): 
    CONTEXT_NAME = ("ContextId[2]",)

class SkylineInspector(WxaInspector): 
    CONTEXT_NAME = ("ContextId[3]",)

class WebviewInspector(IOSInspectorSession): ...

class H5Inspector(IOSInspectorSession): ...
