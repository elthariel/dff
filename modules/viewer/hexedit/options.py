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
from PyQt4.QtGui import QWidget, QHBoxLayout, QVBoxLayout, QGroupBox, QGridLayout, QLabel, QLineEdit, QComboBox, QPushButton, QSlider, QTabWidget, QMatrix, QSpinBox

from utils import *

class options(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self)
        self.init(parent)
        self.initShape()

    def init(self, parent):
        self.heditor = parent        

    def initShape(self):
        self.vbox = QVBoxLayout()
        self.optab = QTabWidget()

        self.fill = QWidget()

        self.createHexOptions()
        self.vbox.addWidget(self.optab)

        self.createButtons()
        self.vbox.addWidget(self.fill)

        self.setLayout(self.vbox)
        
    def createPageOptions(self):
        self.pagegrid = QGridLayout()
        self.pagegroup = QWidget()
        
        pagelabel = QLabel("Page size : ")
        self.sizeEdit = QFFSpinBox(self)
        self.sizeEdit.setMaximum(self.heditor.filesize)
        self.sizeEdit.setValue(self.heditor.pageSize)
#        psize = QString("%.2d" % self.heditor.pageSize)
#        self.sizeEdit.insert(psize)

        headerlabel = QLabel("Header size : ")
        self.headEdit = QFFSpinBox(self)
        self.headEdit.setMaximum(self.heditor.filesize)
        self.headEdit.setValue(self.heditor.pageHead)
#        phead = QString("%.2d" % self.heditor.pageHead)
#        self.headEdit.insert(phead)

        sparelabel = QLabel("Spare size : ")
        self.spareEdit = QFFSpinBox(self)
        self.spareEdit.setMaximum(self.heditor.filesize)
        self.spareEdit.setValue(self.heditor.pageSpare)
#        pspare = QString("%.2d" % self.heditor.pageSpare)
#        self.spareEdit.insert(pspare)
        
        ppb = QLabel("Pages per block:")
        self.pagesperblock = QComboBox()
        self.pagesperblock.addItem("8")
        self.pagesperblock.addItem("16")
        self.pagesperblock.addItem("32")
        self.pagesperblock.addItem("64")
        self.pagesperblock.addItem("128")
        self.pagesperblock.addItem("256")
        self.pagesperblock.addItem("512")
        self.pagesperblock.setCurrentIndex(2)

#        lview = QLabel("Left indication: ")
#        self.indic = QComboBox()
#        self.indic.addItem("Offset")
#        self.indic.addItem("Block")

#        self.pagesperlineEdit = QLineEdit()
#        ppl = QString("%.2d" % self.heditor.pagesPerBlock)
#        self.pagesperlineEdit.insert(ppl)

        self.pagegrid.addWidget(pagelabel, 0, 0)
        self.pagegrid.addWidget(self.sizeEdit, 0, 1)

        self.pagegrid.addWidget(headerlabel, 1, 0)
        self.pagegrid.addWidget(self.headEdit, 1, 1)

        self.pagegrid.addWidget(sparelabel, 2, 0)
        self.pagegrid.addWidget(self.spareEdit, 2, 1)

        self.pagegrid.addWidget(ppb, 3 ,0)
        self.pagegrid.addWidget(self.pagesperblock, 3, 1)

#        self.pagegrid.addWidget(lview, 4, 0)
#        self.pagegrid.addWidget(self.indic, 4, 1)

        self.pagegrid.addWidget(self.fill, 5, 0)
        self.pagegrid.setRowStretch(5, 1)
#        self.pagegrid.addWidget(self.fill, 6, 0)

#        self.pagegrid.addWidget(pagesperline, 6, 0)
#        self.pagegrid.addWidget(self.pagesperlineEdit, 7, 0)

        self.pagegroup.setLayout(self.pagegrid)
        self.vvbox.addWidget(self.pagegroup)

#        self.optab.insertTab(1, self.pagegroup, "Pages" )

#        self.vbox.addWidget(self.pagegroup)

    def createHexOptions(self):
        self.vvbox = QVBoxLayout()
        self.vcontainer = QWidget()

        self.hexgroup = QWidget()

        self.hexgrid = QGridLayout()

        groupebylabel = QLabel("Groupe by:")
        self.groupeby = QComboBox()
        self.groupeby.addItem("1")
        self.groupeby.addItem("2")
        self.groupeby.addItem("4")

        offsetlabel = QLabel("Offset as")
        self.offsetas = QComboBox()
        self.offsetas.addItem("Hexadecimal")
        self.offsetas.addItem("Decimal")


#        self.hexgrid.addWidget(groupebylabel, 0, 0)
#        self.hexgrid.addWidget(self.groupeby, 1, 0)
        self.hexgrid.addWidget(offsetlabel, 0, 0)
        self.hexgrid.addWidget(self.offsetas, 0, 1)
#        self.hexgrid.addWidget(self.fill, 2, 0)
#        self.hexgrid.setRowStretch(2, 1)

        self.hexgroup.setLayout(self.hexgrid)
        
        self.vvbox.addWidget(self.hexgroup)

        self.createPageOptions()

        self.vcontainer.setLayout(self.vvbox)

        self.optab.insertTab(0, self.vcontainer, "General")

#        self.vbox.addWidget(self.hexgroup)

        #Offset as decimal / hexadecimal



    def createButtons(self):
        self.applyB = QPushButton("Apply")
        self.connect(self.applyB, SIGNAL('clicked()'), self.apply)

        self.vbox.addWidget(self.applyB)

    def checkValue(self, value):
        try:
            n = int(value)
            return n
        except ValueError:
            return -1

    def apply(self):
        #PAGE CHECK
        pagesize = self.sizeEdit.value()
        headsize = self.headEdit.value()
        sparesize = self.spareEdit.value()
        pagesperblock = self.checkValue(self.pagesperblock.currentText())

        if (pagesize < 0) or (headsize < 0) or (sparesize < 0) or (pagesperblock < 0):
            print "Wrong values"
        else:
            offas = self.offsetas.currentText()
            if offas == "Decimal":
                self.heditor.decimalview = True
            elif offas == "Hexadecimal":
                self.heditor.decimalview = False
            #Hexview refresh
            self.heditor.readOffset(self.heditor.currentOffset)
            self.heditor.refreshPageValues(headsize, pagesize, sparesize, pagesperblock)





