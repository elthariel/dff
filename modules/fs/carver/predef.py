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
#  Frederic B. <fba@digital-forensic.org>

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from typeSelection import *

import string

import time

class predefPattern(QTreeWidget):
    def __init__(self):
        QTreeWidget.__init__(self)
        self.setHeaderLabel("Predefined patterns")
        self.typeItems = []
        self.populate()

    def populate(self):
        for mimetype, mimecontent in filetypes.iteritems():
            qtwi = QTreeWidgetItem([mimetype])
            qtwi.setFlags(Qt.ItemIsUserCheckable|Qt.ItemIsEnabled|Qt.ItemIsSelectable)
            qtwi.setCheckState(0, Qt.Unchecked)
            self.typeItems.append(qtwi)
            self.connect(self, SIGNAL("itemClicked(QTreeWidgetItem *, int)"), self.clicked)
            self.connect(self, SIGNAL("itemPressed(QTreeWidgetItem *, int)"), self.clicked)
            for type, value in mimecontent.iteritems():
                childqtwi = QTreeWidgetItem([type])
                childqtwi.setFlags(Qt.ItemIsUserCheckable|Qt.ItemIsEnabled|Qt.ItemIsSelectable)
                childqtwi.setCheckState(0, Qt.Unchecked)
                qtwi.addChild(childqtwi)
        self.setColumnCount(1)
        self.insertTopLevelItems(0, self.typeItems)

    def setCheckStateOfChildren(self, item, column, checked):
        children = item.childCount()
        for i in range(0, children):
            item.child(i).setCheckState(0, checked)

    def isAllChildren(self, item, column):
        children = item.childCount()
        checked = 0
        for i in range(0, children):
            if item.child(i).checkState(column) == Qt.Checked:
                checked += 1
        if checked == 0:
            item.setCheckState(0, Qt.Unchecked)
        elif item.checkState(column) == Qt.Unchecked:
            item.setCheckState(0, Qt.Checked)

    def clicked(self, item, column):
        if item.childCount() != 0:
            if item.checkState(column) == Qt.Checked:
                self.setCheckStateOfChildren(item, column, Qt.Checked)
            else:
                self.setCheckStateOfChildren(item, column, Qt.Unchecked)
        else:
            parent = item.parent()
            if parent != None and parent.childCount() != 0:
                self.isAllChildren(parent, column)

    def createGroupBox(self, items):
        gb = QGroupBox(items["type"])
        gb.setCheckable(True)
        gb.setChecked(False)
        vbox = QVBoxLayout()
        for item in items["value"]:
            button = QCheckBox(item)
            vbox.addWidget(button)
        vbox.addStretch(1)
        gb.setLayout(vbox)
        return gb

    def getChecked(self):
        selected = {}
        for typeItem in self.typeItems:
            i = 0
            if typeItem.checkState(0) == Qt.Checked:
                type = str(typeItem.text(0))
                selected[type] = []
                children = typeItem.childCount()
                for i in range(0, children):
                    child = typeItem.child(i)
                    if child.checkState(0) == Qt.Checked and not child.isDisabled():
                        child.setDisabled(True)
                        selected[type].append(str(child.text(0)))
                        i += 1
                if i > 0:
                    typeItem.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
            
        return selected
