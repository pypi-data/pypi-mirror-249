#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@Time     : 2023/6/7 11:43
@Author   : ji hao ran
@File     : data_class.py
@Project  : StreamlitAntdComponents
@Software : PyCharm
"""
from dataclasses import dataclass
from typing import List, Literal, Union
from .setting import Color, MantineSize, MantineColor

__all__ = [
    'BsIcon',  # icon
    'Tag',  # component
    'StepsItem', 'ChipItem', 'CheckboxItem', 'ButtonsItem', 'SegmentedItem'
    , 'TabsItem', 'CasItem', 'MenuItem', 'TreeItem'  # data
]


@dataclass
class BsIcon:
    name: str


@dataclass
class Item:
    label: str = ''  # item label
    icon: str = None  # boostrap icon,https://icons.getbootstrap.com/
    disabled: bool = False  # disabled item


@dataclass
class Tag:
    label: str  # label
    color: Union[str, Color] = None  # color
    icon: str = None  # bootstrap icon
    link: str = None  # hyperlink
    bordered: bool = True  # show border
    radius: Union[MantineSize, int] = 'md'
    size: Union[MantineSize, int] = 'sm'
    closable: bool = False  # show close button


@dataclass
class StepsItem:
    title: str = ''
    subtitle: str = ''
    description: str = ''
    icon: str = None
    disabled: bool = False


@dataclass
class CheckboxItem:
    label: str = ''
    disabled: bool = False


@dataclass
class ChipItem(Item):
    pass


@dataclass
class NestedItem(Item):
    children: List = None  # item children

    @staticmethod
    def parse_tag(tag):
        if isinstance(tag, Tag):
            tag = tag.__dict__
        elif isinstance(tag, str):
            tag = Tag(tag).__dict__
        elif isinstance(tag, list):
            tag = [Tag(i).__dict__ if isinstance(i, str) else i.__dict__ for i in tag]
        return tag


@dataclass
class ButtonsItem(Item):
    href: str = None  # link address
    color: Union[MantineColor, str] = None  # button color


@dataclass
class SegmentedItem(Item):
    href: str = None  # link address


@dataclass
class TabsItem(Item):
    pass


@dataclass
class TreeItem(NestedItem):
    tag: Union[str, Tag] = None  # item tag
    description: str = None
    tooltip: str = None  # item tooltip

    @property
    def __dict__(self):
        d = super(TreeItem, self).__dict__
        d.update({'tag': self.parse_tag(self.tag)})
        return d


@dataclass
class CasItem(NestedItem):
    pass


@dataclass
class MenuItem(NestedItem):
    description: str = None
    href: str = None  # item link address
    tag: Union[str, Tag, List[Union[str, Tag]]] = None  # item tag
    type: Literal['group', 'divider'] = None  # item type
    dashed: bool = False  # divider line style,available when type=='divider'

    @property
    def __dict__(self):
        d = super(MenuItem, self).__dict__
        d.update({'tag': self.parse_tag(self.tag)})
        return d
