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

from PyQt4.QtCore import QSize, SIGNAL, pyqtSignature
from PyQt4.QtGui import QDockWidget, QWidget, QVBoxLayout, QHBoxLayout, QIcon, QComboBox, QPushButton, QSortFilterProxyModel
from PyQt4.Qt import *

from api.gui.itemview.listview import ListView
from api.gui.itemview.listmodel import ListModel
from api.gui.itemview.thumbsitemmodel import ThumbsItemModel
from api.gui.itemview.thumbsview import ThumbsView
from api.gui.dialog.extractor import Extractor
from api.gui.box.nodecombobox import NodeComboBox

from ui.gui.utils.menu import MenuTags
from ui.gui.wrapper.connectorCallback import ConnectorCallback

import os

#Need some APIs functionnalities
from api.magic.filetype import *
from api.loader import *
from api.taskmanager.taskmanager import *
from api.env import *
        
class NodeList(QWidget):
    def __init__(self,  parent, mainWindow, dockBrowser):
        super(NodeList,  self).__init__(parent)
        
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

        self.initListView()
        self.initThumbsView()
        
        self.topButton = QPushButton(self)
        self.topButton.setFixedSize(QSize(32,32))
        self.topButton.setFlat(True)
        self.topButton.setIcon(QIcon(":previous.png"))
        self.topButton.setIconSize(QSize(32,32))
        self.hlayout.addWidget(self.topButton)

        self.listButton = QPushButton(self)
        self.listButton.setFixedSize(QSize(32, 32))
        self.listButton.setFlat(True)
        self.listButton.setIcon(QIcon(":list.png"))
        self.listButton.setIconSize(QSize(32,32))
        self.hlayout.addWidget(self.listButton)

        self.thumButton = QPushButton(self)
        self.thumButton.setFixedSize(QSize(32, 32))
        self.thumButton.setFlat(True)
        self.thumButton.setIcon(QIcon(":image.png"))
        self.thumButton.setIconSize(QSize(32,32))
        self.hlayout.addWidget(self.thumButton)

        self.thumSize = QComboBox()
        self.thumSize.setMaximumWidth(100)
        self.thumSize.addItem("Small")
        self.thumSize.addItem("Medium")
        self.thumSize.addItem("Large")
        self.connect(self.thumSize, SIGNAL("currentIndexChanged(QString)"), self.sizeChanged)
        self.hlayout.addWidget(self.thumSize)


        self.thumButton.setEnabled(True)
        self.thumSize.setEnabled(False)
        self.listButton.setEnabled(False)
        
        self.comboBoxPath = NodeComboBox(self)
        self.comboBoxPath.setMinimumSize(QSize(251,32))
        self.comboBoxPath.setMaximumSize(QSize(16777215,32))
        self.hlayout.addWidget(self.comboBoxPath)
        
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
        self.ThumbsItemModel = ThumbsItemModel(self.ThumbsView.thread)
        
        self.ThumbsView.setModels(self.ThumbsItemModel)
        self.ThumbsView.setSubMenu(self.submenuFile)
        self.vlayout.addWidget(self.ThumbsView)

    def initCallback(self, dockBrowser):
        self.connect(self.topButton, SIGNAL("clicked()"),  self.moveToTop)

        self.connect(self.listButton, SIGNAL("clicked()"),  self.listActivated)
        self.connect(self.thumButton, SIGNAL("clicked()"),  self.thumbActivated)

        self.connect(self.comboBoxPath, SIGNAL("currentIndexChanged(const QString & )"),  self.comboBoxPathChanged)
        self.connect(ConnectorCallback.instance, SIGNAL("reload"), self.reload,  Qt.BlockingQueuedConnection)        
        self.connect(dockBrowser.treeView, SIGNAL("changeDirectory"), self.loadFolder)
        self.connect(dockBrowser.treeView, SIGNAL("reloadNodeView"), self.reload)
        dockBrowser.treeView.connect(self, SIGNAL("setIndexAndExpand"), dockBrowser.treeView.setIndexAndExpand)
        dockBrowser.treeView.connect(self, SIGNAL("setIndex"), dockBrowser.treeView.setCurrentIndexForChild)
        
    def moveToTop(self):
        if self.currentIndexDir <> None :
            index = self.__browsers.treeItemModel.indexWithNode(self.currentNodeDir)
            parent = self.__browsers.treeItemModel.parent(index)
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
  
