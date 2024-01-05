#####################################################################
# File: ecmb_content_folder.py
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

import zipfile
from lxml import etree
from typing import Callable
from .ecmb_utils import ecmbUtils
from .ecmb_content_base_sub import ecmbContentBaseSub
from .ecmb_content_image import ecmbContentImage

class ecmbContentFolder(ecmbContentBaseSub):
    """ecmbContentFolder

    If you want to use chapters (and subchapters) in navigation you have to organize the images in folders, coz a chapter points to a folder.

    :note:
    * because the class will generate internal names no name is necesary
    * provide a unique-id if you want to access this folder easily later at navigation

    :param book_obj:
    :type book_obj: ecmbBook
    :param unique_id: provide a unique-id if you want to access this folder easily later at navigation
    :type unique_id: str, optional 
    """    

    _contents = None

    def __init__(self, book_obj, unique_id: str = None):
        self._init(book_obj, unique_id)
        self._contents = []


    def int_validate(self, warnings: bool|Callable) -> bool:
        found = False
        for content in self._contents:
            if content.int_validate(warnings):
                found = True

        if not found:
            ecmbUtils.raise_exception('folder with the unique_id "' + self._unique_id + '" is empty!')
        return found


    def int_build(self, target_file: zipfile.ZipFile) -> etree.Element:
        if not self.int_validate(False):
            return
        
        self._build_id = self._book_obj.int_get_next_build_id()
        main_node = etree.Element('dir')
        main_node.set('name', self._build_id )

        target_file.mkdir(self.int_get_build_path(False))

        for content in self._contents:
            content_node = content.int_build(target_file)
            if content_node != None:
                main_node.append(content_node)
        
        return main_node


    def int_get_first_image(self) -> ecmbContentImage:
        for content in self._contents:
            if type(content) == ecmbContentImage:
                return content
            image = content.int_get_first_image()
            if image:
                return image


        
