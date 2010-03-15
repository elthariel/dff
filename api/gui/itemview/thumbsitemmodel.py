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
#  Francois Percot <percot@gmail.com>
# 

from PyQt4.QtGui import QIcon, QPixmap, QStandardItemModel, QImage, QPixmapCache
from PyQt4.QtCore import SIGNAL

from api.gui.itemview.nodeitem import NodeItem

import time

class ThumbsItemModel(QStandardItemModel):
    def __init__(self, thread):
        super(ThumbsItemModel,  self).__init__()
        self.__thread = thread
        self.currentNodeDir = None
        self.initSignals()
        self.pixmapCache = QPixmapCache()     
        self.pixmapCache.setCacheLimit(61440) 
	self.__thread.pixmapCache = self.pixmapCache
 
    def initSignals(self):
        self.connect(self.__thread, 
                     SIGNAL("addIcon"),
                     self.addIcon)
        self.connect(self.__thread, 
                     SIGNAL("addIconFromCache"),
                     self.addIconFromCache)
        self.connect(self.__thread, 
                     SIGNAL("addIconFromImage"),
                     self.addIconFromImage)
   
    def removeAll(self):
        if self.rowCount() > 0:
            for i in range(0,  self.rowCount()) :
                item = self.item(i)
                del item
            self.removeRows(0, self.rowCount())
        self.reset()
    

    def addIcon(self, node):
        item = NodeItem(node)
        if node.next.empty():
          icon = QIcon(":folder_empty_128.png")
        else:
          if node.attr.size != 0: 
   	    icon = QIcon(":folder_documents_128.png") 
          else:
	    icon = QIcon(":folder_128.png")
        item.setIcon(icon)
        item.setText(str(node.name))
        item.setEditable(False)
        items = []
        items.append(item)
        self.appendRow(items)
   
    def addIconFromCache(self, node):
        item = NodeItem(node)
	pixmap = self.pixmapCache.find(node.path + "/" + node.name)
        icon = QIcon(pixmap)
        item.setIcon(icon)
        item.setText(str(node.name))
        item.setEditable(False)
        items = []
        items.append(item)
        self.appendRow(items)

    def addIconFromImage(self, img, node):
        item = NodeItem(node)
        pixmap = QPixmap()
        pixmap = pixmap.fromImage(img)
        self.pixmapCache.insert(node.path + "/" + node.name, pixmap) 
        icon = QIcon(pixmap)
        item.setIcon(icon)
        item.setText(str(node.name))
        item.setEditable(False)
        items = []
        items.append(item)
        self.appendRow(items)
