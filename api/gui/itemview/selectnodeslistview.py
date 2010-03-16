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

from api.vfs import *

class SelectNodesListView(QListView):
    def __init__(self, parent):
        super(SelectNodesListView, self).__init__()
        self.__parent = parent
        
        self.initCallback()
        
    def initCallback(self):
        self.connect(self,  SIGNAL("doubleClicked(const QModelIndex &)"), self.selectDoubleClickItem)
        self.connect(self,  SIGNAL("clicked(const QModelIndex &)"), self.selectClickItem)
        
    def currentChanged(self, index, previous):
        if not index.isValid() :
            return
        item = self.model().item(index.row(),  index.column())
        node = item.node
        self.scrollTo(index)
        self.__parent.changeLineEdit(node)

    # This Function call when a doubleclicked event on item of ListView
    def selectDoubleClickItem(self, index):
        node = self.model().item(index.row(),  index.column()).node
        if not node.next.empty() :
            self.__parent.displayDirectory(node)
    
    # This Function call when a clicked event on item of ListView
    def selectClickItem(self,  index):
        node = self.model().item(index.row(),  index.column()).node
        self.model().currentSelection = node
