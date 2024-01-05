#####################################################################
# File: ecmb_navigation_chapter.py
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
from typing import  Callable
from lxml import etree
from .ecmb_enums import *
from .ecmb_utils import ecmbUtils
from .ecmb_navigation_base_sub import ecmbNavigationBaseSub
from .ecmb_content_folder import ecmbContentFolder
from .ecmb_content_image import ecmbContentImage


class ecmbNavigationChapter(ecmbNavigationBaseSub):
    """ecmbNavigationChapter

    You can define a target-image, which could be any image as long its part of this chapter's folder (default is the first image of the folder).  If you are pointing to a double-page-image you can define if it should point to the left or right part (defaults to auto).

    :param book_obj:
    :type book_obj: ecmbBook
    :param label: a label
    :type label: str
    :param folder: a folder-object or a unique-id pointing to a folder
    :type folder: str | ecmbContentFolder
    :param target: a image-object or a unique-id pointing to a image
    :type target: str | ecmbContentImage, optional
    :param target_side: the side of a double-page-image
    :type target_side: TARGET_SIDE, optional
    :param title: the hover-text of the chapter
    :type title: str, optional
    """       

    _target_folder_obj = None

    def __init__(self, book_obj, label: str, folder: str|ecmbContentFolder, target: str|ecmbContentImage = None, target_side: TARGET_SIDE = TARGET_SIDE.AUTO, title:str = None):
        super()._init(book_obj, label, title)
        if target != None:
            super()._set_target('chapter', target, target_side)

        target_folder_obj = None
        if type(folder) == ecmbContentFolder or type(folder) == str and folder != '':
            target_folder_obj = self._book_obj.int_get_content(folder)
            if not target_folder_obj:
                ecmbUtils.raise_exception('the given folder was not found in the book at chapter "' + self._label + '"!')
        else:
            ecmbUtils.raise_exception('folder must be either an unique_id or an ecmbContentFolder at chapter"' + self._label + '"!')

        if type(target_folder_obj) != ecmbContentFolder:
            ecmbUtils.raise_exception('folder is not an ecmbContentFolder at chapter"' + self._label + '"!')

        self._target_folder_obj = target_folder_obj


    def int_validate(self, warnings: bool|Callable) -> bool:
        self._target_folder_obj.int_validate(False)
               
        if self._target_image_obj and not self._target_folder_obj.int_contains(self._target_image_obj):
            ecmbUtils.raise_exception('given target-image is not part of the chapter\'s target-folder at chapter "' + self._label + '"!')

        parent_folder_obj = self._parent_navigation_obj.int_get_parent_chapters_folder()
        if parent_folder_obj and not parent_folder_obj.int_contains(self._target_folder_obj):
            ecmbUtils.raise_exception('the target-folder is not part of parent chapter\'s target-folder at  chapter "' + self._label + '"!')

        super().int_validate(warnings)
        return True
    

    def int_build(self) -> etree.Element:
        if not self.int_validate(False):
            return
        
        main_node = etree.Element('chapter')
        main_node.set('label', self._label)
        if self._title:
            main_node.set('title', self._title)


        folder_link = self._target_folder_obj.int_get_build_path()

        if not self._target_image_obj:
            image_obj = self._target_folder_obj.int_get_first_image()
            image_link = image_obj.int_get_image_path()
        else:
            image_link = self._target_image_obj.int_get_image_path(self._target_image_side)

        image_link = re.sub('^'+folder_link, '', image_link)

        parent_folder_obj = self._parent_navigation_obj.int_get_parent_chapters_folder()
        if parent_folder_obj:
            parent_folder_link = parent_folder_obj.int_get_build_path()
            folder_link = re.sub('^'+parent_folder_link, '', folder_link)

        main_node.set('dir', folder_link)
        main_node.set('href', image_link)
        

        for child in self._children:
            child_node = child.int_build()
            if child_node != None:
                main_node.append(child_node)
        
        return main_node
    

    def int_get_parent_chapters_folder(self) -> ecmbContentFolder:
        return self._target_folder_obj
    
