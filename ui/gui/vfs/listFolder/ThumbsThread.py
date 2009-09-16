# DFF -- An Open Source Digital Forensics Framework
# Copyright (C) 2009 ArxSys
# 
# This program is free software, distributed under the terms of
# the GNU General Public License Version 2. See the LICENSE file
# at the top of the source tree.
# 
# See http://www.digital-forensic.org for more information about this
# project. Please do not directly contact any of the maintainers of
# DFF for assistance; the project provides a web site, mailing lists
# and IRC channels for your use.
# 
# Author(s):
#  Frederic Baguelin <fba@digital-forensic.org>
# 

import re
import time

from PyQt4.QtGui import QImage
from PyQt4.QtCore import QThread, SIGNAL
#from ui.console.builtins.filetype import *
from api.magic.filetype import *

class ThumbsThread(QThread):
    def __init__(self,  *args):
        QThread.__init__(self)
        self.stop = 0
        
        self.reg_viewer = re.compile(".*(JPEG|jpg|jpeg|GIF|gif|bmp|png|pbm|pgm|ppm|xpm|xbm).*", re.IGNORECASE)
        self.reg_pdf = re.compile(".*(pdf).*", re.IGNORECASE)
        self.reg_doc = re.compile(".*(msword|docx|odt|txt).*", re.IGNORECASE)
        self.reg_spreadsheet = re.compile(".*(xlsx|xls).*", re.IGNORECASE)
        self.reg_ppt = re.compile(".*(ppt|pptx|pps).*", re.IGNORECASE)
        
    def initArg(self, ViewerModel,  list):
        self.ViewerModel = ViewerModel
        self.list = list
        self.stop = 0
        
    def myStop(self):
        self.stop = 1
        
    def run(self):
#        reg = re.compile("[a-zA-Z0-9]*(JPEG|jpg|jpeg|GIF|gif|bmp|png|pbm|pgm|ppm|xpm|xbm)\Z[a-zA-Z0-9]", re.IGNORECASE)
        list_img = {}
        iter = 0
        #for node in self.list:
        for node in self.list:
            if self.stop == 1 :
                return
            if node.next.empty():
                map = node.attr.smap
                try:
                    f = node.attr.smap["type-mime"]
                except :
                    ft = FILETYPE()
                    f = ft.filetype(node)
                if self.reg_viewer.match(f) :
                    list_img[iter] = node
                    self.emit(SIGNAL("addIconViewerImage"), node,  None)
                elif self.reg_pdf.match(f) :
                    self.emit(SIGNAL("addIconViewerImage"), node,  ":pdf.png")
                elif self.reg_doc.match(f) :
                    self.emit(SIGNAL("addIconViewerImage"), node,  ":document.png")
                elif self.reg_ppt.match(f) :
                    self.emit(SIGNAL("addIconViewerImage"), node,  ":presentation.png")
                elif self.reg_spreadsheet.match(f) :
                    self.emit(SIGNAL("addIconViewerImage"), node,  ":spreadsheet.png")
                else :
                    self.emit(SIGNAL("addIconViewerImage"), node,  None)
            else :
                self.emit(SIGNAL("addIconViewerImage"), node,  ":folder.png")
            time.sleep(0.05)
            iter = iter + 1

             
        for i in list_img:
            if self.stop == 1 :
                return

            node = list_img[i]
            size = node.attr.size
            f = node.open()
            buff = f.read(size)
            f.close()
            img = QImage()
            if img.loadFromData(buff):
                img = img.scaledToWidth(80)
                self.emit(SIGNAL("updateIconViewerImage"), img, i)
                time.sleep(0.1)
