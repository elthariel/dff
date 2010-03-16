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

# Form Custom implementation for browsing in your vfs
from PyQt4.QtCore import Qt, QSize, SIGNAL
from PyQt4.QtGui import QApplication, QDialog, QIcon, QListView,  QStandardItemModel

from api.vfs import *
from api.gui.dialog.uiselectnodes import UiSelectNodes 
from api.gui.itemview.selectnodesmodel import SelectNodesModel
from api.gui.itemview.selectnodeslistview import SelectNodesListView
from api.gui.box.nodecombobox import NodeComboBox
from api.gui.box.stringcombobox import StringComboBox
from api.gui.box.boolcombobox import BoolComboBox

# QDialog for select Node
class SelectNodes(QDialog,  UiSelectNodes):
    def __init__(self,  parent):
        QDialog.__init__(self,  parent)
        UiSelectNodes.__init__(self)
        self.setupUi(self)
        self.vfs = vfs.vfs()
        self.g_display()
        self.initCallback()
        
    def g_display(self):
        self.comboBoxPath = NodeComboBox(self)
        self.comboBoxPath.setMinimumSize(QSize(251, 23))
        self.comboBoxPath.setMaximumSize(QSize(16777215, 23))
        
        self.modelNodes = SelectNodesModel()
        self.listViewer = SelectNodesListView(self)
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
    
    def displayDirectory(self, node):
        listNode = self.vfs.listingDirectoriesAndFiles(node)
        self.comboBoxPath.addPathAndSelect(node)
        self.modelNodes.newPath(node, listNode)
        
        self.currentSelectionEdit.clear()
    
    def returnSelection(self):
        index = self.listViewer.currentIndex()
        item = self.modelNodes.itemFromIndex(index)
        if item is None :
            return None
        return item.node
        
    def changeLineEdit(self, node):
        self.currentSelectionEdit.clear()
        self.currentSelectionEdit.insert(node.name)
