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


# CORE
from api.loader import *
from api.env import *
from api.vfs import *
from api.taskmanager.taskmanager import *
from api.type import *
from api.gui.box.nodecombobox import NodeComboBox
from api.gui.box.stringcombobox import StringComboBox
from api.gui.box.boolcombobox import BoolComboBox
from api.gui.box.checkbox import CheckBoxWidgetEnable
from api.gui.button.pushbutton import PushButton
from api.gui.dialog.uiapplymodule import UiApplyModule 
from api.gui.widget.applymoduletable import ApplyModuleTable

from ui.gui.utils.utils import DFF_Utils



class ApplyModule(QDialog,  UiApplyModule):
    def __init__(self,  mainWindow):
        QDialog.__init__(self,  mainWindow)
        UiApplyModule.__init__(self)
        self.setupUi(self)
        
        self.__mainWindow = mainWindow
        self.loader = loader.loader()
        self.env = env.env()
        self.vfs = vfs.vfs()
        self.initDialog()
        self.initCallback()
        
    def initDialog(self):
        self.initArguments()
        
        self.vlayout = QVBoxLayout(self)
        self.vlayout.addWidget(self.label)
        self.tableModules = ApplyModuleTable(self)
        self.splitter = QSplitter(Qt.Vertical, self)
        self.splitter.addWidget(self.tableModules)
        self.splitter.addWidget(self.argumentsContainer)
        
        self.vlayout.addWidget(self.splitter)
        self.vlayout.addWidget(self.buttonBox)
    
    
    def initCallback(self):
        self.connect(self.tableModules, SIGNAL("currentItemChanged(QTableWidgetItem *, QTableWidgetItem *)"),  self.currentItemChanged)
        self.connect(self.buttonBox,SIGNAL("accepted()"), self.validateModule)
        #self.connect(self.tableModules, SIGNAL("itemChanged(QTableWidgetItem *)"),  self.itemChanged)

    def currentItemChanged(self,  itemCurrent,  itemPrevious):
        if itemCurrent :
            if (itemPrevious and itemCurrent.row() <> itemPrevious.row()) or not itemPrevious:
                if itemCurrent.column() == 1 :
                    itemType = itemCurrent
                    itemCurrent = self.tableModules.item(itemCurrent.row(), 0)
                else :
                    itemType = self.tableModules.item(itemCurrent.row(), 1)
                self.reloadAllArguments(str(itemCurrent.text()),  str(itemType.text()))
            self.tableModules.resizeTableModules()
            self.tableModules.scrollToItem(itemCurrent)

    def validateModule(self):
        errorArg = []
        for i in self.valueArgs :
            if not i.optional :
                if i.type == "node" :
                    node = self.valueArgs[i].currentNode()
                    if node is None :
                        errorArg.append(i)
                else :
                    value = str(self.valueArgs[i].currentText())
                    if value == "" :
                        errorArg.append(i)
        if len(errorArg) > 0 :
            QMessageBox.warning(self, QApplication.translate("ApplyModule", "Missing Arguments", None, QApplication.UnicodeUTF8), QApplication.translate("ApplyModule", "There are missing arguments.", None, QApplication.UnicodeUTF8))
        else :
            self.accept()
    
    def initAllInformations(self, nameModule, typeModule, nodesSelected):
        self.__nodesSelected = nodesSelected
        self.deleteAllArguments()
        self.deleteList()
        self.fillListModules()
        if nameModule <> None :
            self.loadOneItem(nameModule, typeModule)
        else :
            self.deleteAllArguments()
        self.tableModules.setColumnWidth(0, 333)
        self.tableModules.setColumnWidth(1, 43)
        
    
    ###### MANAGE QTABLEWIDGET ######
    def deleteList(self):
        self.tableModules.clearContents()
        for i in range(0, self.tableModules.rowCount()) :
            self.tableModules.removeRow(0)
    
    def fillListModules(self):
        modules = self.loader.modules
        self.tableModules.setSortingEnabled(False)
        row = self.tableModules.rowCount() 
        self.tableModules.setRowCount(row + len(modules))
        
        for mod in modules :
            #if str(script) <> "opendump" and type(script) == StringType :
            item = QTableWidgetItem(str(mod))
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            item2 = QTableWidgetItem(modules[mod].tags)
            item2.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tableModules.setItem(row, 0, item)
            self.tableModules.setItem(row, 1, item2)
            row = row + 1
    
    def selectedItem(self, nameModule):
        for i in range(0, self.tableModules.rowCount()) :
            item = self.tableModules.item(i, 0)
            if (item.text() == nameModule) :
                self.tableModules.setCurrentItem(item)
                return
    
    def loadOneItem(self, nameModule, typeModule):
        self.tableModules.setRowCount(1)
        item = QTableWidgetItem(str(nameModule))
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        item2 = QTableWidgetItem(str(typeModule))
        item2.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tableModules.setItem(0, 0, item)
        self.tableModules.setItem(0, 1, item2)
        self.tableModules.setCurrentItem(item)
    
    ####### MANAGE ARGUMENTS
    def initArguments(self):
        self.argumentsContainer = QWidget(self)
        self.gridArgs = QGridLayout(self.argumentsContainer)
        self.labelArgs = {}
        self.valueArgs = {}
        self.checkBoxArgs = {}
        self.hboxArgs = {}
        self.browserButtons = {}
            
    def deleteAllArguments(self):
        if self.argumentsContainer <> None :
            listarg = self.argumentsContainer.children()
        for i in self.labelArgs :
            self.gridArgs.removeWidget(self.labelArgs[i])
            #self.labelArgs[i].hide()
            self.labelArgs[i].deleteLater()
            
            if self.valueArgs[i] <> None :
                self.gridArgs.removeWidget(self.valueArgs[i])
                #self.valueArgs[i].hide()
                self.valueArgs[i].deleteLater()
            
            if self.browserButtons[i] != None :
                self.gridArgs.removeWidget(self.browserButtons[i])
                #self.browserButtons[i].hide()
                self.browserButtons[i].deleteLater()
                
            if self.checkBoxArgs[i] != None :
                self.gridArgs.removeWidget(self.checkBoxArgs[i])
                #self.checkBoxArgs[i].hide()
                self.checkBoxArgs[i].deleteLater()
        
        self.valueArgs.clear()
        self.labelArgs.clear()
        self.browserButtons.clear()    
        self.checkBoxArgs.clear()
