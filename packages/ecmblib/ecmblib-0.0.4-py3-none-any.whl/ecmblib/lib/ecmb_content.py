#####################################################################
# File: ecmb_content.py
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
from typing import Callable
from io import BytesIO
from lxml import etree
from .ecmb_utils import ecmbUtils
from .ecmb_content_base_sub import ecmbContentBaseSub


class ecmbContent(ecmbContentBaseSub):
    """ecmbContent

    This is the root-node of the book's contents.

    If you want to use chapters (and subchapters) in navigation you have to organize the images in folders, coz a chapter points to a folder.
    You can add images directly to the root as well for example the introduction, table of contents, spacer-images between the chapters, ...

    """
    _cover_front = None
    _cover_front_format = None
    _cover_rear = None
    _cover_rear_format = None

    def __init__(self, book_obj):
        self._init(book_obj, None)
        self._contents = []

    
    def set_cover_front(self, src: str|BytesIO) -> None:
        """set_cover_front 

        :param src: the front-cover of the book
        :type src: str | BytesIO
        """        
        if src == None or src == '':
            self._cover_front = None
            self._cover_front_format = None
            return
        (ignore, cover_front_format) = self._check_image(src, 'src', False)
        self._cover_front = src
        self._cover_front_format = cover_front_format


    def set_cover_rear(self, src: str|BytesIO) -> None:
        """set_cover_rear 

        :param src: the rear-cover of the book
        :type src: str | BytesIO
        """        
        if src == None or src == '':
            self._cover_rear = None
            self._cover_rear_format = None
            return
        (ignore, cover_rear_format) = self._check_image(src, 'src', False)
        self._cover_rear = src
        self._cover_rear_format = cover_rear_format
    

    def int_validate(self, warnings: bool|Callable) -> bool:
        found = False
        for content in self._contents:
            if content.int_validate(warnings):
                found = True

        if not found:
            ecmbUtils.raise_exception(f'the book doesn\'t contain an image!')
        return found
    

    def int_build(self, target_file: zipfile.ZipFile) -> etree.Element:
        if not self.int_validate(False):
            return
        
        self._build_id = 'content'
        main_node = etree.Element('content')

        if self._cover_front:
            main_node.set('cover_front', 'cover_front.' + self._cover_front_format)
            self._write_image(target_file, 'cover_front.' + self._cover_front_format, self._cover_front)

        if self._cover_rear:
            main_node.set('cover_rear', 'cover_rear.' + self._cover_rear_format)
            self._write_image(target_file, 'cover_rear.' + self._cover_rear_format, self._cover_rear)

        target_file.mkdir(self.int_get_build_path(False))

        for content in self._contents:
            content_node = content.int_build(target_file)
            if content_node != None:
                main_node.append(content_node)
        
        return main_node