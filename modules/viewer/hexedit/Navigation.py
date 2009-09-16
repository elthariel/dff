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

from binascii import *

from api.exceptions.libexceptions import *
from find_not_aligned_thread import PatternSearch

from PyQt4.QtGui import *
from PyQt4.QtCore import *

class Navigation(QWidget):
    def __init__(self, parent):
        super(Navigation,  self).__init__(parent)
        self.vbox = QVBoxLayout()
        self.hexedit = parent

        self.node = self.hexedit.node

        self.founded = []
        self.curFound = 0
        
        #PatternSearch
        self.ps = PatternSearch(self.node, self, None)
        
        self.initInformations()
        self.initNavigation()

        self.setLayout(self.vbox)

    #Informations: File size, current Offset, current block (n/n), 
    def initInformations(self):
        self.createLabelInformations()

    def updateInformations(self):
        self.hexedit.CurrentSector = self.hexedit.CurrentOffset / self.hexedit.sectorSize

        #Update Offset
        off = "Offset: "
        off += "%d" % self.hexedit.CurrentOffset
        self.offsetLabel.setText(off)
        
        #Update Blocks
        blocks = "Block: "
        toint = "%d"% self.hexedit.CurrentSector
        blocks += toint
        blocks += " / "
        blocks += "%d"% self.hexedit.sectors 
        self.blocksLabel.setText(blocks)

        labeltext = "Search: " #0 / 0"
        toint = "%d"% self.curFound
        labeltext += toint
        labeltext += " / "
        toint = "%d"% len(self.founded)
        labeltext += toint
        self.searchLabel.setText(labeltext)

    def initNavigation(self):
        self.nav = QHBoxLayout()
        self.nav.setSpacing(50)

        self.nav.setAlignment(Qt.AlignLeft)

        self.createGoto()
        self.createSearch()

        self.vbox.addLayout(self.nav)


    def updateNavigation(self):
        pass
        

    def initSearch(self):
        pass

    ################################################################

    def createLabelInformations(self):
        self.viewLabel = QHBoxLayout()
        self.viewLabel.setSpacing(50)

        self.viewLabel.setAlignment(Qt.AlignLeft)
        
        self.font = QFont()
        self.font.setBold(True)
        self.font.setPixelSize(12)

        self.createLabelOffset()
        self.createLabelBlock()

        self.createNavBlock()

        self.createLabelSize()
        self.createLabelSearch()
        self.createProgressBar()


        self.vbox.addLayout(self.viewLabel)

    def createLabelOffset(self):
        # Offset
        labeltext = "Offset: "
        toint = "%d"% self.hexedit.CurrentOffset
        labeltext += toint
        
        self.offsetLabel = QLabel(labeltext)
        self.offsetLabel.setFont(self.font)

        self.viewLabel.addWidget(self.offsetLabel)

    def createLabelBlock(self):
        #Block Label
        labeltext = "Block: "
        toint = "%d"% self.hexedit.CurrentSector
        labeltext += toint
        labeltext += " / "
        labeltext += "%d"% self.hexedit.sectors 

        self.blocksLabel = QLabel(labeltext)
        self.blocksLabel.setFont(self.font)
        
        self.viewLabel.addWidget(self.blocksLabel)


    def createLabelSize(self):
        # Dump Size
        labeltext = "Size: "
        toint = "%d"% self.hexedit.filesize
        labeltext += toint
        self.sizeLabel = QLabel(labeltext)
        self.sizeLabel.setFont(self.font)

        self.viewLabel.addWidget(self.sizeLabel)

    def createLabelSearch(self):
        #Search Label
        labeltext = "Search: 0 / 0"

        self.searchLabel = QLabel(labeltext)
        self.searchLabel.setFont(self.font)

        self.viewLabel.addWidget(self.searchLabel)

    def createProgressBar(self):
        self.progressBar = QProgressBar(self) #parent hex or nav?

        #Connect to PatternSearch
        self.connect(self.ps, SIGNAL("setValue ( int ) "), self.refreshProgress)
        self.connect(self.ps, SIGNAL("progressTerminated () "), self.endProgress)

        self.stopButton = QPushButton("Stop")
        self.stopButton.setFixedWidth(50)
        self.stopButton.connect(self.stopButton,  SIGNAL("clicked()"), self.stopSearch)

        self.viewLabel.addWidget(self.progressBar)
        
        self.viewLabel.addWidget(self.stopButton,  Qt.AlignRight)
        

    def createNavBlock(self):
        self.hboxarrow = QHBoxLayout()
        self.hboxarrow.setSpacing(10)
        self.hboxarrow.setAlignment(Qt.AlignLeft)

        self.prevButton = QToolButton()
        self.prevButton.setArrowType(Qt.LeftArrow)
        self.hboxarrow.addWidget(self.prevButton)
        
        self.prevButton.connect(self.prevButton,  SIGNAL("clicked()"), self.prev)

        self.nextButton = QToolButton()
        self.nextButton.setArrowType(Qt.RightArrow)
        
        self.hboxarrow.addWidget(self.nextButton)

        self.nextButton.connect(self.nextButton,  SIGNAL("clicked()"), self.next)
        self.viewLabel.addLayout(self.hboxarrow)


