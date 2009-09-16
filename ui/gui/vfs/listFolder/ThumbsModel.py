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
#  Francois Percot <percot@gmail.com>
# 

from PyQt4.QtGui import QIcon, QPixmap, QStandardItemModel
from PyQt4.QtCore import SIGNAL

from ui.gui.utils.standardItem import DFF_StandardItem

class ThumbsModel(QStandardItemModel):
    def __init__(self, thread):
        super(ThumbsModel,  self).__init__()
        self.__thread = thread
        self.currentNodeDir = None
        self.initSignals()
        
    def initSignals(self):
        self.connect(self.__thread, 
                     SIGNAL("updateIconViewerImage"),
                     self.updateIconViewerImage)
        self.connect(self.__thread, 
                     SIGNAL("addIconViewerImage"),
                     self.addIconViewerImage)
    
    def removeAll(self):
        if self.rowCount() > 0:
            for i in range(0,  self.rowCount()) :
                item = self.item(i)
                del item
            self.removeRows(0, self.rowCount())
        self.reset()
    
    def addIconViewerImage(self,  node, icons):
        items = []
        if icons == None :
            icon = QIcon(":empty.png")
        else :
            icon = QIcon(icons)
        item = DFF_StandardItem(node)
        item.setIcon(icon)
        item.setText(str(node.name))
        item.setEditable(True)

        items.append(item)
        self.appendRow(items)

    def testing(self):
	pass

    def updateIconViewerImage(self,  data,  pos):
        pixmap = QPixmap()
        pixmap = pixmap.fromImage(data)
        item = self.item(pos)
        if item :
           icon = QIcon(pixmap)
           item.setIcon(icon)
           #self.connect(icon, SIGNAL("clicked()"), self.testing)
        del data
