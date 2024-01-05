#####################################################################
# File: ecmb_navigation_link.py
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

import re
from typing import Callable
from lxml import etree
from .ecmb_enums import *
from .ecmb_utils import ecmbUtils
from .ecmb_navigation_base import ecmbNavigationBase
from .ecmb_content_image import ecmbContentImage


class ecmbNavigationLink(ecmbNavigationBase):
    """ecmbNavigationLink 

    The target-image has to be part of its parent chapter's folder. If you are pointing to a double-page-image you can define if it should point to the left or right part (defaults to auto).

    :param book_obj:
    :type book_obj: ecmbBook
    :param label: a label 
    :type label: str 
    :param target: a image-object or a unique-id pointing to a image
    :type target: str | ecmbContentImage
    :param target_side: the side of a double-page-image
    :type target_side: TARGET_SIDE, optional
    :param title: the hover-text of the link
    :type title: str, optional
    """    

    def __init__(self, book_obj, label: str, target: str|ecmbContentImage, target_side: TARGET_SIDE = TARGET_SIDE.AUTO, title:str = None):
        super()._init(book_obj, label, title)
        super()._set_target('navigation-link', target, target_side)


    def int_validate(self, warnings: bool|Callable) -> bool:
        parent_folder_obj = self._parent_navigation_obj.int_get_parent_chapters_folder()
        if parent_folder_obj and not parent_folder_obj.int_contains(self._target_image_obj):
            ecmbUtils.raise_exception('given target-image  is not part of parent chapter\'s target-folder at link "' + self._label + '"!')
        return True
    

    def int_build(self) -> etree.Element:
        if not self.int_validate(False):
            return
        
        main_node = etree.Element('link')
        main_node.set('label', self._label)
        if self._title:
            main_node.set('title', self._title)

        image_link = self._target_image_obj.int_get_image_path(self._target_image_side)

        parent_folder_obj = self._parent_navigation_obj.int_get_parent_chapters_folder()
        if parent_folder_obj:
            parent_folder_link = parent_folder_obj.int_get_build_path()
            image_link = re.sub('^'+parent_folder_link, '', image_link)

        main_node.set('href', image_link)
        
        return main_node