#    def comboBoxModeChanged(self, index):
#        if index == 0 :
#            self.ListView.setVisible(True)
#            self.ThumbsView.setVisible(False)
#        else :
#            self.ListView.setVisible(False)
#            self.ThumbsView.setVisible(True)
#        self.reloadChangedView()
        
    def listActivated(self):
        self.ListView.setVisible(True)
        self.ThumbsView.setVisible(False)
        self.reloadChangedView()

        #Desactivate thumb buttons
        self.thumButton.setEnabled(True)
        self.thumSize.setEnabled(False)
        self.listButton.setEnabled(False)

    def thumbActivated(self):
        self.ListView.setVisible(False)
        self.ThumbsView.setVisible(True)
        self.reloadChangedView()

        self.thumButton.setEnabled(False)
        self.thumSize.setEnabled(True)
        self.listButton.setEnabled(True)

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
            index = self.__browsers.treeItemModel.indexWithNode(self.currentNodeDir)
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

    def changeDirectoryBrowser(self, node):
        dockNodeTree = self.__mainWindow.dockNodeTree
        currentIndex = dockNodeTree.treeView.selectionModel().currentIndex()
        if currentIndex is None :
            return
        currentItem = dockNodeTree.treeItemModel.getItem(currentIndex)
        #if not node.next.empty():
        newcurrent = currentItem.childWithNode(node)
        if not newcurrent:
            return
        #            
        index = dockNodeTree.treeItemModel.index(newcurrent.childNumber(),  0,  currentIndex)
        self.emit(SIGNAL("setIndexAndExpand"), self, index)
        #    #self.loadFolder(node, index)

    ###############
    ## CONTEXT  MENU ##
    ###############
    def createSubMenu(self):
        self.extractor = Extractor(self.__mainWindow)
        self.connect(self.extractor, SIGNAL("filled"), self.launchExtract)
	self.submenuFile = QMenu()
        self.submenuFile.addAction(QIcon(":exec.png"),  "Open", self.openDefault, "Listview")
        self.menuModules = self.submenuFile.addMenu(QIcon(":exec.png"),  "Open With")
        self.menuTags = MenuTags(self, self.__mainWindow, self.getListCurrentNode)
        self.submenuFile.addSeparator()
        self.submenuFile.addAction(QIcon(":hexedit.png"), QApplication.translate("ListView", "Hexeditor", None, QApplication.UnicodeUTF8), self.launchHexedit, "Listview")
        self.submenuFile.addAction(QIcon(":extract.png"), QApplication.translate("ListView", "Extract", None, QApplication.UnicodeUTF8), self.extractNodes, "Listview")
        self.submenuFile.addSeparator()
        self.submenuFile.addAction(QIcon(":info.png"), QApplication.translate("ListView", "Property", None, QApplication.UnicodeUTF8), self.propertyNodes, "Listview")

    def launchExtract(self):
        res = self.extractor.getArgs()
        arg = self.env.libenv.argument("gui_input")
        lnodes = self.env.libenv.ListNode()
        lnodes.thisown = 0
        for node in res["nodes"]:
            lnodes.append(node)
        arg.thisown = 0
        arg.add_path("syspath", str(res["path"]))
        arg.add_lnode("files", lnodes)
        arg.add_bool("recursive", int(res["recurse"]))
        self.taskmanager.add("extract", arg, ["thread", "gui"])


    def extractNodes(self):
        self.extractor.launch(self.getListCurrentNode())

    def openDefault(self):
      nodes = self.getListCurrentNode()
      for node in nodes:
        arg = self.env.libenv.argument("gui_input")
        arg.thisown = 0 
        ft = FILETYPE()
        try:
          mod = ft.findcompattype(node)[0]
          if self.lmodules[mod]:
            conf = self.lmodules[mod].conf
            cdl = conf.descr_l
            for a in cdl:
              if a.type == "node":
                 arg.add_node(a.name, node)
          self.taskmanager.add(mod, arg, ["thread", "gui"])       
        except IndexError: 
          arg.add_node("file", node)
          self.taskmanager.add("hexedit", arg, ["thread", "gui"])        
 
    def launchHexedit(self):
        nodes = self.getListCurrentNode()
        for node in nodes:
            arg = self.env.libenv.argument("gui_input")
            arg.thisown = 0
            arg.add_node("file", node)
            self.taskmanager.add("hexedit", arg, ["thread", "gui"])

    def propertyNodes(self):
        if not self.__mainWindow.QPropertyDialog.isVisible():
            self.__mainWindow.QPropertyDialog.fillInfo(self.currentNodeDir, self.getListCurrentNode())
            iReturn = self.__mainWindow.QPropertyDialog.exec_()
            self.__mainWindow.QPropertyDialog.removeAttr()
        else:
            QMessageBox.critical(self, "Erreur", u"This box is already open")


# CALLBACK

    def sizeChanged(self, string):
        if string == "Small":
            self.ThumbsView.configure(64, 64)
        elif string == "Medium":
            self.ThumbsView.configure(96, 96)
        elif string == "Large":
            self.ThumbsView.configure(128, 128)