#        if self.argumentsContainer <> None :
#            listarg = self.argumentsContainer.children()
#            self.argumentsContainer.destroy(True, True)
#            self.argumentsContainer = None   
    
    def reloadAllArguments(self, nameModule, type):
        self.deleteAllArguments()
        if self.argumentsContainer == None :
            self.argumentsContainer = QWidget(self)

        iterator = 0
        args = DFF_Utils.getArgs(nameModule)
        vars_db = self.env.vars_db
        for arg in args:
            label = QLabel(arg.name + " ( "+ str(arg.type) + " ) " + ":", self.argumentsContainer)
            label.setMinimumSize(QSize(80,  28))
            label.setMaximumSize(QSize(120,  28))
            list = self.env.getValuesInDb(arg.name,  arg.type)
            if arg.type == "node" :
                value = NodeComboBox(self.argumentsContainer)
                
                for i in range(0, len(list)) :
                    value.addPath(list[i])
                button = PushButton(self.argumentsContainer, value, arg.name, self.__mainWindow.QSelectNodes , self.__mainWindow.dockNodeTree.treeItemModel.rootItemVFS.node)
                currentItem = self.__mainWindow.dockNodeTree.treeView.getCurrentItem()
                value.addPath(currentItem.node)
                
                if self.__nodesSelected  :
                    list = self.__nodesSelected
                    for i in range(0,  len(self.__nodesSelected)):
                        value.addPath(self.__nodesSelected[i])

            elif arg.type == "int":
                value = StringComboBox(self.argumentsContainer)
                value.setEditable(True)
                for i in range(0, len(list)) :
                    value.addPath(str(list[i]))
                button = None
            
            elif arg.type == "string":
                value = StringComboBox(self.argumentsContainer)
                value.setEditable(True)
                for i in range(0, len(list)) :
                    value.addPath(list[i])
                button = None
                    
            elif arg.type == "path" :
                value = StringComboBox(self.argumentsContainer)
                value.setEditable(True)
                for i in range(0, len(list)) :
                    value.addPath(list[i])
                button = PushButton(self.argumentsContainer,  value, arg.name)
            
            elif arg.type == "bool" :
                value = BoolComboBox(self.argumentsContainer)
                button = None
                    
            if arg.optional :
                checkBox =  CheckBoxWidgetEnable(self.argumentsContainer, label, value,  button)
            else :
                checkBox = None
            
            self.gridArgs.addWidget(label, iterator, 0)
            if value != None :
                self.gridArgs.addWidget(value, iterator, 1)
            if button != None:
                self.gridArgs.addWidget(button, iterator, 2)
            if checkBox != None :
                self.gridArgs.addWidget(checkBox, iterator, 3)

            value.setCurrentIndex(value.count() - 1)
            self.labelArgs[arg] = label
            self.valueArgs[arg] = value
            self.checkBoxArgs[arg] = checkBox
            self.browserButtons[arg] = button
            iterator = iterator + 1

    def currentType(self):
        item = self.tableModules.currentItem()
        if item.column() == 0 :
            item = self.tableModules.item(item.row() , 1)
        return str(item.text())
        
    def currentModuleName(self):
        item = self.tableModules.currentItem()
        if item.column() == 1 :
            item = self.tableModules.item(item.row(), 0)
        return str(item.text())

    # get Arguments
    def getDFFArguments(self):
        self.arg = self.env.libenv.argument("gui_input")
        self.arg.thisown = 0
        for i in self.valueArgs :
            if i.type == "node" :
                self.arg.add_node(str(i.name), self.valueArgs[i].currentNode())
        #        print DFF_Utils.getPath(self.valueArgs[i].currentNode())
            else :
                value = str(self.valueArgs[i].currentText())
                if i.type == "path" :
                    tmp = libtype.Path(str(value))
                    tmp.thisown = 0
                    self.arg.add_path(str(i.name), tmp)
                elif i.type == "int" :
                    self.arg.add_int(str(i.name), int(value))
                elif i.type == "string" :
                    self.arg.add_string(str(i.name), value)            
                elif i.type == "bool" :
                    if value == "True" :
                        value = 1
                    else :
                        value = 0
                    self.arg.add_bool(str(i.name), int(value))
        self.taskmanager = TaskManager()
        modules = self.currentModuleName()
        self.taskmanager.add(str(modules), self.arg, ["thread", "gui"])
        return self.arg
