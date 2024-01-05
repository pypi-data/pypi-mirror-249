#####################################################################
# File: ecmb_navigation_base.py
# Copyright (c) 2023 Clemens K. (https://github.com/metacreature)
# 
# MIT License
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#####################################################################

from typing import Self, Callable
from abc import ABC, abstractmethod
from lxml import etree
from .ecmb_enums import *
from .ecmb_utils import ecmbUtils
from .ecmb_content_folder import ecmbContentFolder
from .ecmb_content_image import ecmbContentImage


class ecmbNavigationBase(ABC):

    _book_obj = None
    _parent_navigation_obj = None
    _label = None
    _title = None
    _target_image_obj = None
    _target_image_side = None

    def set_title(self, title:str) -> None:
        """set_title 

        :param title: the hover-text of the node
        :type title: str

        """    
        ecmbUtils.validate_str_or_none(True,  'title', title)
        self._title = title


    def int_set_parent(self, parent_navigation_obj: Self) -> None:
        if self._parent_navigation_obj != None:
            ecmbUtils.raise_exception(f'the navigation-object with the label "' + self._label + '" can\'t be added twice!', 1)
        self._parent_navigation_obj = parent_navigation_obj

        
    def int_get_parent_chapters_folder(self) -> ecmbContentFolder:
        if self._parent_navigation_obj:
            return self._parent_navigation_obj.int_get_parent_chapters_folder()
        return None


    def _init(self, book_obj, label: str, title: str) -> None:
        if not 'ecmbBook' in str(type(book_obj)):
            ecmbUtils.raise_exception(f'ecmbBook expected, but got diffrent type!', 1)
        
        ecmbUtils.validate_not_empty_str(True,  'label', label, 1)
        ecmbUtils.validate_str_or_none(True,  'title', title, 1)

        self._book_obj = book_obj
        self._label = label
        self._title = title


    def _set_target(self, origin: str, target: str|ecmbContentImage, target_side: TARGET_SIDE) -> None:
        target_side = ecmbUtils.enum_value(target_side)
        if target_side:
            if not ecmbUtils.validate_enum(False, 'target_side', target_side, TARGET_SIDE, 1):
                ecmbUtils.raise_exception('target_side has to be one of these values: "'+ '","'.join(ecmbUtils.enum_values(TARGET_SIDE))+ f'" at {origin} "' + self._label + '"!', 1)

        target_image_obj = None
        if type(target) == ecmbContentImage or (type(target) == str and target != ''):
            target_image_obj = self._book_obj.int_get_content(target) 
            if not target_image_obj:
                ecmbUtils.raise_exception(f'the given target was not found in the book at {origin} "' + self._label + '"!', 1)
        else:
            ecmbUtils.raise_exception(f'target must be either an unique_id or an ecmbContentImage at {origin} "' + self._label + '"!', 1)

        if type(target_image_obj) != ecmbContentImage:
            ecmbUtils.raise_exception(f'target is not an ecmbContentImage at {origin} "' + self._label + '"!', 1)

        self._target_image_obj = target_image_obj
        self._target_image_side = target_side


    @abstractmethod
    def int_validate(self, warnings: bool|Callable) -> bool:
        pass


    @abstractmethod
    def int_build(self) -> etree.Element:
        pass