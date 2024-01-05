#####################################################################
# File: ecmb_navigation_headline.py
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

from typing import Callable
from lxml import etree
from .ecmb_utils import ecmbUtils
from .ecmb_navigation_base_sub import ecmbNavigationBaseSub


class ecmbNavigationHeadline(ecmbNavigationBaseSub):
    """ecmbNavigationHeadline

    :note:
    * you have to add at minimum one child to a headline

    :param book_obj:
    :type book_obj: ecmbBook
    :param label: a label 
    :type label: str
    :param title: the hover-text of the headline
    :type title: str, optional
    """    

    def __init__(self, book_obj, label: str, title:str = None):
        
        super()._init(book_obj, label, title)


    def int_validate(self, warnings: bool|Callable) -> bool:
        if not super().int_validate(warnings):
            ecmbUtils.raise_exception('the headline "' + self._label + '" doesn\'t contain a navigation-object!')
            return False
        return True
    

    def int_build(self) -> etree.Element:
        if not self.int_validate(False):
            return
        
        main_node = etree.Element('headline')
        main_node.set('label', self._label)
        if self._title:
            main_node.set('title', self._title)

        for child in self._children:
            child_node = child.int_build()
            if child_node != None:
                main_node.append(child_node)
        
        return main_node