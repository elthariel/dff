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

import binascii
import struct
import string
import time

from cursors import *

from PyQt4.QtCore import QString, Qt
from PyQt4.QtGui import QWidget, QFont, QColor, QTextCursor, QGraphicsTextItem, QGraphicsItem, QPen, QFontMetrics

class asciiItem(QGraphicsTextItem):
    def __init__(self, whex):
        QGraphicsTextItem.__init__(self)
        self.initValues(whex)
        self.initPosition()
        self.initFont()
        self.initMetricsValues()
#        self.initCursor()

    def initPosition(self):
        self.setPos(485, 25)
#        self.setTextInteractionFlags(Qt.TextSelectableByMouse)

    def initValues(self, whex):
        self.whex = whex
        self.heditor = self.whex.heditor
        #Buffer
        self.buffer = []
        self.bufferLines = 0 
        #Line
        self.currentLine = 0
        #Offset
        self.startOffset = 0
        self.fontPixel = 14
        #Current Positions
        self.currentPos = 0

#    def initCursor(self):
#        self.cursor = asciiCursor(self)
#        self.heditor.scene.addItem(self.cursor)

    def initFont(self):
        self.setDefaultTextColor(QColor(Qt.darkCyan))

        self.font = QFont("Gothic")
        self.font.setFixedPitch(1)
        self.font.setBold(False)
        self.font.setPixelSize(self.fontPixel)
        self.setFont(self.font)
        self.metric = QFontMetrics(self.font)

    def initMetricsValues(self):
        #Calibrate
        calibrate = QString("A")
        self.charsByByte = 1
        self.charW = self.metric.width(calibrate)
        self.charH = self.metric.height()

        self.byteW = self.charW * self.charsByByte
        self.byteH = self.charH

    def initStartBlank(self):
        self.lineW = self.boundingRect().width()
        self.startBlank = self.lineW - (self.byteW * 16)
#        print "start ASCII blank"
#        print self.startBlank

    #Print Operations
    def printBuffer(self, buff):
        del self.buffer
        self.buffer = buff

        count = 0
        printer = QString()

        for char in buff:
            if char > "\x20" and char < "\x7e":
               printer.append(char)
            else:
                printer.append(".")
            if count < 15:
                count += 1
            else:
                printer.append("\n")
                count = 0

        #Clear and set
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.Start)
        cursor.movePosition(QTextCursor.End, QTextCursor.KeepAnchor)
        self.setPlainText(printer)
        cursor.movePosition(QTextCursor.Start)
        #Update pixel Informations

    def updateCurrentSelection(self, posx, posy):
        self.currentSelection = self.heditor.currentOffset + ((posy * 16) + posx)

    def getXPos(self, x):
        count = 0
        current = self.byteW + (self.startBlank / 2)
        while current < x:
            count += 1
            current = current + self.byteW
        return count

    def getYPos(self, y):
        count = 0
        current = self.byteH
        while current < y:
            count += 1
            current = current + self.byteH
        return count

    def mouseMoveEvent(self, event):
        pos = event.pos()
        x = pos.x()
        y = pos.y()
        xpos = self.getXPos(x)
        ypos = self.getYPos(y)
        self.heditor.selection.select(self.heditor.selection.xstart, self.heditor.selection.ystart, xpos, ypos)
        self.heditor.infos.update()
        self.heditor.right.decode.update()

    def mousePressEvent(self, event):
        button = event.button()
        pos = event.pos()

        if event.button() == 1:
            #Get Clicked coordonates
            x = pos.x()
            y = pos.y()
            #Transform pixel into cursor position
            xpos = self.getXPos(x)
            ypos = self.getYPos(y)

            self.whex.asciicursor.draw(xpos, ypos)
            self.whex.hexcursor.draw(xpos, ypos)
            #Refresh hexadecimal cursor
            self.heditor.selection.select(xpos, ypos, xpos, ypos, True)
            self.heditor.right.decode.update()
            self.heditor.infos.update()


    def mouseReleaseEvent(self, event):
        pass
