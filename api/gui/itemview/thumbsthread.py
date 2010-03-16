# DFF -- An Open Source Digital Forensics Framework
# Copyright (C) 2009-2010 ArxSys
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

from PyQt4.QtGui import QImage, QImageReader
from PyQt4.QtCore import QThread, SIGNAL, QBuffer, QIODevice, QByteArray, QSize, Qt

from api.magic.filetype import *

class ThumbsThread(QThread):
    def __init__(self,  *args):
        QThread.__init__(self)
        self.stop = 0
        self.ft = FILETYPE()
        self.reg_viewer = re.compile("(JPEG|JPG|jpg|jpeg|GIF|gif|bmp|BMP|png|PNG|pbm|PBM|pgm|PGM|ppm|PPM|xpm|XPM|xbm|XBM).*", re.IGNORECASE)
 
    def initArg(self, viewerModel,  list, iconSize):
        self.model = viewerModel
        self.list = list
        self.stop = 0
        self.iconSize = iconSize       
 
    def myStop(self):
        self.stop = 1


    def getThumb(self, node):
        buff = ""
        if node.attr.size > 6:
            file = node.open()
            head = file.find("\xff\xd8\xff", 3, "", 3)
            if head > 0 and head < node.attr.size:
                foot = file.find("\xff\xd9", 2, "", int(head))
                if foot > 0 and foot < node.attr.size:
                    file.seek(head)
                    buff = file.read(foot + 2 - head)
            file.close()
        return buff


    def run(self):
        list_img = {}
        iter = 0
        for node in self.list:
            if self.stop == 1 :
                return
            if self.pixmapCache.find(node.path + "/" + node.name):
	       self.emit(SIGNAL("addIconFromCache"), node)
	       continue
            if node.attr.size != 0:
                map = node.attr.smap
                try:
                    #XXX temporary patch for windows magic
                    ftype = node.attr.smap["type"]
                except IndexError:
                    #XXX temporary patch for windows magic
                    self.ft.filetype(node)
                    ftype = node.attr.smap["type"]
                res = self.reg_viewer.match(ftype)
                if res != None:
                    type = ftype[:ftype.find(" ")]
                    buff = ""
                    tags = None
                    if type in ["JPEG", "JPG", "jpg", "JPEG"]:
                        try:
                            buff = self.getThumb(node)
                        except:
                            buff = ""
                    if len(buff) == 0:
                        f = node.open()
                        f.seek(0, 0)
                        buff = f.read()
                        f.close()
                    img = QImage()
                    if img.loadFromData(buff, type):
                        img = img.scaled(QSize(128, 128), Qt.KeepAspectRatio, Qt.FastTransformation)
                        self.emit(SIGNAL("addIconFromImage"), img, node)
			continue
	    self.emit(SIGNAL("addIcon"), node)   	
