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

from PyQt4.QtGui import QPixmap
from PyQt4.QtCore import QAbstractItemModel, QModelIndex, Qt, QVariant 

from api.vfs import *

from DirModelItem import DirModelItem
from ui.gui.utils.utils import DFF_Utils

class DirModel(QAbstractItemModel):
    # TAKE :        headers : StringList ( For header Column )
    #                   data : QString ( For Fill the tree )
    def __init__(self, headers):
        QAbstractItemModel.__init__(self)
        self.vfs = vfs.vfs()
        self.rootItem = DirModelItem(headers)
        self.rootItem.setNode(None)
    
    def addRootVFS(self):
        self.rootItem.insertChildren(0, 1, 1)
        self.rootItemVFS = self.rootItem.child(0)
        self.rootItemVFS.setData(0, "/")
        self.rootItemVFS.setNode(self.vfs.getnode("/"))

    # TAKE :        Parent : QModelIndex
    # RETURN :  True or False
    def hasChildren(self, parent):
        item = self.getItem(parent)
        if self.rowCount(parent) == 0 :
            return False
        else :
            return True
    
    # TAKE :        parent : QModelIndex
    # RETURN :  int
    def columnCount(self, parent):
        return self.rootItem.columnCount()
        #return 1
    
    # TAKE :        index : QModelIndex
    #                   role : int
    # RETURN :  QVariant
    def data(self, index,  role):
        if not index.isValid():
            return QVariant()
