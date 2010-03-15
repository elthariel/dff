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

from PyQt4.QtCore import QSize, Qt
from PyQt4.QtGui import QAbstractItemView, QApplication, QCursor, QFileDialog, QHBoxLayout, QIcon, QLabel, QListView, QMenu, QPixmap, QWidget

from api.vfs import *

from thumbsthread import ThumbsThread

class ThumbsView(QListView):
    def __init__(self,  mainWindow, parent):
        super(ThumbsView,  self).__init__(parent)
        self.__mainWindow = mainWindow
        self.__parent = parent
        self.vfs = vfs.vfs()
        self.setVisible(False)
        self.configure(64, 64)
        self.thread = ThumbsThread()
 
    def configure(self, width, height):
        self.setIconSize(QSize(width,  height))       
        self.setGridSize(QSize(width + 10, height + 20)) 
        self.setFlow(QListView.LeftToRight)
	self.setLayoutMode(QListView.SinglePass)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setViewMode(QListView.IconMode)
        self.setUniformItemSizes(False)
        self.setMovement(QListView.Static)
        self.setSelectionRectVisible(True)
        self.setResizeMode(QListView.Adjust)

    def setModels(self, model):
        self.setModel(model)
        self.__model = model
        
    def getModel(self):
        return self.__model
    
    def setSubMenu(self, submenu):
        self.submenuFile = submenu
    
    def getListCurrentItems(self):
        currentListIndexs = self.selectionModel().selectedIndexes()
        currentListItem = []
    
        for i in xrange(0, len(currentListIndexs)):
            if currentListIndexs[i].column() == 0:
                currentListItem.append(self.__model.item(currentListIndexs[i].row(), currentListIndexs[i].column()))
        return currentListItem
        
    def getListCurrentNode(self):
        currentListIndexs = self.selectionModel().selectedIndexes()
        currentListNode = []
    
        for i in xrange(0, len(currentListIndexs)):
            if currentListIndexs[i].column() == 0:
                currentListNode.append(self.__model.item(currentListIndexs[i].row(), currentListIndexs[i].column()).node)
        return currentListNode
    
    def mousePressEvent(self, e):
        indexClicked = self.indexAt(e.pos())
        if  not indexClicked:
            return
        if not indexClicked.isValid():
            self.setCurrentIndex(indexClicked)
            return
        
        if e.button() == Qt.LeftButton :
            self.setCurrentIndex(indexClicked)
            
        if e.button() == Qt.RightButton:
            if not self.isSelected(indexClicked) :
                self.setCurrentIndex(indexClicked)
            self.submenuFile.popup(QCursor.pos())
            self.submenuFile.show()
            return
        return
    
    def isSelected(self,  currentIndex):
        list = self.selectionModel().selectedIndexes()
        for index in list:  
            if index == currentIndex :
                return True
        return False

    def loadFolder(self,  node,  force):
        if str(self.__model.currentNodeDir) <> str(node) or force == 1 :
            if not node.next.empty():
                if not self.thread.isFinished() :
                    self.thread.myStop()
                    self.thread.wait()
                self.__model.removeAll()
                self.thread.initArg(self.__model,  node.next, self.iconSize())
                self.__model.currentNodeDir = node
                self.thread.start() 

    def mouseDoubleClickEvent(self, e):
        indexClicked = self.indexAt(e.pos())
        if  not indexClicked:
            return
        self.__parent.setChildSelected()
        
        if not indexClicked.isValid():
            self.setCurrentIndex(indexClicked)
            return
        item = self.__model.item(indexClicked.row(),indexClicked.column())
        
        if not item.node.next.empty():
            self.__parent.changeDirectoryBrowser(item.node)
            return
        else:
	    self.__parent.openDefault()
            return
