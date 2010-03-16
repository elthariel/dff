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

from PyQt4.QtCore import QString, Qt, SIGNAL, QLineF, QThread
from PyQt4.QtGui import QWidget, QVBoxLayout, QCheckBox, QGridLayout, QLabel, QLineEdit, QPushButton, QTabWidget, QComboBox, QTreeWidget, QTreeWidgetItem

from utils import *

import binascii

class search(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self)
        self.init(parent)
        self.initShape()

    def init(self, parent):
        self.heditor = parent
        #Open a new instance for I/O
        self.file = self.heditor.node.open()
        #Last search type tag [0:hex|1:characters]
        self.lastSearchType = 0
        #Init Thread
        self.search_th = searchThread(self.file)
        #tupple of searched patterns [key:hex(pattern)|value:offsetslist]
        self.searchedPatterns = {}
#        print self.searchThread
        self.connect(self.search_th, SIGNAL("searchDone()"), self.searchdone)

    def initShape(self):
        self.vbox = QVBoxLayout()
        self.createValues()
        self.createOptions()
        self.createResults()
        self.createSearching()
        self.createButtons()
        #fill
        fill = QWidget()
        self.vbox.addWidget(fill)

        self.setLayout(self.vbox)

    def createValues(self):
        self.wvalues = QWidget()
        self.valuesgrid = QGridLayout()

        ltype = QLabel("Type:")
        self.type = QComboBox()
        self.type.addItem("Hexadecimal")
        self.type.addItem("Character(s)")

        lneedle = QLabel("Pattern:")
        self.needle = QLineEdit()

        lwild = QLabel("Wildcard:")
        self.wildcard = QLineEdit()

        lstart = QLabel("Start: ")
        self.start = QFFSpinBox(self)
        self.start.setMaximum(self.heditor.filesize)
        self.start.setValue(0)

        self.valuesgrid.addWidget(ltype, 0, 0)
        self.valuesgrid.addWidget(self.type, 0, 1)

        self.valuesgrid.addWidget(lneedle, 1, 0)        
        self.valuesgrid.addWidget(self.needle, 1, 1)

        self.valuesgrid.addWidget(lwild, 2, 0)        
        self.valuesgrid.addWidget(self.wildcard, 2, 1)

        self.valuesgrid.addWidget(lstart, 3, 0)        
        self.valuesgrid.addWidget(self.start, 3, 1)
        
        self.wvalues.setLayout(self.valuesgrid)
        self.vbox.addWidget(self.wvalues)

    def createOptions(self):
        self.woptions = QWidget()
        self.optgrid= QGridLayout()

        lopt = QLabel("Options:")

        self.fromcursor = QCheckBox("From cursor")
        self.back = QCheckBox("Backwards")

        self.optgrid.addWidget(lopt, 0, 0)
        self.optgrid.addWidget(self.fromcursor, 0, 1)
#        self.optgrid.addWidget(self.back, 2, 0)

        self.woptions.setLayout(self.optgrid)
        self.vbox.addWidget(self.woptions)

    def createResults(self):
        self.wresults = QWidget()
        self.resgrid= QGridLayout()

#        lres = QLabel("Results")
        self.resultab = resultab(self)

#        self.resgrid.addWidget(lres, 0, 0)
        self.resgrid.addWidget(self.resultab, 0, 0)

        self.wresults.setLayout(self.resgrid)
        self.vbox.addWidget(self.wresults)

    def createSearching(self):
        self.wsing = QWidget()
        self.singgrid= QGridLayout()

        self.searchlabel = QLabel("Please launch search")
        self.singgrid.addWidget(self.searchlabel, 0, 0)

        self.wsing.setLayout(self.singgrid)
        self.vbox.addWidget(self.wsing)
        
    def createButtons(self):
        self.applyB = QPushButton("Apply")
        self.connect(self.applyB, SIGNAL('clicked()'), self.searchit)

        self.vbox.addWidget(self.applyB)


    def toHex(self, str, wildcard = None):
        HEXCHAR = "0123456789abcdefABCDEF"
        hexStr = ""
        evenhex = ""
        for i in range(len(str)):
            if str[i] in HEXCHAR:
                if len(evenhex) == 1:
                    hexStr += chr(int(evenhex+str[i], 16))
                    evenhex = ""
                else:
                    evenhex = str[i]
            elif wildcard != None and str[i] == wildcard:
                if evenhex == "":
                    hexStr += wildcard
                else:
                    raise ValueError, "argument 'str' must be an even number of char"
            else:
                raise ValueError, "argument 'str' contains not valid characters"
        if len(evenhex) != 0:
            raise ValueError, "argument 'str' must be an even number of char"
        return hexStr

