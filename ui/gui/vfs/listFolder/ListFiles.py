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

from PyQt4.QtCore import QSize, SIGNAL, pyqtSignature
from PyQt4.QtGui import QDockWidget, QWidget, QVBoxLayout, QHBoxLayout, QIcon, QComboBox, QPushButton, QSortFilterProxyModel
from PyQt4.Qt import *

from ListView import ListView
from ListModel import ListModel
from ThumbsModel import ThumbsModel
from ThumbsView import ThumbsView

from ui.gui.utils.utils import DFF_Utils
from ui.gui.utils.comboBox import DFF_ComboBoxNode
from ui.gui.utils.menu import MenuTags, MenuModules

from ui.gui.wrapper.connectorCallback import ConnectorCallback

#Need some APIs functionnalities
from api.magic.filetype import *
from api.loader import *
from api.taskmanager.taskmanager import *
from api.env import *

class Dock_ListFiles(QDockWidget):
    def __init__(self, mainWindow, dockBrowser, nbr):
        QDockWidget.__init__(self, mainWindow)
        self.configure()
        self.addAction(mainWindow,  nbr)
        self.g_display(mainWindow, dockBrowser)
        self.initCallback()
        self.setObjectName("LISTFILES " + str(nbr))

    def configure(self):
        self.setAllowedAreas(Qt.AllDockWidgetAreas)
        self.setWindowTitle(QApplication.translate("Files", "Files", None, QApplication.UnicodeUTF8))
    
    def addAction(self, mainWindow, nbr):
        self.__action = QAction(self)
        self.__action.setCheckable(True)
        self.__action.setChecked(True)
        self.__action.setObjectName("actionCoreInformations")
        self.__action.setText(QApplication.translate("MainWindow", "List Files", None, QApplication.UnicodeUTF8) + str(nbr))
        mainWindow.menuWindowMenuList.addAction(self.__action)
        self.connect(self.__action,  SIGNAL("triggered()"),  self.changeVisibleInformations)
    
    def changeVisibleInformations(self):
        if not self.isVisible() :
            self.setVisible(True)
            self.__action.setChecked(True)
        else :
            self.setVisible(False)
            self.__action.setChecked(False)
            
    def g_display(self, mainWindow, dockBrowser):
        self.widget = DFF_ListFiles(self, mainWindow, dockBrowser)
        self.setWidget(self.widget)
    
    def initCallback(self):
        self.connect(self, SIGNAL("visibilityChanged(bool)"), self.changedVisibility)
    
    def initContents(self, nodeVFS, index):
        self.widget.loadFolder(nodeVFS, index, 2)
    
    def changedVisibility(self, bool):
        if not self.isVisible() and not bool :
	     pass
        if bool :
            self.widget.setChildSelected()
        
        
