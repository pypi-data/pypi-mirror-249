#####################################################################
# File: ecmb_navigation_base_sub.py
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

from __future__ import annotations
from typing import Callable
from .ecmb_enums import *
from .ecmb_utils import ecmbUtils
from .ecmb_navigation_base import ecmbNavigationBase
from .ecmb_navigation_link import ecmbNavigationLink
from .ecmb_content_folder import ecmbContentFolder
from .ecmb_content_image import ecmbContentImage


class ecmbNavigationBaseSub(ecmbNavigationBase):

    _children = None

    def _init(self, book_obj, label: str, title: str) -> None:
        super()._init(book_obj, label, title)
        self._children = []


    def add_headline(self, label_or_headline: str|ecmbNavigationHeadline, title: str = None) -> ecmbNavigationHeadline:
        """add_headline 
        
        Adds/creates a headline.

        :note:
        * you have to add at minimum one child to a headline
        * if you add a previously created ecmbContentImage all other parameters are ignored

        :param label_or_headline: a label or a previously created ecmbNavigationHeadline
        :type label_or_headline: str | ecmbNavigationHeadline
        :param title: the hover-text of the headline
        :type title: str, optional
        
        :rtype: ecmbNavigationHeadline
        """        
        headline_obj = None

        if type(label_or_headline) == ecmbNavigationHeadline:
            headline_obj = label_or_headline
        elif type(label_or_headline) == str:
            headline_obj = ecmbNavigationHeadline(self._book_obj, label_or_headline, title)
        else:
            ecmbUtils.raise_exception('please provide ecmbNavigationHeadline or a label!')
            
        headline_obj.int_set_parent(self)
        self._children.append(headline_obj)

        return headline_obj
    

    def add_chapter(self, label_or_chapter: str|ecmbNavigationChapter, folder: str|ecmbContentFolder, target: str|ecmbContentImage = None, target_side: TARGET_SIDE = TARGET_SIDE.AUTO, title: str = None) -> ecmbNavigationChapter:
        """add_chapter 

        Adds/creates a (sub-) chapter.

        You can define a target-image, which could be any image as long its part of the chapter's folder (default is the first image of the folder). If you are pointing to a double-page-image you can define if it should point to the left or right part (defaults to auto).

        :note:
        * if you add a previously created ecmbNavigationChapter all other parameters are ignored
        

        :param label_or_chapter: a label or a previously created ecmbNavigationChapter
        :type label_or_chapter: str | ecmbNavigationChapter
        :param folder: a folder-object or a unique-id pointing to a folder
        :type folder: str | ecmbContentFolder
        :param target: a image-object or a unique-id pointing to a image
        :type target: str | ecmbContentImage, optional
        :param target_side: the side of a double-page-image
        :type target_side: TARGET_SIDE, optional
        :param title: the hover-text of the chapter
        :type title: str, optional
        
        :rtype: ecmbNavigationChapter
        """  
        chapter_obj = None

        if type(label_or_chapter) == ecmbNavigationChapter:
            chapter_obj = label_or_chapter
        elif type(label_or_chapter) == str:
            chapter_obj = ecmbNavigationChapter(self._book_obj, label_or_chapter, folder, target, target_side, title)
        else:
            ecmbUtils.raise_exception('please provide ecmbNavigationChapter or a label!')
            
        chapter_obj.int_set_parent(self)
        self._children.append(chapter_obj)

        return chapter_obj


    def add_link(self, label_or_link: str|ecmbNavigationLink, target: str|ecmbContentImage, target_side: TARGET_SIDE = TARGET_SIDE.AUTO, title: str = None) -> ecmbNavigationLink:
        """add_link

        Adds/creates a link to an image.

        The target-image has to be part of this chapter's folder. If you are pointing to a double-page-image you can define if it should point to the left or right part (defaults to auto).

        :note:
        * if you add a previously created ecmbNavigationLink all other parameters are ignored


        :param label_or_link: a label or a previously created ecmbNavigationLink
        :type label_or_link: str | ecmbNavigationLink
        :param target: a image-object or a unique-id pointing to a image
        :type target: str | ecmbContentImage
        :param target_side: the side of a double-page-image
        :type target_side: TARGET_SIDE, optional
        :param title: the hover-text of the link
        :type title: str, optional

        :rtype: ecmbNavigationLink
        """        
        link_obj = None

        if type(label_or_link) == ecmbNavigationLink:
            link_obj = label_or_link
        elif type(label_or_link) == str:
            link_obj = ecmbNavigationLink(self._book_obj, label_or_link, target, target_side, title)
        else:
            ecmbUtils.raise_exception('please provide ecmbNavigationLink or a label!')
            
        link_obj.int_set_parent(self)
        self._children.append(link_obj)

        return link_obj
    

    def int_validate(self, warnings: bool|Callable) -> bool:
        found = False
        for child in self._children:
            if child.int_validate(warnings):
                found = True
        return found
    

# for type-hinting and and type-check in combination with "from __future__ import annotations"
# can't include them on top coz these ar subclasses of ecmbNavigationBaseSub
from .ecmb_navigation_chapter import ecmbNavigationChapter
from .ecmb_navigation_headline import ecmbNavigationHeadline