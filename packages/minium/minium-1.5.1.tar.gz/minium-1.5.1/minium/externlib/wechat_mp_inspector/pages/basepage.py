'''
Author: yopofeng
Date: 2023-09-27 23:41:11
LastEditors: yopofeng yopofeng@tencent.com
LastEditTime: 2023-10-31 17:47:53
FilePath: /wechat-mp-inspector/wechat_mp_inspector/driver/pages.py
Description: 定义各种page实例

Copyright (c) 2023 by ${git_name_email}, All Rights Reserved. 
'''

from dataclasses import dataclass
import re
from typing import Union, List, Mapping


@dataclass  
class BasePage:
    title: str = ''
    url: str = ''

class NormalPage(BasePage):
    unique_id = None
    empty = False

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, NormalPage):
            return False
        return self.unique_id == __value.unique_id
    
    def __str__(self) -> str:
        return f"id: {self.unique_id}, type: {self.__class__.__name__}, url: {self.url}, title: {self.title}"

class WebViewPage(NormalPage):
    appid: str = ''
    path: str = ''
    visible: bool = None
    initial: bool = False

class AppServicePage(NormalPage):
    appid = ''

