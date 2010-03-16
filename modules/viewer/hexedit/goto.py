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

from PyQt4.QtCore import QString, Qt, SIGNAL, QLineF
from PyQt4.QtGui import QWidget, QHBoxLayout, QVBoxLayout, QGroupBox, QLabel, QGridLayout, QComboBox, QLineEdit, QPushButton, QCheckBox

class goto(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self)
        self.init(parent)
        self.initShape()

    def init(self, parent):
        self.heditor = parent
        
    def initShape(self):
        self.vbox = QVBoxLayout()
        self.createGoto()
        self.createOptions()

        #Go button
        self.gobutton = QPushButton("Go!")
        self.connect(self.gobutton, SIGNAL('clicked()'), self.go)
        self.vbox.addWidget(self.gobutton)
       
        fill = QWidget()
        self.vbox.addWidget(fill)
        self.setLayout(self.vbox)

    def createGoto(self):
        self.offbox = QGroupBox("Go to location")
        self.offgrid = QGridLayout()

        #Format
        formatlabel = QLabel("Format :")
        self.format = QComboBox()
        self.format.addItem("Hexadecimal")
        self.format.addItem("Decimal")
        #Type: Offset, Page, Block
        typelabel = QLabel("Type :")
        self.type = QComboBox()
        self.type.addItem("Offset")
        self.type.addItem("Page")
        self.type.addItem("Block")
        #Place
        offsetlabel = QLabel("Place :")
        self.offset = QLineEdit()

        self.offgrid.addWidget(formatlabel, 0, 0)
        self.offgrid.addWidget(self.format, 0, 1)

        self.offgrid.addWidget(typelabel, 1, 0)
        self.offgrid.addWidget(self.type, 1, 1)

        self.offgrid.addWidget(offsetlabel, 2, 0)
        self.offgrid.addWidget(self.offset, 2, 1)

#        self.offgrid.addWidget(self.gobutton, 6, 0)

        self.offbox.setLayout(self.offgrid)
        self.vbox.addWidget(self.offbox)

    def createOptions(self):
        self.optbox = QGroupBox("Options")
        self.optgrid = QGridLayout()

        self.fromcursor = QCheckBox("From cursor")
        self.backwards = QCheckBox("Backwards")

        self.optgrid.addWidget(self.fromcursor, 0, 0)
        self.optgrid.addWidget(self.backwards, 1, 0)

        self.optbox.setLayout(self.optgrid)
        self.vbox.addWidget(self.optbox)

    def checkLocation(self, str, base, type):
        offset = QString(str)
        off = offset.toULongLong(base)
        if off[1]:
            if type == "Offset":
                if off[1] < self.heditor.filesize:
                    return off[0]
                else:
                    print "Offset too high"
                    return -1
            elif type == "Page":
                if off[1] < self.heditor.pages:
                    return off[0]
                else:
                    print "Page too high"
                    return -1
            elif type == "Block":
                if off[1] < self.heditor.blocks:
                    return off[0]
                else:
                    print "Block too high"
                    return -1
            else:
                return -1
        else:
            return -1
        return -1

    def getOffset(self, offset, fromcursor, back, type):
        #Init position
        if type == "Offset":
            if fromcursor:
                off = self.heditor.currentOffset
                if back:
                    off -= offset
                else:
                    off += offset
            else:
                if back:
                    off = self.heditor.filesize - offset
                else:
                    off = offset
            return off
        elif type == "Page":
            if fromcursor:
                off = self.heditor.currentPage
                if back:
                    off -= offset
                else:
                    off += offset
            else:
                if back:
                    off = self.heditor.pages - offset
                else:
                    off = offset
            return (off * self.heditor.pageSize)
        elif type == "Block":
            if fromcursor:
                off = self.heditor.currentBlock
                if back:
                    off -= offset
                else:
                    off += offset
            else:
                if back:
                    off = self.heditor.blocks - offset
                else:
                    off = offset
            return (off * (self.heditor.pageSize * self.heditor.pagesPerBlock))
        else:
            return -1
        return -1

    def go(self):
        format = self.format.currentText()
        off = self.offset.text()
        type = self.type.currentText()

        opt_fromcursor = self.fromcursor.isChecked()
        opt_backwards = self.backwards.isChecked()

        if format == "Hexadecimal":
            offset = self.checkLocation(str(off), 16, type)
        else:
            offset = self.checkLocation(str(off), 10, type)

        if offset != -1:
            off = self.getOffset(offset, opt_fromcursor, opt_backwards, type)
            if off != -1:
                self.heditor.readOffset(off)
            else:
                print "Get Offset ERROR"
        else:
            print "Check value error"

