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

from PyQt4.QtGui import QApplication, QDockWidget, QHBoxLayout, QWidget
from PyQt4.QtCore import QModelIndex, QReadWriteLock, QSize, Qt, SIGNAL

from api.taskmanager import *
from api.vfs.libvfs import *

from DirModel import DirModel
from DirView import DirView

from ui.gui.vfs.listFolder.ListFiles import Dock_ListFiles
from ui.gui.wrapper.connectorCallback import ConnectorCallback
from ui.gui.utils.utils import DFF_Utils

class DFF_Browsers():
    class __DFF_Browsers(QWidget):
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
            self.DirModel = DirModel(tmp)
            self.DirView = DirView(self, self.__mainWindow, self.DirModel)

            self.layout.addWidget(self.DirView)
            
            # Set Model and Resize
            self.DirView.setModel(self.DirModel)
            
            self.DirModel.addRootVFS()
            self.DirModel.fillAllDirectory(self.DirModel.rootItemVFS)
            self.DirModel.reset()
            self.DirView.resizeAllColumn()
            self.DirView.setCurrentIndex(self.DirModel.createIndex(self.DirModel.rootItemVFS.childNumber(), 0,  self.DirModel.rootItemVFS))
            
        def initCallback(self):
            self.connect(self, SIGNAL("refreshNodeView"), self.refreshNodeView) 
            self.sched.set_callback("refresh_tree", self.refreshNode)
	    self.vfs.set_callback("refresh_tree", self.refreshNode)       
 
        def refreshNode(self, node):
            index = self.DirView.currentIndex()
            isExpanded = self.DirView.isExpanded(index)
            item = self.DirModel.getItemWithPath(DFF_Utils.getPath(node))
            self.DirModel.fillAllDirectory(self.DirModel.rootItemVFS)
            self.DirModel.reset()
            self.emit(SIGNAL("refreshNodeView"), index, isExpanded)
            self.emit(SIGNAL("reloadNodeView"))
            
        def refreshNodeView(self, index, isExpanded):
            self.DirView.expandAllIndex(index)
            self.DirView.setCurrentIndex(index)
            self.DirView.setExpanded(index, isExpanded)
        
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
            dockList = Dock_ListFiles(self.__mainWindow, self, len(self.__listFiles))
            self.__listFiles.append(dockList)
            self.__mainWindow.addNewDockWidgetTab(Qt.RightDockWidgetArea, dockList)
            dockList.initContents(self.DirView.getCurrentItem().nodeVFS, self.DirView.currentIndex())
            return dockList
    
    instance = None
    
    def __init__(self,  mainWindow = None):
        if not DFF_Browsers.instance :
            if mainWindow :
                DFF_Browsers.instance = DFF_Browsers.__DFF_Browsers(mainWindow)
            else :
                #print "Class DFF_Browsers don't create. Need mainWindow and action for first instanciation. Thanks"
		pass
    
    def __getattr__(self, attr):
        return getattr(self.instance, attr)

    def __setattr__(self, attr, val):
        return setattr(self.instance, attr, val)
