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

# Form Custom implementation for browsing in your vfs
from PyQt4.QtCore import Qt, QSize, SIGNAL
from PyQt4.QtGui import QApplication, QDialog, QIcon, QListView,  QStandardItemModel

# Import the template generate by QtDesigner Ui_selectNode
from _selectNode import Ui_selectNode 

# CORE
from api.vfs import *

# UTILS
from ui.gui.utils.standardItem import DFF_StandardItem
from ui.gui.utils.comboBox import DFF_ComboBoxNode

# MODEL ListView
class SelectNodesModel( QStandardItemModel):
    def __init__(self):
        super(SelectNodesModel,  self).__init__(0,  1)
        self.currentNode = 0
        self.currentSelection = 0
    
    def newPath(self, nodeVFS, listNode):
        self.currentNode = nodeVFS
        self.clear()
            
        for itemVFS in listNode:
            item = []
            item.append(DFF_StandardItem(itemVFS))
            item[0].setEditable(False)
            item[0].setText(QApplication.translate("MainWindow", str(itemVFS.name), None, QApplication.UnicodeUTF8))
            if not itemVFS.next.empty():
                item[0].setIcon(QIcon(":dff_folder.png"))
            else :
                item[0].setIcon(QIcon(":file.png"))
            self.appendRow(item)
        self.sort(0,  Qt.AscendingOrder)
        
    def clear(self):
        if self.rowCount() > 0:
            self.removeRows(0, self.rowCount())

class SelectNodesView(QListView):
    def __init__(self, parent):
        super(SelectNodesView, self).__init__()
        self.__parent = parent
        
        self.initCallback()
        
    def initCallback(self):
        self.connect(self,  SIGNAL("doubleClicked(const QModelIndex &)"), self.selectDoubleClickItem)
        self.connect(self,  SIGNAL("clicked(const QModelIndex &)"), self.selectClickItem)
        
    def currentChanged(self, index, previous):
        if not index.isValid() :
            return
        item = self.model().item(index.row(),  index.column())
        node = item.nodeVFS
        self.scrollTo(index)
        self.__parent.changeLineEdit(node)

    # This Function call when a doubleclicked event on item of ListView
    def selectDoubleClickItem(self, index):
        node = self.model().item(index.row(),  index.column()).nodeVFS
        if not node.next.empty() :
            self.__parent.displayDirectory(node)
    
    # This Function call when a clicked event on item of ListView
    def selectClickItem(self,  index):
        node = self.model().item(index.row(),  index.column()).nodeVFS
        self.model().currentSelection = node
        
# QDialog for select Node
class DFF_SelectNodes(QDialog,  Ui_selectNode):
    def __init__(self,  parent):
        QDialog.__init__(self,  parent)
        Ui_selectNode.__init__(self)
        self.setupUi(self)
        self.vfs = vfs.vfs()
        self.g_display()
        self.initCallback()
        
    def g_display(self):
        self.comboBoxPath = DFF_ComboBoxNode(self)
        self.comboBoxPath.setMinimumSize(QSize(251, 23))
        self.comboBoxPath.setMaximumSize(QSize(16777215, 23))
        
        self.modelNodes = SelectNodesModel()
        self.listViewer = SelectNodesView(self)
        self.listViewer.setModel(self.modelNodes)
        
        self.hboxlayout.insertWidget(1, self.comboBoxPath)
        self.vboxlayout.insertWidget(1, self.listViewer)
        
        icon = QIcon(":top.png")
        self.topButton.setIcon(icon)
        
    def initCallback(self):
        self.connect(self.topButton, SIGNAL("clicked()"),  self.moveToTop)
        self.connect(self.comboBoxPath, SIGNAL("currentIndexChanged(const QString & )"),  self.comboBoxPathChanged)
    
    def moveToTop(self):
        self.displayDirectory(self.modelNodes.currentNode.parent)
    
    def comboBoxPathChanged(self, text):
        node = self.comboBoxPath.currentNode()
        self.displayDirectory(node)
    
    def displayDirectory(self, nodeVFS):
        listNode = self.vfs.listingDirectoriesAndFiles(nodeVFS)
        self.comboBoxPath.addPathAndSelect(nodeVFS)
        self.modelNodes.newPath(nodeVFS, listNode)
        
        self.currentSelectionEdit.clear()
    
    def returnSelection(self):
        index = self.listViewer.currentIndex()
        item = self.modelNodes.itemFromIndex(index)
        if item is None :
            return None
        return item.nodeVFS
        
    def changeLineEdit(self, node):
        self.currentSelectionEdit.clear()
        self.currentSelectionEdit.insert(node.name)
