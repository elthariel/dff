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

from PyQt4.QtGui import QApplication, QDialog, QFont, QHBoxLayout, QLabel, QSizePolicy, QLayout
from PyQt4.QtCore import QSize

# Import the template generate by QtDesigner Ui_PropertyDialog
from _propertyDialog import Ui_PropertyDialog 

# CORE
from api.vfs import *

# UTILS
from ui.gui.utils.utils import DFF_Utils

# QDialog about one file or one directory
class DFF_PropertyDialog(QDialog,  Ui_PropertyDialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        Ui_PropertyDialog.__init__(self)
        self.__mainWindow = parent
        self.setupUi(self)
        self.listAttrLayout = []
        self.listAttrName = []
        self.listAttrValue = []
        self.vfs = vfs.vfs()
        # Review
        #self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        

                
    def fillInfo(self, node, listNode = 0):
        # type = -1 : Undefine
        # type = 0 : Files and Directory
        # type = 1 : Only Directory
        # type = 2 : Only Files
        type = -1
        entryName = ""
        info = {}
        info['size'] = 0
        info['item'] = 0
        
        for i in  listNode :
            if not i.next.empty() :
                info_child = self.vfs.getInfoDirectory(i)
                info['size'] = info['size'] + info_child['size']
                info['item'] = info['item'] + info_child['item']
                if type == -1 or type == 1:
                    type = 1
                else :
                    type = 0
            else :
                info['size'] = info['size'] + i.attr.size
                info['item'] = info['item'] + 1
                if type == -1 or type == 2:
                    type = 2
                else :
                    type = 0
            entryName = entryName + i.name + ", "
        
        self.fillInfo2(entryName[:-2],  node, type,  info, len(listNode), listNode[0])
                
    def fillInfo2(self, names, node, types, info, nbrItem,  oneNode):
        self.vboxlayout.removeWidget(self.buttonClose)
        self.valueName.setText(names)
        
        if node.name == "" :
            self.valuePath.setText("/")
        else :
            self.valuePath.setText(node.path + "/" + node.name)
        
        if nbrItem == 1 :
            if oneNode.is_file :
                self.valueSize.setText(str(DFF_Utils.formatSize(info['size'])) + " ( "+str(info['size']) + " bytes ), dump size : "+ str(oneNode.attr.size))
            else :
                self.valueSize.setText(str(DFF_Utils.formatSize(info['size'])) + " ( "+str(info['size']) + " bytes ) ")
            if types == 1 :
                # One Directory
                self.valueType.setText(QApplication.translate("DFF_PropertyDialog", "Folder", None, QApplication.UnicodeUTF8))
            if types == 2 :
                # One Files
                self.valueType.setText(QApplication.translate("DFF_PropertyDialog", "File", None, QApplication.UnicodeUTF8))
            self.addAttr(oneNode)
        else :
            self.valueSize.setText(str(info['item']) +QApplication.translate("DFF_PropertyDialog", " items, totalling ", None,QApplication.UnicodeUTF8) + str(DFF_Utils.formatSize(info['size'])))
            if types == 1 :
                self.valueType.setText(QApplication.translate("DFF_PropertyDialog", "Folders", None,QApplication.UnicodeUTF8))
            if types == 2 :
                self.valueType.setText(QApplication.translate("DFF_PropertyDialog", "Files", None, QApplication.UnicodeUTF8))
            if types == 0 :
                self.valueType.setText(QApplication.translate("DFF_PropertyDialog", "---", None, QApplication.UnicodeUTF8))
        
        self.vboxlayout.addWidget(self.buttonClose)
        qsize = self.vboxlayout.minimumSize()
        self.resize(qsize.width(), qsize.height())
        self.vboxlayout.update()

            
    def addAttr(self, node):
        map = node.attr.smap 
        time = node.attr.time
        font = QFont()
        font.setWeight(75)
        font.setBold(True)
        
        for i in map :
            hboxlayout = QHBoxLayout()
            hboxlayout.setObjectName("labelType")
            labelType = QLabel(self.widget)
            labelType.setMinimumSize(QSize(92,22))
            labelType.setMaximumSize(QSize(92,22))
            labelType.setFont(font)
            labelType.setText(str(i) + " :")
            labelType.setObjectName("labelType")
            self.listAttrName.append(labelType)
            hboxlayout.addWidget(labelType)

            valueType =QLabel(self.widget)
            valueType.setMinimumSize(QSize(300,22))
            valueType.setMaximumSize(QSize(16777215,22))
            valueType.setObjectName("valueType")
            valueType.setText(str(map[i]))
            self.listAttrValue.append(valueType)
            hboxlayout.addWidget(valueType)
            
            self.listAttrLayout.append(hboxlayout)
            self.vboxlayout.addLayout(hboxlayout)
        
        for i in time :
            hboxlayout = QHBoxLayout()
            labelType = QLabel(self.widget)
            labelType.setMinimumSize(QSize(92,22))
            labelType.setMaximumSize(QSize(92,22))
            labelType.setFont(font)
            labelType.setText(str(i) + " :")
            labelType.setObjectName("labelType")
            self.listAttrName.append(labelType)
            hboxlayout.addWidget(labelType)

            valueType = QLabel(self.widget)
            valueType.setMinimumSize(QSize(300,22))
            valueType.setMaximumSize(QSize(16777215,22))
            valueType.setObjectName("valueType")
            valueType.setText(str(time[i].get_time()))
            self.listAttrValue.append(valueType)
            hboxlayout.addWidget(valueType)
            
            self.listAttrLayout.append(hboxlayout)
            self.vboxlayout.addLayout(hboxlayout)
        

    def removeAttr(self):
        incr = range(len(self.listAttrLayout))
        incr.reverse()
        for i in incr:
            self.listAttrLayout[i].removeWidget(self.listAttrName[i])
            self.listAttrLayout[i].removeWidget(self.listAttrValue[i])
    
            self.listAttrName[i].deleteLater()
            self.listAttrValue[i].deleteLater()
            self.vboxlayout.removeItem(self.listAttrLayout[i])
            self.listAttrLayout[i].deleteLater()
            self.listAttrLayout.remove(self.listAttrLayout[i])
            self.listAttrName.remove(self.listAttrName[i])
            self.listAttrValue.remove(self.listAttrValue[i])
