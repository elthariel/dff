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
#  Jeremy Mounier <jmo@digital-forensic.org>
# 


from PyQt4.QtGui import *
from PyQt4.QtCore import *

class selection():
    def __init__(self, parent):
        self.init(parent)
        self.initFont()

    def init(self, parent):
        #Parent widgets and items
        self.heditor = parent
        self.hexitem = parent.whex.hexitem
        self.asciitem = parent.whex.asciitem

        #Start selection
        self.xstart = 0
        self.ystart = 0
        #End Selection
        self.xend = 0
        self.yend = 0

        self.length = 0
        self.offset = 0
        self.startoffset = 0
        self.endoffset = 0
        self.way = 0

    def initFont(self):
        self.font = QFont("Gothic")
        self.font.setFixedPitch(1)
        self.font.setBold(False)
        self.font.setPixelSize(14)

    def setWay(self):
        if ((self.xend - self.xstart) < 0) or ((self.yend - self.ystart) < 0):
            self.way = 0
        else:
            self.way = 1

    def setData(self):
        startoff = self.heditor.currentOffset + ((self.ystart * self.heditor.bytesPerLine) + self.xstart)
        endoff = self.heditor.currentOffset + ((self.yend * self.heditor.bytesPerLine) + self.xend)
        len = endoff - startoff
        if len < 0:
            len = len * -1
            self.offset = startoff - len
            self.startoffset = self.offset
            self.xinit = self.xend
            self.yinit = self.yend
        else:
            self.offset = startoff + len
            self.startoffset = startoff
            self.xinit = self.xstart
            self.yinit = self.ystart
        self.length = len

    def setCount(self):
        self.ycount = self.length / self.heditor.bytesPerLine
        self.xcount = self.length % self.heditor.bytesPerLine
        if self.way > 0:
            self.xcount += 1

    def select(self, xstart, ystart, xend, yend, first = False):
        self.resetSelection()
        if first:
            self.xstart = xstart
            self.ystart = ystart
            self.xend = xend
            self.yend = yend
        else:
            self.xend = xend
            self.yend = yend
        #Set Data selection
        self.setWay()
        self.setData()
        self.setCount()

        self.heditor.whex.hexcursor.update()
        self.heditor.whex.asciicursor.update()
        
        #Colorize process
        if self.length > 0:
            self.colorize()

    def update(self):
        self.initStartPosition()
        if self.length > 0:
            self.colorize()

    def initStartPosition(self):
        if self.way > 0:
            startrange = (self.offset - self.length) - self.heditor.currentOffset
        else:
            startrange = self.offset - self.heditor.currentOffset

        if startrange < 0:
            len = self.length - (startrange * -1)
            if len < 0:
                len = 0
            startrange = 0
        else:
            len = self.length

        self.yinit = startrange / self.heditor.bytesPerLine
        self.xinit = startrange % self.heditor.bytesPerLine

        self.ycount = len / self.heditor.bytesPerLine
        self.xcount = len % self.heditor.bytesPerLine

    def colorize(self):
        #Get hex cursor
        hexcur = self.getCursorSelection(0)
        self.colorizeCursor(hexcur, 0)
        asciicur = self.getCursorSelection(1)
        self.colorizeCursor(asciicur, 1)

    def getCursorSelection(self, item):
        #Init Position
        if item == 0:
            #Hexadecimal
            cursor = self.hexitem.textCursor()
            xway = QTextCursor.NextWord
        else:
            #Ascii
            cursor = self.asciitem.textCursor()
            xway = QTextCursor.NextCharacter

        cp = 0
        while cp < self.yinit:
            cursor.movePosition(QTextCursor.Down, QTextCursor.MoveAnchor)
            cp += 1
        cp = 0
        while cp < self.xinit:
            cursor.movePosition(xway, QTextCursor.MoveAnchor)
            cp += 1

        #Move Cursor
        cp = 0
        while cp < self.ycount:
            cursor.movePosition(QTextCursor.Down, QTextCursor.KeepAnchor)
            cp += 1

        cp = 0            
        while cp < self.xcount:
            cursor.movePosition(xway, QTextCursor.KeepAnchor)
            cp += 1

        return cursor
    
    #Item: 0 hex 1 ascii
    def colorizeCursor(self, cursor, item):
        format = QTextCharFormat()
        format.setFont(self.font)
        if item == 0:
            format.setForeground(QBrush(QColor(Qt.blue)))
        else:
            format.setForeground(QBrush(QColor(Qt.blue)))
        cursor.setCharFormat(format)

    def resetSelection(self):
        self.resetColorSelection(self.hexitem.textCursor())
        self.resetColorSelection(self.asciitem.textCursor())

    def resetColorSelection(self, cursor):
        #Set Format
        bformat = QTextCharFormat()
        bformat.setFont(self.font)
        #Set Black Color
        cursor.movePosition(QTextCursor.Start)
        cursor.movePosition(QTextCursor.End, QTextCursor.KeepAnchor)
        cursor.setCharFormat(bformat)
        cursor.movePosition(QTextCursor.Start)

    def hexCopy(self):
        if self.way > 0:
            off = self.offset - self.length
        else:
            off = self.offset

        buff = self.heditor.readHexValue(off, self.length)
#        print buff

    def createToolBar(self):
        self.toolbar = QToolBar()

        self.copy = QAction(QIcon(":bookmark_add.png"),  "Copy selection",  self.toolbar)
        self.toolbar.addAction(self.copy)

        
