from functools import partialmethod
import logging
from ..utils import Object


class InitDefault(type):
    def __new__(cls, name, base, attr_dict):
        kwargs = {}
        for k, v in attr_dict.items():
            if k.startswith("_"):
                continue
            kwargs[k] = v
        new_cls = super().__new__(cls, name, base, attr_dict)
        src_init = new_cls.__init__
        new_cls.__init__ = partialmethod(src_init, **kwargs)
        return new_cls


class BaseConfig(Object, metaclass=InitDefault):
    _unique_key_ = ""  # format for str(self)
    logger_level = logging.INFO

    def __str__(self) -> str:
        if not self.__class__._unique_key_:
            return super().__str__()
        return self.__class__._unique_key_ % self


class AndroidConfig(BaseConfig):
    _unique_key_ = "%(serial)s"
    serial = None  # 设备udid


class IOSConfig(BaseConfig):
    udid = None  # 设备udid
    connect_timeout = 30  # 链接超时时间
    bundle = None  # 目标app
    wait_for_app_timeout = 180  # 等待app连接服务时间


class MPConfig(BaseConfig):
    _unique_key_ = "%(appid)s"
    platform = None
    appid = ""
    skyline = True
    webview = True
    h5 = True
    timeout = 20  # 检测appservice的超时时间
    sock_cache = True  # 把sock name => pid 缓存起来(如果sock重新实例化有一定风险)
    init_page_info = False  # 尝试获取webview页面的page info
    cmd_timeout = 20  # 指令默认超时时间


class AndroidMP(MPConfig, AndroidConfig):
    platform = "android"

    def __init__(self, __map=None, **kwargs):
        MPConfig.__init__(self, __map, **kwargs)
        AndroidConfig.__init__(self, __map, **kwargs)


class IOSMP(MPConfig, IOSConfig):
    platform = "ios"

    def __init__(self, __map=None, **kwargs):
        MPConfig.__init__(self, __map, **kwargs)
        IOSConfig.__init__(self, __map, **kwargs)