#XXX partition / folder
        if role == Qt.DecorationRole :
            if self.getItem(index).nodeVFS.is_file :
                #icon = QPixmap(":dff_partition.png")
                icon = QPixmap(":dff_folder.png")
            else:
                icon = QPixmap(":dff_folder.png")
            return QVariant(icon)
        
        if role != Qt.DisplayRole and role != Qt.EditRole :
            return QVariant()
                    
        item = self.getItem(index)
        
        if item:
            return QVariant(item.data(index.column()))
        else :
            return QVariant()
        
    # TAKE :        Index : QModelIndex
    # RETURN :  Qt.ItemFlags
    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled
        return Qt.ItemFlags(QAbstractItemModel.flags(self, index) )

    # TAKE :        Section : QModelIndex
    #                   Orientation : Qt.Orientation
    #                   Role : int
    # RETURN :  QVariant
    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.rootItem.data(section))
        return QVariant()
    
    # TAKE :        Row : int
    #                   Column : int
    #                   Parent : QModelIndex
    # RETURN :  QModelIndex
    def index(self, row, column, parent):
        if self.hasIndex(row,column,parent) == False:
            return QModelIndex()
            
        if parent.isValid()== False :
            parentItem = self.rootItem
        else:
            parentItem = self.getItem(parent)
        
        childItem =  parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else :
            return QModelIndex()

    # TAKE :        Position : int
    #                   Columns : int
    #                   Parent : QModelIndex
    # RETURN :  True or False
    def insertColumns(self, position, columns, parent):
        success = False
        
        beginInsertColumns(parent, position, position + columns - 1)
        success = self.rootItem.insertColumns(position, columns)
        endInsertColumns()
        
        return success
    
    # TAKE :        Position : int
    #                   Rows : int
    #                   Parent : QModelIndex
    # RETURN :  True or False
    def insertRows(self, position, rows, parent):
        parentItem = self.getItem(parent)
        success = False
            
        beginInsertRows(parent, position, position + rows - 1)
        success = parentItem.insertRows(position, rows)
        endInsertRows()
        
        return success
    
    # TAKE :        Parent : QModelIndex
    # RETURN :  QModelIndex
    def parent(self, index):
        if not index.isValid() :
            return QModelIndex()
        childItem = self.getItem(index)
        parentItem =  childItem.parent()
        
        if parentItem == self.rootItem:
            return QModelIndex()
        if parentItem :
            return self.createIndex(parentItem.childNumber(), 0,  parentItem)
        return QModelIndex()
    
    # TAKE :        Parent : QModelIndex
    # RETURN :  QModelIndex
    def parent2(self, index):
        if index is None :
            return False
        if not index.isValid() :
            return False
        childItem = self.getItem(index)
        parentItem =  childItem.parent()
        if parentItem == self.rootItem:
            return False
        if parentItem : 
            return self.createIndex(parentItem.childNumber(), 0,  parentItem)
        return False
        
    def indexWithNode(self, node):
        theItem = self.rootItemVFS
        list = DFF_Utils.getPath(node).split('/')
        for j in range(0, len(list)):
            for i in range(0,  theItem.childCount()) :
                if theItem.child(i):
                    if str(theItem.child(i).nodeVFS.name) == str(list[j]):
                        theItem = theItem.child(i)
                        i = theItem.childCount()
        return self.createIndex(theItem.childNumber(), 0,  theItem)

    # TAKE :        Row : int
    #                   Columns : int
    #                   Parent : QModelIndex
    # RETURN :  True or False
    def removeColumns(self, position, columns, parent):
        success = False
        
        beginRemoveColumns(parent, position, position + columns - 1)
        success = self.rootItem.removeColumns(position, columns)
        endRemoveColumns()
        
        return success
    
    # TAKE :        Position : int
    #                   Rows : int
    #                   Parent : QModelIndex
    # RETURN :  True or False
    def removeRows(self, position, rows, parent):
        parentItem = self.getItem(parent)
        success = False
            
        beginRemoveRows(parent, position, position + rows - 1)
        success = parentItem.removeRows(position, rows)
        endRemoveRows()
        
        return success
        
    # TAKE :        Parent : QModelIndex
    # RETURN :  int
    def rowCount(self, parent):
        #if parent.isValid():
        return self.getItem(parent).childCount()
        #else:
        #    return self.rootItem.childCount()
    
    # TAKE :        Index : QModelIndex
    #                   Value : QVariant
    #                   role : int
    # RETURN :  True or False
    def setData(self, index, value, role):
        if role != Qt.EditRole:
            return False
        item = self.getItem(index)
        return item.setData(index.column(), value)
    
    # TAKE :        Section : int
    #                   Orientation : Qt.Orientation
    #                   Value : QVariant
    #                   Role : int
    # RETURN :  True or False
    def setheaderData(self, section, orientation, value, role):
        if role != Qt.EditRole or orientation!= Qt.Horizontal:
            return False
        return self.rootItem.setData(section,  value)
    
    # TAKE :        Index : QModelIndex
    # RETURN :  OCaseDirItemModel
    def getItem(self, index):
        if index.isValid():
            try:
                item = index.internalPointer()
                if item:
                    return item
            except:
		    pass
                    #print "probleme pointeur"
        return self.rootItem
    
    # TAKE :        Path : String
    # RETURN :  OCaseDirItemModel
    def getItemWithPath(self,  path):
        theItem = self.rootItemVFS
        list = path.split('/')
        for item in list:
            for i in range(0,  theItem.childCount()) :
                if theItem.child(i):
                    if str(theItem.child(i).nodeVFS.name) == str(item):
                        theItem = theItem.child(i)
                        i = theItem.childCount()
        return theItem
        
    def createNeedingDirectory(self,  path):
        theItem = self.rootItem
        list = path.split('/')
        currentPath = ""
        for item in list:
            find = False
            if str(item) <> "" :
                for i in range(0,  theItem.childCount()) :
                    if theItem.child(i):
                        if str(theItem.child(i).nodeVFS.name) == str(item):
                            theItem = theItem.child(i)
                            i = theItem.childCount()
                            find = True
                            currentPath = currentPath + "/" + str(item)
                if find == False :
                    currentPath = currentPath + "/" + str(item)
                    theItem.insertChildren(theItem.childCount(), 1, 1)
                    theItem.child(theItem.childCount() - 1).setData(0, str(item))
                    theItem.child(theItem.childCount() - 1).setNode(self.vfs.getnode(currentPath))
                    theItem = theItem.child(theItem.childCount() - 1)
        return theItem
        
    #   #   #   #   #   #   #   #   #   #
    #                                               #
    #   FUNCTION FOR OUR VFS   #
    #                                               #
    #   #   #   #   #   #   #   #   #   #
    
    # TAKE :        Index : OCaseDirItemModel
    # RETURN :  String ( VFSself.CaseDirModel.fillAllDirectory(self.CaseDirModel.rootItem, self.pVFS) Absolute Path )
    def getAbsolutePath(self, index):
        path = "/" + index.data(0)
        currentItem = index
        while currentItem:
            currentItem = currentItem.parent()
            if currentItem == self.rootItem:
                return path
            path = "/" + currentItem.data(0) + path
        
    # TAKE :        currentObject : OCaseDirItemModel
    # RETURN :  True or False
    def fillAllDirectory(self, currentObject):
        if currentObject.nodeVFS is None :
            return
        
        list = self.vfs.listingDirectories(currentObject.nodeVFS)
        currentList = currentObject.childItems
        delList = []
        find = None
        # Delete folder (closedump)
        for i in range(0, len(currentList)):
            j = 0
            find = None
            while j < len(list) and find == None :
                if currentList[i].nodeVFS.this == list[j].this :
                    find = 1
                j = j + 1
            if find is None :
                delList.append(currentList[i])
                
        #if len(delList) > 0 :
            #print str(currentObject.nodeVFS.name) + "CALL KRAKOSS PB DELETE ITEM SAUF SI VOUS AVEZ FAI UN DELETEDUMP" + str(len(delList))
        for i in range(0, len(delList)):
            self.deleteChild(delList[i])
            
        # Add just new folder
        if currentObject.childCount() > 0 :
            removeItem = []            
            for i in range(0, len(list)) :
                for j in range(0, currentObject.childCount()) :
                    if list[i].this == currentObject.child(j).nodeVFS.this :
                        removeItem.append(list[i])
                        self.fillAllDirectory(currentObject.child(j))

            if len(removeItem) > 0 :
                for i in range (0, len(removeItem)) :
                    list.remove(removeItem[i])
        
        if len(list) == 0 :
            return
        currentObject.insertChildren(0, len(list), 1)
        for i in range(0, len(list)) :
            currentObject.child(i).setData(0, list[i].name)
            currentObject.child(i).setNode(list[i])
            self.fillAllDirectory(currentObject.child(i))
        return
