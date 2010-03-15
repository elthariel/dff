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

from types import *

from PyQt4.QtGui import QAbstractItemView, QApplication, QCheckBox, QDialog, QGridLayout, QLabel, QMessageBox,QSplitter, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
from PyQt4.QtCore import Qt,  QObject, QRect, QSize, SIGNAL

class ApplyModuleTable(QTableWidget):
    def __init__(self, parent):
        QTableWidget.__init__(self, parent)
        self.configure()
        self.addHeaders()
        
    def configure(self):
        self.setGeometry(QRect(9,40,403,358))
        #self.setMinimumSize(QSize(200, 358))
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setAutoScroll(True)
        self.setEditTriggers(QAbstractItemView.AnyKeyPressed|QAbstractItemView.DoubleClicked|QAbstractItemView.EditKeyPressed|QAbstractItemView.NoEditTriggers)
        self.setAlternatingRowColors(True)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setHorizontalScrollMode(QAbstractItemView.ScrollPerItem)
        self.setShowGrid(False)
        self.setGridStyle(Qt.NoPen)
        self.setSortingEnabled(True)
        self.setCornerButtonEnabled(False)
        self.verticalHeader().hide()
        self.setColumnCount(2)
        self.setRowCount(0)
        
    def addHeaders(self):
        headerItem = QTableWidgetItem()
        headerItem.setText(QApplication.translate("applyModule", "Name", None, QApplication.UnicodeUTF8))
        self.setHorizontalHeaderItem(0,headerItem)

        headerItem1 = QTableWidgetItem()
        headerItem1.setText(QApplication.translate("applyModule", "Tags", None, QApplication.UnicodeUTF8))
        self.setHorizontalHeaderItem(1,headerItem1)
    
    def resizeTableModules(self):
        self.setSortingEnabled(True)
        self.sortByColumn(0, Qt.AscendingOrder)
        self.resizeColumnToContents(1)
        if self.verticalScrollBar().isVisible() :
            newWidth = self.width() - self.columnWidth(1) - 8- self.verticalScrollBar().width()
        else :
            newWidth = self.width() - self.columnWidth(1) - 8 
        self.setColumnWidth(0, newWidth)
    
    def resizeEvent(self, e):
        self.resizeTableModules()
        self.scrollToItem(self.currentItem())
        #pos = self
        #self.repaint() #0, 0, e.size().width(), e.size().height())
        #qsize = self.vboxlayout.minimumSize()
        #self.resize(qsize.width(), qsize.height())
