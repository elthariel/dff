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
#  Frederic B. <fba@digital-forensic.org>

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from typeSelection import *

import string

import time

class userPattern(QGroupBox):
    def __init__(self):
        QGroupBox.__init__(self, "User defined patterns")
        self.setCheckable(True)
        self.setChecked(False)
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.patternArea()
        self.patternTable()

    def createPattern(self, name, x):
        label = name.lower() + "Label"
        type = name.lower() + "Type"
        entry = name.lower() + "Entry"
        setattr(self, label, QLabel(name))
        setattr(self, entry, QLineEdit())
        setattr(self, type, QComboBox())
        labelobj = getattr(self, label)
        typeobj = getattr(self, type)
        entryobj = getattr(self, entry)
        typeobj.addItem("Hexadecimal")
        typeobj.addItem("String")
        self.grid.addWidget(labelobj, x, 0)
        self.grid.addWidget(entryobj, x, 1)
        self.grid.addWidget(typeobj, x, 2)


    def patternArea(self):
        self.wildcardLabel = QLabel("Wilcard")
        self.wildcard = QLineEdit()
        self.wildcard.setMaxLength(1)
        self.filetypeLabel = QLabel("File type")
        self.filetype = QLineEdit()
        self.windowLabel = QLabel("Window size")
        self.window = QSpinBox()
        self.window.setSuffix(" bytes")
        self.window.setRange(0, 2500000)
        self.window.setSingleStep(100)
        self.addEntry = QPushButton("add")
        self.connect(self.addEntry, SIGNAL("clicked()"), self.insertPattern)
        self.grid.addWidget(self.filetypeLabel, 0, 0)
        self.grid.addWidget(self.filetype, 0, 1, 1, 2)
        self.grid.addWidget(self.wildcardLabel, 1, 0)
        self.grid.addWidget(self.wildcard, 1, 1, 1, 2)
        self.createPattern("Header", 2)
        self.createPattern("Footer", 3)
        self.grid.addWidget(self.windowLabel, 4, 0)
        self.grid.addWidget(self.window, 4, 1)
        self.grid.addWidget(self.addEntry, 5, 1)

    def patternTable(self):
        self.patterns = QTableWidget()
        self.patterns.setShowGrid(False)
        self.patterns.setColumnCount(5)
        self.patterns.setHorizontalHeaderLabels(["Filetype", "Wildcard", "Header", "Footer", "Window"])
        self.patterns.horizontalHeader().setStretchLastSection(True)
        self.connect(self.patterns.verticalHeader(), SIGNAL("sectionClicked(int)"), self.patterns.removeRow)
        self.grid.addWidget(self.patterns, 6, 0, 1, 3)
        

    def warning(self, msg):
        msgBox = QMessageBox()
        msgBox.setText(msg)
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.exec_()

    def validate(self, **kwargs):
        msg = ""

        if len(kwargs["type"]) == 0:
            msg = "Type must be defined"
        else:
            for i in kwargs["type"]:
                if i not in string.letters:
                    msg = "Type's characters must be in the following set\n\n" + string.letters
                    break
        if msg != "":
            self.warning(msg)
            return False

        if kwargs["headerType"] == "Hexadecimal" and not self.isHex(kwargs["header"], kwargs["wildcard"]):
            msg = "Header must be an even number of chars (wildcard included)"
            self.warning(msg)
            return False
        
        if len(kwargs["header"]) == 0:
            msg = "Header must be provided"
            self.warning(msg)
            return False

        if kwargs["footerType"] == "Hexadecimal" and not self.isHex(kwargs["header"], kwargs["wildcard"]):
            msg = "Footer must be an even number of chars (wildcard included)"
            self.warning(msg)
            return False

        if kwargs["window"] <= 0:
            msg = "Window size must be greater than 0"
            self.warning(msg)
            return False

        return True


    def insertPattern(self):
        filetype = str(self.filetype.text())
        wildcard = str(self.wildcard.text())
        header = str(self.headerEntry.text())
        headerType = str(self.headerType.currentText())
        footer = str(self.footerEntry.text())
        footerType = str(self.footerType.currentText())
        window = self.window.text()

        #Validate most of provided items
        kwargs = {"type": filetype, "header": header, "headerType": headerType, 
                  "footer": footer, "footerType": footerType, "wildcard": wildcard,
                  "window": int(window.replace(" bytes", ""))}
        if not self.validate(**kwargs):
            return

        filetypeItem = QTableWidgetItem(filetype)
        wildcardItem = QTableWidgetItem(wildcard)
        headerItem = QTableWidgetItem(header + " (" + headerType[0:3] + ")")
        footerItem = QTableWidgetItem(footer + " (" + footerType[0:3] + ")")
        windowItem = QTableWidgetItem(window)
        self.patterns.insertRow(self.patterns.rowCount())
        vertHeader = QTableWidgetItem(QIcon(":closetab.png"), "")
        row = self.patterns.rowCount() - 1
        self.patterns.setVerticalHeaderItem(row, vertHeader)
        self.patterns.setItem(row, 0, filetypeItem)
        self.patterns.setItem(row, 1, wildcardItem)
        self.patterns.setItem(row, 2, headerItem)
        self.patterns.setItem(row, 3, footerItem)
        self.patterns.setItem(row, 4, windowItem)
        self.patterns.resizeRowToContents(row)

        
    def isHex(self, str, wildcard):
        HEXCHAR = "0123456789abcdefABCDEF"
        hexStr = ""
        even = False
        for i in range(len(str)):
            if str[i] in HEXCHAR:
                if even == True:
                    even = False
                else:
                    even = True
            elif wildcard != None and str[i] == wildcard:
                if even:
                    return False
            else:
                return False
        if even:
            return False
        return True
    

    def toHex(self, str, wildcard):
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


    def textToPattern(self, text, wildcard):
        idx = text.find("(")
        pattern = ""
        if idx != -1:
            type = text[idx+1:idx+4]
            pattern = text[0:idx-1]
            if type == "Hex":
                pattern = self.toHex(pattern, wildcard)
        return pattern

    def itemToFileDescr(self, row):
        fd = file_description()
        fd.type = str(self.patterns.item(row, 0).text())
        fd.wildcard = str(self.patterns.item(row, 1).text())
        header = self.textToPattern(str(self.patterns.item(row, 2).text()), fd.wildcard)
        fd.header = header
        fd.header_size = len(header)
        footer = self.textToPattern(str(self.patterns.item(row, 3).text()), fd.wildcard)
        fd.footer = footer
        fd.footer_size = len(footer)
        fd.window = int(self.patterns.item(row, 4).text().replace(" bytes", ""))
        return fd

    def getChecked(self):
        entries = []
        if self.isChecked():
            rowCount = self.patterns.rowCount()
            for row in range(0, rowCount):
                entries.append(self.itemToFileDescr(row))
        return entries