class DFF_ListFiles(QWidget):
    def __init__(self,  parent, mainWindow, dockBrowser):
        super(DFF_ListFiles,  self).__init__(parent)
        
        self.__browsers = dockBrowser
        # Necessary
        self.type = "views"
        self.icon = QIcon(":list.png")
        self.name = ""
        self.__mainWindow = mainWindow
        self.__parent = parent
    
        # Specific
        self.currentIndexDir = None
        self.currentNodeDir = None
        
        self.g_display()
        self.initCallback(dockBrowser)

        self.loader = loader.loader()
        self.lmodules = self.loader.modules

        self.taskmanager = TaskManager()

        self.env = env.env()
        
    def g_display(self):
        self.setMinimumSize(QSize(400, 300))
        self.createSubMenu()
        self.vlayout = QVBoxLayout(self)
        self.hlayout = QHBoxLayout()
        self.vlayout.addLayout(self.hlayout)

        self.comboBoxPath = DFF_ComboBoxNode(self)
        self.comboBoxPath.setMinimumSize(QSize(251,23))
        self.comboBoxPath.setMaximumSize(QSize(16777215,23))
        self.hlayout.addWidget(self.comboBoxPath)
        
        self.initListView()
        self.initThumbsView()
        
        self.topButton = QPushButton(self)
        self.topButton.setFixedSize(QSize(23,23))
        self.topButton.setIcon(QIcon(":top.png"))
        self.hlayout.addWidget(self.topButton)
        
        self.comboBoxMode = QComboBox(self)
        self.comboBoxMode.setFixedSize(QSize(45,23))
        self.comboBoxMode.addItem(QIcon(":list.png"), "")
        self.comboBoxMode.addItem(QIcon(":viewer.png"), "")
        self.hlayout.addWidget(self.comboBoxMode)
        
    def initListView(self):    
        self.ListView = ListView(self, self.__mainWindow)
	self.ListModel = ListModel(self)
        self.ListModelFilter = QSortFilterProxyModel()
        self.ListModelFilter.setDynamicSortFilter(True)
        self.ListModelFilter.setSortCaseSensitivity(Qt.CaseInsensitive)
        self.ListModelFilter.setSourceModel(self.ListModel) 
        self.ListView.setModels(self.ListModel, self.ListModelFilter)
        self.ListView.setModel(self.ListModelFilter)
        self.ListView.setSubMenu(self.submenuFile)
        
        self.vlayout.addWidget(self.ListView)
        
    def initThumbsView(self):
        self.ThumbsView = ThumbsView(self.__mainWindow, self)
        self.ThumbsModel = ThumbsModel(self.ThumbsView.thread)
        
        self.ThumbsView.setModels(self.ThumbsModel)
        self.ThumbsView.setSubMenu(self.submenuFile)
        self.vlayout.addWidget(self.ThumbsView)
        
    def initCallback(self, dockBrowser):
        self.connect(self.topButton, SIGNAL("clicked()"),  self.moveToTop)
        self.connect(self.comboBoxPath, SIGNAL("currentIndexChanged(const QString & )"),  self.comboBoxPathChanged)
        self.connect(self.comboBoxMode, SIGNAL("currentIndexChanged(int )"),  self.comboBoxModeChanged)
        
        self.connect(ConnectorCallback.instance, SIGNAL("reload"), self.reload,  Qt.BlockingQueuedConnection)        
      #  self.connect(ConnectorCallback.instance, SIGNAL("reload"), self.reload)        
        self.connect(dockBrowser.DirView, SIGNAL("changeDirectory"), self.loadFolder)
        self.connect(dockBrowser.DirView, SIGNAL("reloadNodeView"), self.reload)
        
        dockBrowser.DirView.connect(self, SIGNAL("setIndexAndExpand"), dockBrowser.DirView.setIndexAndExpand)
        dockBrowser.DirView.connect(self, SIGNAL("setIndex"), dockBrowser.DirView.setCurrentIndexForChild)
        
    def moveToTop(self):
        if self.currentIndexDir <> None :
            index = self.__browsers.DirModel.indexWithNode(self.currentNodeDir)
            parent = self.__browsers.DirModel.parent(index)
            if parent:
                self.emit(SIGNAL("setIndexAndExpand"), self, parent)
                self.currentIndexDir = parent
            else :
                self.emit(SIGNAL("setIndexAndExpand"), self, index)
                self.currentIndexDir  = index
    
    def comboBoxPathChanged(self, text):
        node = self.comboBoxPath.getNode(str(text))    
        
        if node.this == self.currentNodeDir.this :
            return
        index = self.comboBoxPath.getBrowserIndex(str(text))
        self.loadFolder(node, index)
        self.emit(SIGNAL("setIndex"), self, self.currentIndexDir)
  
    def comboBoxModeChanged(self, index):
        if index == 0 :
            self.ListView.setVisible(True)
            self.ThumbsView.setVisible(False)
        else :
            self.ListView.setVisible(False)
            self.ThumbsView.setVisible(True)
        self.reloadChangedView()
        
    def reloadChangedView(self):
        if not self.visibleRegion().isEmpty() :
            view = self.viewVisible()
            if view.getModel().currentNodeDir is not None and view.getModel().currentNodeDir.this == self.currentNodeDir.this :
                return
            self.loadFolder(self.currentNodeDir, self.currentIndexDir, 1)
  
    # Specific type views
    def loadFolder(self,  node, indexFolder = None,  force = None):
        if node is None :
            return
        if self.currentNodeDir is not None :
            if force is None and self.currentNodeDir.this == node.this:
                return
        if force <> 2 and str(self) <> str(self.__browsers.getChild()) :
            return
            
        self.currentIndexDir = indexFolder
        self.currentNodeDir = node
        self.comboBoxPath.addPathAndSelect(node, indexFolder)
        
        if self.ThumbsView.isVisible() :
            self.ThumbsView.loadFolder(node, force)
        if self.ListView.isVisible() or force == 2:
            self.ListView.loadFolder(node)
        if force == 2 :
            self.emit(SIGNAL("setIndexAndExpand"), self, self.currentIndexDir)
    
    def setChildSelected(self):
        if str(self.__browsers.getChild()) <> str(self) :
            index = self.__browsers.DirModel.indexWithNode(self.currentNodeDir)
            self.emit(SIGNAL("setIndexAndExpand"), self, index)

    def getListCurrentItems(self):
        view = self.viewVisible()
        return view.getListCurrentItems()
    
    def getListCurrentNode(self):
        view = self.viewVisible()
        return view.getListCurrentNode()
    
    def reload(self):
        self.loadFolder(self.currentNodeDir, self.currentIndexDir, 1)
    
    def refreshIndexBrowser(self):
        self.emit(SIGNAL("setIndex"), self, self.currentIndexDir)
        
    def viewVisible(self):
        if self.ListView.isVisible() :
            return self.ListView
        if self.ThumbsView.isVisible() :
            return self.ThumbsView
        return self.ListView

    def changeDirectoryBrowser(self, nodeVFS):
        dockBrowser = self.__mainWindow.dockBrowser
        currentIndex = dockBrowser.DirView.selectionModel().currentIndex()
        if currentIndex is None :
            return
        currentItem = dockBrowser.DirModel.getItem(currentIndex)
        if not nodeVFS.next.empty():
            newcurrent = currentItem.childWithNode(nodeVFS)
            if not newcurrent:
                return
        #            
            index = dockBrowser.DirModel.index(newcurrent.childNumber(),  0,  currentIndex)
            self.emit(SIGNAL("setIndexAndExpand"), self, index)
        #    #self.loadFolder(nodeVFS, index)

    ###############
    ## CONTEXT  MENU ##
    ###############
    def createSubMenu(self):
	self.submenuFile = QMenu()
        self.menuModules = self.submenuFile.addMenu(QIcon(":applydriver.png"),  "Open With")
        self.menuTags = MenuTags(self, self.__mainWindow, self.getListCurrentNode)
        self.submenuFile.addSeparator()
        #self.submenuFile.addAction(QIcon(":extract.png"), QApplication.translate("ListView", "Extract", None, QApplication.UnicodeUTF8), self.extractNodes, "Listview")
        self.submenuFile.addSeparator()
        self.submenuFile.addAction(QIcon(":info.png"), QApplication.translate("ListView", "Property", None, QApplication.UnicodeUTF8), self.propertyNodes, "Listview")

    def extractNodes(self):
        if self.__mainWindow.DFF_CONFIG.extractFolder == "" :
            sDirName = QFileDialog.getExistingDirectory(self, QApplication.translate("MainWindow", "Choose Your Directory For Extraction", None, QApplication.UnicodeUTF8),  "/home",  QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
            if (sDirName) :
                self.__mainWindow.DFF_CONFIG.extractFolder = sDirName
            else :
                return
        DFF_Utils().execExtract(self.getListCurrentNode(), self.__mainWindow.DFF_CONFIG.extractFolder)
                
    def propertyNodes(self):
        if not self.__mainWindow.QPropertyDialog.isVisible():
            self.__mainWindow.QPropertyDialog.fillInfo(self.currentNodeDir, self.getListCurrentNode())
            iReturn = self.__mainWindow.QPropertyDialog.exec_()
            self.__mainWindow.QPropertyDialog.removeAttr()
        else:
            QMessageBox.critical(self, "Erreur", u"This box is already open")


    def openFileWith(self, nodeVFS):
        key = None
        mod = None
        module = None

        ft = FILETYPE()
        compat_module = ft.findcompattype(nodeVFS)
        for cmodule in compat_module:
            mod = self.lmodules[cmodule]
            if mod.tags == "viewer":
                module = cmodule
        
        if module != None:
            mod = self.lmodules[module]
            conf = mod.conf
            cdl = conf.descr_l
            for arg in cdl:
                if arg.type == "node":
                    key = arg.name
                    break

        if key != None and module != None:
            arg = self.env.libenv.argument("gui_input")
            arg.thisown = 0
            arg.add_node(key, nodeVFS)
            self.taskmanager.add(module, arg, ["thread", "gui"])
        else:
            if nodeVFS.attr.smap["type-mime"].find("pdf") != -1:
                pass
                #arg = self.env.libenv.argument("gui_input")
                #arg.thisown = 0
                #arg.add_node("file", nodeVFS)
                #arg.add_string("command", "/usr/bin/xpdf")
                #self.taskmanager.add("pipe_exec", arg, ["thread", "gui"])
