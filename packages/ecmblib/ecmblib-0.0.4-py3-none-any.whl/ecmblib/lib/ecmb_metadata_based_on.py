#####################################################################
# File: ecmb_metadata_based_on.py
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

from lxml import etree
from .ecmb_utils import ecmbUtils
from .ecmb_enums import *
from .ecmb_metadata_original import ecmbMetaDataOriginal


class ecmbMetaDataBasedOn(ecmbMetaDataOriginal):
    """ecmbMetaDataBasedOn

    If the book based on eg. a light-novel and you want to give that credit, you can place the information here.

    :note: 
    * if you add any to this, the title is mandatory

    """
    def __init__(self):
       super().__init__()
       self._msg = f'if you provide a based-on-information the title is mandatory! Please use book.based_on.set_title("My Book Title")'
       self._node = 'basedon'
    
    def set_type(self, book_type: BASED_ON_TYPE) -> None:
        """set_type 

        :param book_type:
        :type book_type: BASED_ON_TYPE
        """        
        book_type = ecmbUtils.enum_value(book_type)

        if book_type != None and book_type != '':
            ecmbUtils.validate_enum(True, 'book_type', book_type, BASED_ON_TYPE)
        self._data['type'] = (book_type, {})

    