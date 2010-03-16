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


#For long file mode
#For scrollbar LFMOD

from hexView import *
from bookmark import *

from informations import *

from right import *

from selection import *

from api.vfs import *
from api.vfs.libvfs import *
from api.exceptions.libexceptions import *

import binascii
import struct
import string

from PyQt4.QtGui import *
from PyQt4.QtCore import *

class Heditor(QWidget):
    def __init__(self, parent):
        super(Heditor,  self).__init__(parent)
        self.mainWindow = parent
        self.vfs = vfs.vfs()
        
    def init(self, node):
        self.node = node
        self.file = node.open()
        self.filesize = self.file.node.attr.size

        self.initInfos()
        #Init view and scene
        self.initShape()
        #First Read and Sector Shape Creation
        try:
            self.file.seek(0)
            buffer = self.file.read(self.readSize)    
            self.updateCurrents(0)
            self.updateHexItems(buffer, 0, True)
            self.whex.asciicursor.draw(0, 0)
            self.whex.hexcursor.draw(0, 0)
            self.right.decode.update()
        except vfsError,  e:
            print e.error

    def initInfos(self):
        self.initOffsetInfos()
        self.initPageInfos()
        #XXX Screen size
        self.readSize = self.pageSize
        self.bytesPerLine = 16

        self.linkmode = True

        self.cursorOffset = 0
        self.groupBytes = 1

    def initOffsetInfos(self):
        #Offset
        self.currentOffset = 0
        self.decimalview = False

    def initPageInfos(self):
        #Sectors
        self.currentPage = 0
        self.startBlockOffset = 0

        self.pageSize = 512
        if self.filesize < self.pageSize:
            self.pageSize = self.filesize

        self.pageHead = 0
        self.pageSpare = 0
        self.pagesPerBlock = 32

        self.pages = self.filesize / self.pageSize
        if self.filesize % self.pageSize > 0:
            self.pages += 1

        self.blocks = self.pages / self.pagesPerBlock
        self.currentBlock = 0
        #Display offset or Block
        self.pageOffView = True

    def initShape(self):
        #General Layout : Header + View + Footer
        self.vlayout = QVBoxLayout()
        self.vlayout.setSpacing(1)


        self.vsplitter = QSplitter()
        self.lhsplitter = QSplitter()
        self.whex = wHex(self)


        self.lhsplitter.addWidget(self.whex)
 
        #Add block and pixel views
        self.initFooterViews()


        #INIT SELECTION
        self.selection = selection(self)
#        self.pageselection = pageSelection(self)

        self.lhsplitter.setOrientation(Qt.Vertical)
        self.vsplitter.addWidget(self.lhsplitter)

        self.right = righTab(self)
        self.infos = informations(self)

        self.vsplitter.addWidget(self.right)

#        self.shapeToolBars()
#        self.lhsplitter.addWidget(self.infos)

#        self.vlayout.addWidget(self.toolbars)
        self.vlayout.addWidget(self.vsplitter)
        self.vlayout.addWidget(self.infos)

        self.setLayout(self.vlayout)

    def initFooterViews(self):
        self.footab = QTabWidget()

        self.footab.setTabPosition(QTabWidget.South)
        #Bookmark
        self.book = bookmark(self)

        self.footab.insertTab(0, self.book, QIcon(":bookmark.png"), "Bookmarks")
        
        self.lhsplitter.addWidget(self.footab)

    def toLineOffset(self, lineNumber):
        return (lineNumber * self.bytesPerLine)

    def toPageOffset(self, lineNumber):
        startLineOffset = lineNumber * self.bytesPerLine
        currentPage = startLineOffset / self.pageSize
        startPageOffset = currentPage * self.pageSize
        return startPageOffset

    def refreshPageValues(self, header, size, spare, len):
        self.pageHead = header
        self.pageSpare = spare
        self.pageSize = self.pageHead + size + self.pageSpare
        self.pagesPerBlock = len


    def updateHexItems(self, buffer, offset, first = None):
        self.whex.offsetitem.printFullOffset(offset, (len(buffer) / self.bytesPerLine))
        self.whex.hexitem.dumpHexBuffer(buffer)
        self.whex.asciitem.printBuffer(buffer)
        if first:
            self.whex.hexitem.initStartBlank()
            self.whex.asciitem.initStartBlank()

    def updateCurrents(self, offset):
        self.currentOffset = offset
        self.currentPage = offset / self.pageSize
        self.currentBlock = offset / (self.pageSize * self.pagesPerBlock)


##########################################
#                SELECTION               #
##########################################


    def getSelectionPos(self):
        range = self.currentSelection - self.currentOffset
        y = (range / self.bytesPerLine)
        x = range % self.bytesPerLine


##########################################
#             READ OPERATIONS            #
##########################################

    def readOffset(self, offset):
        #Transform offset to start of its line
        line = offset / self.bytesPerLine
        readoff = line * self.bytesPerLine
        if readoff >= 0 or readoff < self.filesize:
            try:
#                print "roff: ", readoff
                self.file.seek(readoff)
                buffer = self.file.read(self.readSize)
                self.updateCurrents(readoff)
                self.updateHexItems(buffer, readoff)
                if (self.selection.offset >= readoff) and (self.selection.offset < (readoff + self.pageSize)):
                    self.selection.update()

                self.infos.update()
                self.whex.hexcursor.update()
                self.whex.asciicursor.update()

            except vfsError,  e:
                print "Read error"

    def readHexValue(self, offset, length):
        buff = []
        if (offset >= 0 or offset < self.filesize) and length > 0:
            try:
                self.file.seek(offset)
                buffer = self.file.read(length)
                pos = str(len(buffer)) + 'B'
                buff = struct.unpack(pos, buffer)
                res = QString()

                for byte in buff:
                    res.append("%.2X" % byte)
                return res
            except vfsError,  e:
                print "Read error"

    def readAsciiValue(self, offset, length):
        buff = []
        if (offset >= 0 or offset < self.filesize) and length > 0:
            try:
                self.file.seek(offset)
                buffer = self.file.read(length)
                res = QString()
                for char in buffer:
                    if char > "\x20" and char < "\x7e":
                        res.append(char)
                    else:
                        res.append(".")
                return res

            except vfsError,  e:
                print "Read error"



#    def readPage(self, line):
#        start = (self.CurrentOffset / self.pageSize) * self.pageSize
#        offset = self.toPageOffset(line)
#        try:
#            self.file.seek(offset)
#            buffer = self.file.read(self.readSize)
#            self.updateHexItems(buffer, offset)
#            self.refreshSectorShape(buffer)
#        except vfsError,  e:
#            print "Read error"

