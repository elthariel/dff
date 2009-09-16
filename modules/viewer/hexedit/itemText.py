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
#  Jeremy Mounier <jmo@digital-forensic.org>
# 

from PyQt4.QtGui import *
from PyQt4.QtCore import *

class hexItem(QGraphicsTextItem):
    def __init__(self, parent,  buffer):
        QGraphicsTextItem.__init__(self,  buffer)
        self.hexedit = parent
        #self.setFlag(QGraphicsItem.ItemIsFocusable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        
        self.setAcceptsHoverEvents(True)
        
        self.font = QFont("Courier")
        self.font.setFixedPitch(1)
        self.font.setBold(True)
        self.setFont(self.font)
        
        #self.setDefaultTextColor(Qt.darkRed)
        #brush = QBrush(Qt.NoBrush)
    def mousePressEvent(self,  event):
        pos = self.pos()
        x = pos.x()
        y = pos.y()        
        blockoffset = 0
        xpos = 0
        ypos = 0
        
        x -= 115
        
        #Item position to offset
        xpos = x / 25
        ypos = y / 20

        blockoffset = int((ypos * 16) + xpos)
        
        self.hexedit.scene.clearSelection()
        self.setSelected(True)
        
        self.hexedit.iteAscMap[blockoffset].setSelected(True)
        
        #selected = self.hexedit.scene.selectedItems()

        self.hexedit.CurrentOffset = (self.hexedit.CurrentSector * self.hexedit.sectorSize) + blockoffset
        
        self.hexedit.navigation.updateInformations()
        
        if self.hexedit.CurrentOffset < (self.hexedit.filesize - 3) :
            self.hexedit.navigationValues.update()        
        
    def mouseReleaseEvent(self,  event):
        pass
        
class asciiItem(QGraphicsTextItem):
    def __init__(self, parent,  buffer):
        QGraphicsTextItem.__init__(self,  buffer)
        self.setFlag(QGraphicsItem.ItemIsFocusable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        
        self.hexedit = parent

        self.setAcceptsHoverEvents(True)
        
        self.font = QFont("Courier")
        self.font.setFixedPitch(1)
        self.font.setBold(False)
        self.setFont(self.font)
        
    def mousePressEvent(self,  event):
        pos = self.pos()
        x = pos.x()
        y = pos.y()   
        blockoffset = 0
        xpos = 0
        ypos = 0
        
        x -= 530

        #Item position to offset
        xpos = x / 10
        ypos = y / 20

        blockoffset = int((ypos * 16) + xpos)
        
        self.hexedit.scene.clearSelection()
        self.setSelected(True)
        
        self.hexedit.iteHexMap[blockoffset].setSelected(True)
        self.hexedit.CurrentOffset = (self.hexedit.CurrentSector * self.hexedit.sectorSize) + blockoffset
        self.hexedit.navigation.updateInformations()

        if self.hexedit.CurrentOffset < (self.hexedit.filesize - 3) :
            self.hexedit.navigationValues.update()

    def mouseReleaseEvent(self,  event):
        pass
        

class offItem(QGraphicsTextItem):
    def __init__(self, parent,  buffer):
        QGraphicsTextItem.__init__(self,  buffer)
        self.setFlag(QGraphicsItem.ItemIsFocusable)
        self.setAcceptsHoverEvents(True)
        
        self.font = QFont("Courier")
        self.font.setFixedPitch(1)
        self.font.setBold(True)
        self.setFont(self.font)
        self.setDefaultTextColor(Qt.red)
