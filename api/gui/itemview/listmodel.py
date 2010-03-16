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

import sys

from PyQt4.QtCore import QVariant
from PyQt4.QtGui import QApplication, QIcon, QStandardItemModel, QStandardItem
from PyQt4.Qt import *

class ListModel(QStandardItemModel):
    def __init__(self, parent):
        super(ListModel,  self).__init__(0,  6, parent)
        self.setHeaderData(0, Qt.Horizontal, QVariant(QApplication.translate("ListModel", "Name", None, QApplication.UnicodeUTF8)))
        self.setHeaderData(1, Qt.Horizontal, QVariant(QApplication.translate("ListModel", "Size", None, QApplication.UnicodeUTF8)))
        self.setHeaderData(2, Qt.Horizontal, QVariant(QApplication.translate("ListModel", "Accessed Time", None, QApplication.UnicodeUTF8)))
        self.setHeaderData(3, Qt.Horizontal, QVariant(QApplication.translate("ListModel", "Changed Time", None, QApplication.UnicodeUTF8)))
        self.setHeaderData(4, Qt.Horizontal, QVariant(QApplication.translate("ListModel", "Modified Time", None, QApplication.UnicodeUTF8)))
        self.setHeaderData(5, Qt.Horizontal, QVariant("Module"))
        self.timeHeader = {
                "accessed": 2, 
                "changed": 3, 
                "modified": 4, 
                           }
        self.currentNodeDir = None

    def initCallback(self, listView):               
        self.__thread = listView.thread 
	self.connect(self.__thread, SIGNAL("addItem"), self.addItem)

    def addItem(self, item, icon):
	item[0].setIcon(QIcon(icon))
	self.appendRow(item)
#	self.sort(0, Qt.DescendingOrder)
   # def PopulateList(self):
    #   self.sort(0,  Qt.DescendingOrder)
    def SortList(self):
	self.sort(0)
    
    def clear(self):
        if self.rowCount() > 0:
            self.removeRows(0, self.rowCount())
