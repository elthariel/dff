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

import binascii
import struct
import string

from itemText import *

from GView import *
from Navigation import *
from NavigationValues import *

from api.vfs import *
from api.vfs.libvfs import *

from PyQt4.QtGui import *
from PyQt4.QtCore import *

class Heditor(QSplitter):
    def __init__(self, parent):
        super(Heditor,  self).__init__(parent)
        self.vfs = vfs.vfs()
        
    def initFile(self, node):
        self.node = node
        self.file = node.open()
        self.filesize = self.file.node.attr.size
        
        self.initInfos()
        self.initBaseShape()
        
        #First Read and Sector Shape Creation
        try:
            self.file.seek(0)
            buffer = self.file.read(self.sectorSize)
            self.createSectorShape(buffer)
        except vfsError,  e:
            print "error first read"

    def initInfos(self):
        self.CurrentOffset = 0
        self.CurrentSector = 0
        self.sectorSize = 1024

        self.hexoffset = False
        
        self.sectors = self.filesize / self.sectorSize

    def initBaseShape(self):
        self.wiew = QVBoxLayout()
        
        self.navigation = Navigation(self)
        self.wiew.addWidget(self.navigation)
        
        ##View here scroll bar?

        self.view = GView(self)

        self.wiew.addWidget(self.view)
        self.widwiew = QWidget()
        self.widwiew.setLayout(self.wiew)
        self.insertWidget(0, self.widwiew)

        self.view.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        self.view.setAlignment(Qt.AlignLeft)
        
        ## Scene
        self.scene = QGraphicsScene()
        self.scene.setBackgroundBrush(Qt.white)
        self.view.setScene(self.scene)

        self.navigationValues = NavigationValues(self)
        self.wiew.addWidget(self.navigationValues)

    def createSectorShape(self,  buffer):
        self.iteOffMap = []
        self.iteHexMap = []
        self.iteAscMap = []
        cp = 0
        offset = 0
        
        buff = QString()
        pos = str(len(buffer)) + 'B'
        block = struct.unpack(pos, buffer)
        
        #Fill and add ascii istem to map
        for char in buffer:
            if char in string.printable:
                ascii = asciiItem(self,  char)
            else:
                ascii = asciiItem(self,  ".")
            self.iteAscMap.append(ascii)
        
        #print self.iteAscMap[16].toPlainText()
            
        #Fill and add Hexa item to map
        for index in block:
            buff = "%.2x" % index
            item = hexItem(self, buff)
            if not cp % 2:
                item.setDefaultTextColor(Qt.blue)
                self.iteHexMap.append(item)
            else:
                self.iteHexMap.append(item)


            if cp < 16:
                cp +=1
            else:
                oitem =  "%.10d" % offset
                offitem =  offItem(self,  oitem)
                self.iteOffMap.append(offitem)
                offset += 16
                cp = 1

        #Last one
        oitem =  "%.10d" % offset
        offitem =  offItem(self,  oitem)
        self.iteOffMap.append(offitem)


        self.mapOffset(20)
        self.mapHexa()
        self.mapAscii()
        
    def mapOffset(self,  height):
        x = 0
        y = 0
        cp = 0
        for i in self.iteOffMap:
            i.setPos(x,  y)
            y += height
            self.scene.addItem(i)
    
    def mapHexa(self):
        startx = 115
        x = startx
        y = 0
        cp = 0
        for i in self.iteHexMap:
            if cp < 16:
                i.setPos(x,  y)                
                self.scene.addItem(i)
                x += 25
                cp += 1
            else:
                x = startx
                y += 20
                i.setPos(x,  y)
                self.scene.addItem(i)
                x += 25
                cp = 1
                
    def mapAscii(self):
        startx = 530
        x = startx
        y = 0
        cp = 0
        for i in self.iteAscMap:
            if cp < 16:
                i.setPos(x,  y)
                self.scene.addItem(i)
                x += 10
                cp += 1
            else:
                x = startx
                y += 20
                i.setPos(x,  y)
                self.scene.addItem(i)
                x += 10
                cp = 1
        
    def fillEndBlock(self,  cp,  map):
        itemlen = len(map)
        count = cp
        
        while count < itemlen:
            map[count].hide()
            count += 1

    def refreshSectorOffsetItems(self, off = None):
        if off == None:
            offset = (self.CurrentOffset / self.sectorSize) * self.sectorSize
        else:
            offset = off
    
        startoff = offset
        cp = 0

        for item in self.iteOffMap:
            if not self.hexoffset:
                oitem =  "%.10d" % offset
            else:
                oitem =  "%.10x" % offset
            self.iteOffMap[cp].setVisible(True)

            self.iteOffMap[cp].setPlainText(oitem)
            offset += 16
            cp += 1
            
        if self.CurrentSector == self.sectors:
            lines = (self.filesize - startoff) / 16
            while lines < len(self.iteOffMap) - 1:
                lines +=1
                self.iteOffMap[lines].hide()
                
        
    def refreshSectorHexItems(self,  buffer):
        buff = QString()
        pos = str(len(buffer)) + 'B'
        block = struct.unpack(pos, buffer)
        cp = 0
        
        for index in block:
            buff = "%.2x" % index
            self.iteHexMap[cp].setVisible(True)
            self.iteHexMap[cp].setPlainText(buff)
            cp += 1
        
        if self.CurrentSector == self.sectors:
            self.fillEndBlock(cp,  self.iteHexMap)
    
    def refreshSectorAscItems(self,  buffer):
        cp = 0

        for char in buffer:
            if char in string.printable:
                self.iteAscMap[cp].setVisible(True)
                self.iteAscMap[cp].setPlainText(char)
            else:
                self.iteAscMap[cp].setPlainText(".")
            cp += 1
            
        if self.CurrentSector == self.sectors:
            self.fillEndBlock(cp,  self.iteAscMap)
        
    #Refresh sector shape update Items from buffer
    def refreshSectorShape(self, buffer, off = None):
        if off == None:
            self.refreshSectorOffsetItems(None)
        else:
            self.refreshSectorOffsetItems(off)

        self.refreshSectorHexItems(buffer)
        self.refreshSectorAscItems(buffer)
        #for offItem in self.iteOffMap

    def readSector(self):
        #seek
        start = (self.CurrentOffset / self.sectorSize) * self.sectorSize
        try:
            self.file.seek(start)
            buffer = self.file.read(self.sectorSize)
            self.refreshSectorShape(buffer)
        except vfsError,  e:
            print "Read error"
