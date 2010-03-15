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

from PyQt4.QtGui import QPixmap
from PyQt4.QtCore import QModelIndex, Qt, QVariant 

class RootItemModel():
    # TAKE :        data : QVector<Qvariant>
    #                   parent : OCaseDirItemModel
    def __init__(self, data,  parent = None):
        self.dataItem =  data
        self.parentItem = parent
        
        # spec
        self.childItems = []
        self.dump = 0
        self.node = 0
    
    # TAKE :        row : int
    # RETURN :  OCaseDirItemModel or False
    def child(self, row):
        if row >= self.childCount():
            return False
        else :
            return self.childItems[row]
    # XXX
    # TAKE :        row : int
    # RETURN :  OCaseDirItemModel or False
    def childWithNode(self, node):
        if self.childCount() < 1:
            return False
        else :
            childItems = self.childItems
            for i in childItems:
                if i.node.this == node.this:
                    return i
        return False
    
    def deleteChild(self, node):
        if self.childCount() < 1:
            return False
        else :
            childItems = self.childItems
            for i in childItems :
                if i.node.this == node.this :
                    del i
                    return True
        return False
        
    # TAKE :        None
    # RETURN :  Number of children
    def childCount(self):
        return len(self.childItems)
    
    # TAKE :        None
    # RETURN :   Position of it in his parent
    def childNumber(self):
        if self.parentItem:
            return self.parentItem.childItems.index(self)
        return 0
    
    # TAKE :        None
    # RETURN :  Number of Column
    def columnCount(self):
        return 1
    
    # TAKE :        Column of Row : int
    # RETURN :  Data for the column : QVariant
    def data(self, column):
        return self.dataItem[column]
    
    # TAKE :        Position : int
    #                    Count : int
    #                    Columns : int
    # RETURN :  true or false
    def insertChildren(self, position, count, columns):
        if position < 0 or position > len(self.childItems):
            return False
            
        for row in range(count):
            data = []
            for nbr in range(columns):  
                data.append("")
            item = RootItemModel(data, self)
            self.childItems.insert(position, item)
        return True
    
    # TAKE :        position : int
    #                    columns : int
    # RETURN :  true or false
    def insertColumns(self, position, columns):
        if position < 0 or position > len(self.dataItem):
            return False
        
        for row in range(columns):
            self.dataItem.insert(position,  QVariant())
        
        for child in self.childItems:
            child.insertColumns(position, columns)
        return True
     
    # TAKE :        None
    # RETURN :  OCaseDirItemModel
    def parent(self):
        return self.parentItem
    
    # TAKE :        Position : int
    #                   Count : int
    # RETURN :  True or False
    def removeChildren(self, position, count):
        if position < 0 or position + count > len(self.childItems):
            return False
        
        for row in range(count):
            self.childItems.remove(row)
        return True
        
    # TAKE :        Position : int
    #                   Columns : int
    # RETURN :  True or False
    def removeColumns(self, position, columns):
        if position < 0 or position + columns > len(self.dataItem):
            return False
        
        for row in range(columns):
            self.dataItem.remove(row)
        return True
        
        for child in self.childItems:
            child.removeColumns(position, columns)
    
    # TAKE :        Column : int
    #                   Value : QVariant
    # RETURN :  True or False
    def setData(self, column, value):
        if column < 0 or column >= len(self.dataItem):
            return False
        self.dataItem[column] = value
        return True
    
    # XXX
    # TAKE :        node
    # RETURN :  True or False
    def setNode(self, node):
        self.node = node
    
    # Return the level of item in order to number of parent
    def getLevel(self):
        level = 0
        tmp_item = self.parentItem
        while tmp_item != None :
            level = level + 1
            tmp_item = tmp_item.parentItem
        return level