####################################################################################


    def createGoto(self):
        self.gotohbox = QHBoxLayout()
        self.gotohbox.setSpacing(5)
        self.gotohbox.setAlignment(Qt.AlignLeft)

        label = QLabel("Go to: ")
        self.gotohbox.addWidget(label)

        self.gotoEdit = QLineEdit()
        self.gotoEdit.setMinimumWidth(50)
        self.gotohbox.addWidget(self.gotoEdit, Qt.AlignRight)
                
        self.cbox = QComboBox()
        self.cbox.addItem("offset")
        self.cbox.addItem("block")
        self.gotohbox.addWidget(self.cbox)

        self.gotoButton = QPushButton("Go")

        self.gotoButton.setFixedWidth(50)

        self.gotoButton.connect(self.gotoButton,  SIGNAL("clicked()"), self.goto)
        self.gotohbox.addWidget(self.gotoButton,  Qt.AlignRight)
        
        self.nav.addLayout(self.gotohbox)
    
    def createSearch(self):
        self.hsearch = QHBoxLayout()
        self.hsearch.setSpacing(5)
        self.hsearch.setAlignment(Qt.AlignLeft)

        label = QLabel("Search: ")
        self.hsearch.addWidget(label)

        self.searchEdit = QLineEdit()
        self.searchEdit.setMinimumWidth(50)
        self.hsearch.addWidget(self.searchEdit, Qt.AlignRight)

        self.searchType = QComboBox()
        self.searchType.addItem("Ascii")
        self.searchType.addItem("Hexadecimal")
        self.hsearch.addWidget(self.searchType)

        self.searchButton = QPushButton("Search")

        self.searchButton.setFixedWidth(50)
        
        self.searchButton.connect(self.searchButton,  SIGNAL("clicked()"), self.search)
        self.hsearch.addWidget(self.searchButton,  Qt.AlignRight)

        #Result navigation
        
        self.prevSearchButton = QToolButton()
        self.prevSearchButton.setArrowType(Qt.LeftArrow)
        self.prevSearchButton.setDisabled(True)
        self.hsearch.addWidget(self.prevSearchButton)

        self.prevButton.connect(self.prevSearchButton,  SIGNAL("clicked()"), self.prevSearch)

        self.nextSearchButton = QToolButton()
        self.nextSearchButton.setArrowType(Qt.RightArrow)
        self.nextSearchButton.setDisabled(True)
        self.hsearch.addWidget(self.nextSearchButton)
        self.nextSearchButton.connect(self.nextSearchButton,  SIGNAL("clicked()"), self.nextSearch)

        self.nav.addLayout(self.hsearch)
        
    ##############################################################################
                                #  CallBacks  #
    #
    #Block Navigation
    #

    def stopSearch(self):
        print "nav stop"
        self.emit(SIGNAL("stopsearch()"))

    def refreshProgress(self, count):
        #print "refresh progress"
        self.progressBar.setValue(count)
        #self.hexedit.stateinfo = "Searching"

    def endProgress(self):
        self.founded = self.ps.getResults()

        if len(self.founded) > 0:
            blocks = "Search: 0 / "
            toint = "%d"% len(self.founded)
            blocks += toint
            self.searchLabel.setText(blocks)
            
                #Activate navigation arrows
            self.prevSearchButton.setDisabled(False)
            self.nextSearchButton.setDisabled(False)

    def prev(self):
        #Prev Block
        if (self.hexedit.CurrentOffset - self.hexedit.sectorSize) >= 0:
            self.hexedit.CurrentOffset -= self.hexedit.sectorSize
            self.hexedit.readSector()
            self.updateInformations()
        else:
            print "Begin Of File"

    def next(self):
        #Next Block
        if (self.hexedit.CurrentOffset  + self.hexedit.sectorSize) < self.hexedit.filesize:
            self.hexedit.CurrentOffset += self.hexedit.sectorSize
            self.hexedit.readSector()
            self.updateInformations()
        else:
            print "End Of File"

    #
    #Search Navigation
    #

    def prevSearch(self):
        #print self.curFound
        if self.curFound > 0:

            if self.curFound != 0:
                self.curFound -= 1

            self.hexedit.CurrentOffset = self.founded[self.curFound]

            self.readSearch(self.hexedit.CurrentOffset)

            self.updateInformations()
        else:
            print "Begin of search"
    

    def nextSearch(self):
        #print self.curFound
        if self.curFound < len(self.founded):
            if self.curFound != len(self.founded):
                self.curFound += 1

            self.hexedit.CurrentOffset = self.founded[self.curFound]

            self.readSearch(self.hexedit.CurrentOffset)

            self.updateInformations()
        else:
            print "End of search"


    def readSearch(self, offset):
        #seek
        try:
            self.hexedit.file.seek(offset)
            buffer = self.hexedit.file.read(self.hexedit.sectorSize)
            self.hexedit.refreshSectorShape(buffer, offset)
        except vfsError,  e:
            print "Read error"
    #
    #Go to
    #

    def goto(self):
        if not self.gotoEdit.text():
            print "Enter Value"
        else:
            #Get offset or block
            type = self.cbox.currentText()
            if type == "block":
                sec = self.gotoEdit.text()
                #print sec
                sector = int(sec)
                if sector < self.hexedit.sectors:
                    self.hexedit.CurrentOffset = sector * self.hexedit.sectorSize
                    self.hexedit.readSector()                
                    self.hexedit.navigation.updateInformations()
                else:
                    print "Invalid block"
            elif type == "offset":
                off = self.gotoEdit.text()
                offset = off.toInt(10)
                #print offset
                if offset[0] < self.hexedit.filesize:
                    self.hexedit.CurrentOffset = offset[0]
                    self.hexedit.readSector()
                    self.hexedit.navigation.updateInformations()
                else:
                    print "Invalid sector"

    def search(self):
        node = self.hexedit.file

        toSearch = str(self.searchEdit.text())

        self.founded = []
        self.curFound = 0

        if toSearch != "":
            #Get type
            type = self.searchType.currentText()

            if type == "Ascii":
                pattern = toSearch
            else:
                if len(toSearch) % 2 == 0:
                    pattern = unhexlify(toSearch)
                else:
                    print "Invalid hexadecimal size"
                    return

            
            self.ps.set("pattern", pattern)
            self.ps.start()
            
            #self.founded = self.ps.getResults()

         
                ##Search process
            #If founded
            if len(self.founded) > 0:
                #Refresh label
                #print len(self.founded)
                #self.curFound = 1
                blocks = "Search: 0 / "
                toint = "%d"% len(self.founded)
                blocks += toint
                self.searchLabel.setText(blocks)

                #Activate navigation arrows
                self.prevSearchButton.setDisabled(False)
                self.nextSearchButton.setDisabled(False)
        else:
            print "Fill search"

