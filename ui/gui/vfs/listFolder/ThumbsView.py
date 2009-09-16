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

from PyQt4.QtCore import QSize, Qt
from PyQt4.QtGui import QAbstractItemView, QApplication, QCursor, QFileDialog, QHBoxLayout, QIcon, QLabel, QListView, QMenu, QPixmap, QWidget

from api.vfs import *

from ThumbsThread import ThumbsThread

class ThumbsView(QListView):
    def __init__(self,  mainWindow, parent):
        super(ThumbsView,  self).__init__(parent)
        self.__mainWindow = mainWindow
        self.__parent = parent
        self.vfs = vfs.vfs()
        self.setVisible(False)
        self.configure()
        self.thread = ThumbsThread()
        
        
    def configure(self):
        self.setIconSize(QSize(80, 80))        
        self.setSpacing(2)
        #self.setFlow(QtGui.QListView.TopToBottom)
        self.setLayoutMode(QListView.Batched)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setViewMode(QListView.IconMode)
        self.setLineWidth(80)
        self.setUniformItemSizes(True)
        self.setMidLineWidth(80)
        self.setMovement(QListView.Static)
    
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
    
        for i in range(0, len(currentListIndexs)):
            if currentListIndexs[i].column() == 0:
                currentListItem.append(self.__model.item(currentListIndexs[i].row(), currentListIndexs[i].column()))
        return currentListItem
        
    def getListCurrentNode(self):
        currentListIndexs = self.selectionModel().selectedIndexes()
        currentListNode = []
    
        for i in range(0, len(currentListIndexs)):
            if currentListIndexs[i].column() == 0:
                currentListNode.append(self.__model.item(currentListIndexs[i].row(), currentListIndexs[i].column()).nodeVFS)
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

    def loadFolder(self,  nodeVFS,  force):
        if str(self.__model.currentNodeDir) <> str(nodeVFS) or force == 1 :
            list = self.vfs.listingDirectoriesAndFiles(nodeVFS)
            if list != False :
                #print "START" + str(len(list))
                if not self.thread.isFinished() :
                    self.thread.myStop()
                    self.thread.wait()
                self.__model.removeAll()
                self.thread.initArg(self.__model,  list)
                self.__model.currentNodeDir = nodeVFS
                self.thread.start() 

    def loadModule(self, node):
        self.taskmanager = TaskManager()
        modules = self.currentModuleName()
        self.taskmanager.add(str(modules), self.arg, ["thread", "gui"])
        

    def mouseDoubleClickEvent(self, e):
        indexClicked = self.indexAt(e.pos())
        if  not indexClicked:
            return
        self.__parent.setChildSelected()
        
        if not indexClicked.isValid():
            self.setCurrentIndex(indexClicked)
            return
        item = self.__model.item(indexClicked.row(),indexClicked.column())
        
        if not item.nodeVFS.next.empty():
            self.__parent.changeDirectoryBrowser(item.nodeVFS)
            return
        else:
            self.__parent.openFileWith(item.nodeVFS)
            return
            #return self.arg
#        size = item.nodeVFS.attr.size
#        f = item.nodeVFS.open()
#        buff = f.read(size)
#        f.close()
#        img = QPixmap()
#        if img.loadFromData(buff):
#            widget = QWidget()
#            layout = QHBoxLayout(widget)
#            widget.setLayout(layout)
#            
#            label = QLabel()
#            index = self.__mainWindow.tabBarCentral.addTab(widget, str(item.nodeVFS.name))
#            label.setMaximumSize(widget.width(),  widget.height())
#            
#            if widget.height() < img.height() :
#                img = img.scaledToHeight(widget.height())
#            if widget.width() < img.width() :
#                img = img.scaledToWidth(widget.width())
#            label.setPixmap(img)
#            layout.addWidget(label)
#            
#            self.__mainWindow.tabBarCentral.setCurrentIndex(index)
