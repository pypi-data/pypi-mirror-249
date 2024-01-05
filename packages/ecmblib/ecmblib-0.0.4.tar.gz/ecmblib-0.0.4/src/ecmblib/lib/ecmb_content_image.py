#####################################################################
# File: ecmb_content_image.py
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
from io import BytesIO
from lxml import etree
from typing import Callable
from .ecmb_enums import *
from .ecmb_utils import ecmbUtils
from .ecmb_content_base import ecmbContentBase

class ecmbContentImage(ecmbContentBase):
    """ecmbContentImage 
    
    :note:
    * if you add a double-page-image you have to add the splitted left and right part as well to give the reader-app more opportunities. The class automatic detects if a double-page-image is added and will raise an ecmbException if you didn't provide the left and right part
    * provide a unique-id if you want to access this image easily later at navigation

    :param book_obj:
    :type book_obj: ecmbBook
    :param src: an image (single-page or double-page)
    :type src: str | BytesIO
    :param src_left: the left part of the double-page-image
    :type src_left: str | BytesIO, optional
    :param src_right: the right part of the double-page-image
    :type src_right: str | BytesIO, optional
    :param unique_id: provide a unique-id if you want to access this image easily later at navigation
    :type unique_id: str, optional
    """    

    _src = None
    _src_format = None
    _src_left = None
    _src_left_format = None
    _src_right = None
    _src_right_format = None
    
    def __init__(self, book_obj, src: str|BytesIO, src_left: str|BytesIO = None, src_right: str|BytesIO = None, unique_id: str = None):
        self._init(book_obj, unique_id)

        msg = 'for image: "' + src + '"' if type(src) == str else 'at unique_id: "' + self._unique_id + '"'

        (is_double, src_format) = self._check_image(src, 'src', True)
        if is_double:
            if not src_left or not src_right:
                ecmbUtils.raise_exception(f'double-page-image detected, but src_left or/and src_right missing {msg}!')
            
            (ignore, src_left_format) = self._check_image(src_left, 'src_left', False)
            (ignore, src_right_format) = self._check_image(src_right, 'src_right', False)
            
            self._src_left = src_left
            self._src_left_format = src_left_format
            self._src_right = src_right
            self._src_right_format = src_right_format
        elif src_left or src_right:
            ecmbUtils.raise_exception(f'single-page-image detected, but src_left or/and src_right are provided {msg}!')
            
        self._src = src
        self._src_format = src_format


    def int_validate(self, warnings: bool|Callable) -> bool:
        self._book_obj.int_get_next_page_nr()

        if self._src_left:
            page_nr = self._book_obj.int_get_next_page_nr()
            if page_nr % 2 != 0:
                msg = 'image: "' + self._src + '"' if type(self._src ) == str else 'image with the unique_id: "' + self._unique_id + '"'
                ecmbUtils.write_warning(warnings, f'{msg} is on an uneven page!')

        return True
    

    def int_build(self, target_file: zipfile.ZipFile) -> etree.Element:
        self._build_id = self._book_obj.int_get_next_build_id()
        file_path = self.int_get_build_path(False)

        if self._src_left:
            node = etree.Element('dimg')

            node.set('src', self._build_id + '.' + self._src_format)
            self._write_image(target_file, file_path + '.' + self._src_format, self._src)

            node.set('src_left', self._build_id + '_l.' + self._src_left_format)
            self._write_image(target_file, file_path + '_l.' + self._src_left_format, self._src_left)

            node.set('src_right', self._build_id + '_r.' + self._src_right_format)
            self._write_image(target_file, file_path + '_r.' + self._src_right_format, self._src_right)
        else:
            node = etree.Element('img')

            node.set('src', self._build_id + '.' + self._src_format)
            self._write_image(target_file, file_path + '.' + self._src_format, self._src)
        
        return node
    

    def int_get_image_path(self, target_side: TARGET_SIDE = TARGET_SIDE.AUTO) -> str:
        target_side = ecmbUtils.enum_value(target_side)

        link = self.int_get_build_path()
        link += '.' + self._src_format
        if self._src_left:
            link += '#' + (target_side if target_side else TARGET_SIDE.AUTO.value)

        return link