#####################
#     Search IT     #
#####################

    def searchit(self):
        if self.needle.text() != "":
            needle = self.needle.text()
            #check needle
            type = self.type.currentText()
            if type == "Hexadecimal":
                self.lastSearchType = 0
                try:
                    pattern = self.toHex(str(needle))
                except ValueError:
                    print "Wrong Hex pattern"
            else:
                self.lastSearchType = 1
                pattern = str(needle)
            opt_fromcursor = self.fromcursor.isChecked()
            spinstart = self.start.value()
            wild = self.wildcard.text()
#            opt_back = self.back.isTristate()
            #From cursor
            if opt_fromcursor:
                start = self.heditor.currentSelection
            elif spinstart > 0:
                start = spinstart
            else:
                start = 0
            print start
            self.search_th.setData(pattern, start, wild)
            self.searchlabel.setText("Searching ...")

            self.search_th.start()

#            res = self.file.search(pattern, len(pattern), None, start)            
                     
    def searchdone(self):
#            print "Results found: ", nres
        res = self.search_th.getResults()
        label = "%2.d" % len(res)
        label += " matchs"
        self.searchlabel.setText(label)

        self.resultab.addResults(res)

class searchThread(QThread):
    def __init__(self, file):
        QThread.__init__(self)
        self.file = file
        self.pattern = ""
        self.wild = ""

    def run(self):
        if self.wild == "":
            wild = None
        else:
            wild = self.wild

        self.res = self.file.search(self.pattern, len(self.pattern), wild, self.startOffset)
        self.emit(SIGNAL("searchDone()"))

    def setData(self, pattern, startOffset, wild):
        self.pattern = pattern
        self.startOffset = startOffset
        self.wild = wild

    def getResults(self):
        return self.res

class resultab(QTabWidget):
    def __init__(self, parent):
        QTabWidget.__init__(self)
        self.init(parent)
        self.initShape()

    def init(self, parent):
        self.search = parent
        self.heditor = parent.heditor
        self.trees = []

    def initShape(self):
        self.setTabPosition(QTabWidget.North)
#    def formatHighlightPattern(self, pattern):
#        res = QString("\\b(")
#        count = 0
#        for p in pattern:
#            print "add Byte"
#            res.append(binascii.hexlify(p))
#            count += 1
#            if count == self.heditor.groupBytes:
#                print "add blank"
#                res.append(" ")
#                count = 0
#        res.append(")\\b")
#        print "   formater highlight:", res
#        return res

    def addResults(self, results):
        tree = QTreeWidget()
        tree.setColumnCount(1)
        header = QString("Offset")
        tree.setHeaderLabel(header)
        tree.setAlternatingRowColors(True)
        
        self.connect(tree, SIGNAL("itemDoubleClicked(QTreeWidgetItem *, int)"), self.treeClicked)

        for res in results:
#            print hex(res)
            item = QTreeWidgetItem(tree)
            off = "0x"
            off += "%.2x" % res
            item.setText(0, str(off))
        self.trees.append(tree)

        #Add pattern and offsets to tupple
        key = binascii.hexlify(self.search.search_th.pattern)
#        print "key: ", key
        self.search.searchedPatterns[key] = results

        if self.search.lastSearchType == 0:
            p = binascii.hexlify(self.search.search_th.pattern)
        else:
            p = self.search.search_th.pattern

        #Add Ascii hex pattern in searched list for syntaxHighliter
        self.insertTab(len(self.trees), tree, p)

        #resuts: list of offset
    def treeClicked(self, item, column):
        coffset =  item.text(column)
        coffset.remove(0, 2)
#        print coffset
        off = coffset.toULongLong(16)
        if off[1]:
            offset = off[0]
#        print offset
            self.search.heditor.readOffset(offset)
            value = self.search.heditor.whex.offsetToValue(offset)
            self.search.heditor.whex.scroll.setValue(value)
            #Update
            self.heditor.selection.offset = offset
            self.heditor.whex.hexcursor.update()
            self.heditor.whex.asciicursor.update()
            self.heditor.infos.update()
            
        
        
