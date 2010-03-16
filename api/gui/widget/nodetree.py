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

from PyQt4.QtGui import QApplication, QDockWidget, QHBoxLayout, QWidget
from PyQt4.QtCore import QModelIndex, QReadWriteLock, QSize, Qt, SIGNAL

from api.taskmanager import *
from api.vfs.libvfs import *
from api.gui.itemview.treeitemmodel import TreeItemModel
from api.gui.itemview.treeview import TreeView

from ui.gui.vfs.docknodelist import DockNodeList
from ui.gui.wrapper.connectorCallback import ConnectorCallback

class NodeTree():
    class __NodeTree(QWidget):
        def __init__(self, mainWindow):
            QWidget.__init__(self, mainWindow)
            self.__mainWindow = mainWindow
            #self.__action = action
            self.sched = scheduler.sched
	    self.vfs = VFS.Get()            

            self.__listFiles = []
            self.childSelected = None
            self.childSelectedLock = QReadWriteLock()
        
            self.configure()
            self.g_display()
            self.initCallback()
        
        def configure(self):
            self.setObjectName("Browser")
            self.resize(300, 300)
            
        def g_display(self):
            self.layout = QHBoxLayout(self)
            
            # Browser 
            tmp = ["Virtual File System"]
            self.treeItemModel = TreeItemModel(tmp)
            self.treeView = TreeView(self, self.__mainWindow, self.treeItemModel)

            self.layout.addWidget(self.treeView)
            
            # Set Model and Resize
            self.treeView.setModel(self.treeItemModel)
            
            self.treeItemModel.addRootVFS()
            self.treeItemModel.fillAllDirectory(self.treeItemModel.rootItemVFS)
            self.treeItemModel.reset()
            self.treeView.resizeAllColumn()
            self.treeView.setCurrentIndex(self.treeItemModel.createIndex(self.treeItemModel.rootItemVFS.childNumber(), 0,  self.treeItemModel.rootItemVFS))
            
        def initCallback(self):
            self.connect(self, SIGNAL("refreshNodeView"), self.refreshNodeView) 
            self.sched.set_callback("refresh_tree", self.refreshNode)
	    self.vfs.set_callback("refresh_tree", self.refreshNode)       
 
        def refreshNode(self, node):
            index = self.treeView.currentIndex()
            isExpanded = self.treeView.isExpanded(index)
            item = self.treeItemModel.getItemWithPath(node.absolute())
            self.treeItemModel.fillAllDirectory(self.treeItemModel.rootItemVFS)
            self.treeItemModel.reset()
            self.emit(SIGNAL("refreshNodeView"), index, isExpanded)
            self.emit(SIGNAL("reloadNodeView"))
            
        def refreshNodeView(self, index, isExpanded):
            self.treeView.expandAllIndex(index)
            self.treeView.setCurrentIndex(index)
            self.treeView.setExpanded(index, isExpanded)
        
        def setChild(self, child):
            if self.childSelectedLock.tryLockForWrite() :
                self.childSelected = child
                self.childSelectedLock.unlock()
        
        def getChild(self):
            if self.childSelectedLock.tryLockForRead():
                tmp = self.childSelected
                self.childSelectedLock.unlock()
                return tmp
        
        def addList(self):
            dockList = DockNodeList(self.__mainWindow, self, len(self.__listFiles))
            self.__listFiles.append(dockList)
            self.__mainWindow.addNewDockWidgetTab(Qt.RightDockWidgetArea, dockList)
            dockList.initContents(self.treeView.getCurrentItem().node, self.treeView.currentIndex())
            return dockList
    
    instance = None
    
    def __init__(self,  mainWindow = None):
        if not NodeTree.instance :
            if mainWindow :
                NodeTree.instance = NodeTree.__NodeTree(mainWindow)
    
    def __getattr__(self, attr):
        return getattr(self.instance, attr)

    def __setattr__(self, attr, val):
        return setattr(self.instance, attr, val)
