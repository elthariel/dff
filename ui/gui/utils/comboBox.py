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

from PyQt4.QtGui import QComboBox
from PyQt4.QtCore import QVariant
from utils import DFF_Utils

class DFF_ComboBoxNode(QComboBox):
    def __init__(self, parent):
        QComboBox.__init__(self,  parent)
        self.dictNode = {}
        self.dictIndex = {}
        
    def addPathAndSelect(self, node,  index = 0):
        path = DFF_Utils.getPath(node)
        
        for i in range(0, self.count()):
            if self.itemText(i) == path :
                self.setCurrentIndex(i)
                return False
        
        self.dictNode[path] = node
        self.dictIndex[path] = index
        self.addItem(path)
        self.setCurrentIndex(self.count() - 1)
        return True
    
    def addPath(self, node,  index = 0):
        path = DFF_Utils.getPath(node)
        for i in range(0, self.count()):
            if self.itemText(i) == path :
                return False
        self.addItem(path)
        self.dictNode[path] = node
        self.dictIndex[path] = index
        return True
    
    def currentNode(self):
        path = self.currentText()
        return self.dictNode[str(path)]
    
    def getNode(self, path):
        try :
            return self.dictNode[path]
        except :
            return None
    
    def getBrowserIndex(self, path):
        return self.dictIndex[path]

class DFF_ComboBoxString(QComboBox):
    def __init__(self, parent):
        QComboBox.__init__(self,  parent)
        
    def addPathAndSelect(self, path):
        for i in range(0, self.count()):
            if self.itemText(i) == path :
                self.setCurrentIndex(i)
                return False
        self.addItem(path)
        self.setCurrentIndex(self.count() - 1)
        return True
    
    def addPath(self, path):
        for i in range(0, self.count()):
            if self.itemText(i) == path :
                return False
        self.addItem(path)
        return True
        
class DFF_ComboBoxBool(QComboBox):
    def __init__(self, parent):
        QComboBox.__init__(self,  parent)
        self.addItem("True")
        self.addItem("False")
