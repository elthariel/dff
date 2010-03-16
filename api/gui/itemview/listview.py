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

from PyQt4.QtGui import QTableView, QAbstractItemView, QFont, QCursor, QMenu, QIcon, QApplication, QFileDialog, QMessageBox
from PyQt4.Qt import *
from PyQt4.QtCore import SIGNAL

from api.vfs import *
from api.gui.itemview.listthread import ListThread

class ListView(QTableView):
    # TAKE :        None
    def __init__(self,  parent, mainWindow):
        super(ListView,  self).__init__(parent)
        self.__mainWindow = mainWindow
        self.__parent = parent
        self.vfs = vfs.vfs()
        self.configure()
        self.initCallback()

    def configure(self):        
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSortingEnabled(True)
        self.horizontalHeader().setStretchLastSection(True)
        self.setShowGrid(0)
        self.resizeColumnsToContents()
        self.resizeRowsToContents()        
        self.verticalHeader().hide()
        font = QFont()
        font.setPointSize(8)
        self.setFont(font)
    
    def initCallback(self):
        self.connect(self.horizontalHeader(), SIGNAL("sortIndicatorChanged(int, Qt::SortOrder)"), self.sortIndicatorChanged)
    def sortIndicatorChanged(self, index,  sortIndicator):
        self.resizeColumnToContents(index)
        
    def setModels(self, model, filtermodel):
        self.__model = model
        self.__filtermodel = filtermodel
   	self.thread =  ListThread(self, self.__model)
	self.connect(self.thread, SIGNAL("resizeList"), self.resizeList)
	self.__model.initCallback(self)   
 
    def getModel(self):
        return self.__model
    
    def setSubMenu(self, submenu):
        self.submenuFile = submenu
        
    def loadFolder(self, node):
        list = self.vfs.listingDirectoriesAndFiles(node)
	self.__model.clear()
        self.thread.renderList(list, node)
	self.__model.currentNodeDir = node
    
    def reloadFolder(self):
        node = self.__model.currentNodeDir
        list = self.vfs.listingDirectoriesAndFiles(node)
        self.thread.renderList(list, node)

    def resizeList(self): 
	    self.__model.SortList()	
            self.resizeColumnsToContents()
            self.resizeRowsToContents()     
    
    def mouseDoubleClickEvent(self, e):
        indexClicked = self.indexAt(e.pos())
        if indexClicked.isValid():
            self.__parent.setChildSelected()
            indexModel = self.__filtermodel.mapToSource(indexClicked)
            item2 = self.__model.item(indexModel.row(),  0)
            if not item2.node.next.empty():
              self.__parent.changeDirectoryBrowser(item2.node)
            else:
	      self.__parent.openDefault()
            
    def mousePressEvent(self, e):
        indexClicked = self.indexAt(e.pos())
        if  not indexClicked:
            return
    
        if not indexClicked.isValid():
            self.setCurrentIndex(indexClicked)
            return
        
        if e.button() == Qt.LeftButton:
            self.setCurrentIndex(indexClicked)
            return
        
        if e.button() == Qt.RightButton:
            if not self.isSelected(indexClicked) :
                self.setCurrentIndex(indexClicked)
            self.submenuFile.popup(QCursor.pos())
            self.submenuFile.show()
        return
    
    def currentChanged(self,  currentIndex,  previousIndex):
        self.__parent.setChildSelected()
        if currentIndex == previousIndex :
            return 
        self.scrollTo(currentIndex)

    def isSelected(self,  currentIndex):
        list = self.selectionModel().selectedIndexes() 
        for index in list:  
            if index.column() == 0 and index == currentIndex :
                return True
        return False
        
    def getListCurrentItems(self):
        currentListIndexs = self.selectionModel().selectedIndexes()
        currentListItem = []
    
        for i in range(0, len(currentListIndexs)):
            if currentListIndexs[i].column() == 0:
                indexModel = self.__filtermodel.mapToSource(currentListIndexs[i])
                currentListItem.append(self.__model.item(indexModel.row(), indexModel.column()))
        return currentListItem
        
    def getListCurrentNode(self):
        currentListIndexs = self.selectionModel().selectedIndexes()
        currentListItem = []
        for i in range(0, len(currentListIndexs)):
            if currentListIndexs[i].column() == 0:
                indexModel = self.__filtermodel.mapToSource(currentListIndexs[i])
                currentListItem.append(self.__model.item(indexModel.row(), indexModel.column()).node)
        return currentListItem
