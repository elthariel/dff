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

# Form Custom implementation for browsing in your vfs
from PyQt4.QtCore import Qt, QSize, SIGNAL
from PyQt4.QtGui import QApplication, QDialog, QIcon, QListView,  QStandardItemModel

# CORE
from api.vfs import *
from api.gui.itemview.nodeitem import NodeItem

# MODEL ListView
class SelectNodesModel( QStandardItemModel):
    def __init__(self):
        super(SelectNodesModel,  self).__init__(0,  1)
        self.currentNode = 0
        self.currentSelection = 0
    
    def newPath(self, node, listNode):
        self.currentNode = node
        self.clear()
            
        for node in listNode:
            item = []
            item.append(NodeItem(node))
            item[0].setEditable(False)
            item[0].setText(QApplication.translate("MainWindow", str(node.name), None, QApplication.UnicodeUTF8))
            if not node.next.empty():
                item[0].setIcon(QIcon(":dff_folder.png"))
            else :
                item[0].setIcon(QIcon(":file.png"))
            self.appendRow(item)
        self.sort(0,  Qt.AscendingOrder)
        
    def clear(self):
        if self.rowCount() > 0:
            self.removeRows(0, self.rowCount())


