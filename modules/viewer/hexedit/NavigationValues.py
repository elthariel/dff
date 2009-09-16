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

import struct
import binascii

from api.exceptions.libexceptions import *

from PyQt4.QtGui import *
from PyQt4.QtCore import *

class NavigationValues(QWidget):
    def __init__(self,  parent):
        QWidget.__init__(self)
        self.hexedit = parent

        self.grid = QGridLayout()
        self.createInformations()
        
        self.setLayout(self.grid)
        
    def createInformations(self):
        self.create8bits()
        self.create16bits()
        self.create32bits()
        self.createBinOctal()

        
    def create8bits(self):
        #Signed Char
        char = self.readConvers(1)
        
        charlabel = QLabel("Signed 8 bit")
        self.grid.addWidget(charlabel, 0, 0)
        
        self.editCharSigned = QLineEdit()
        
        #DO Unpack 
        bchar = struct.unpack('b',  char)
        charedit = "%.0d" % bchar
        self.editCharSigned.insert(charedit)
        self.editCharSigned.setReadOnly(True)

        self.grid.addWidget(self.editCharSigned, 0, 1)

        charlabel = QLabel("Unsigned 8 bit")
        self.grid.addWidget(charlabel, 0, 2)
        #self.hcharusigned.addWidget(charlabel)
        
        self.edituCharSigned = QLineEdit()
        #DO Unpack 
        bchar = struct.unpack('B',  char)
        charedit = "0x"
        charedit += "%.0X" % bchar
        self.edituCharSigned.insert(charedit)
        self.edituCharSigned.setReadOnly(True)
        self.grid.addWidget(self.edituCharSigned, 0, 3)

        #Binary and octal values
        self.binary = self.byte_to_bits_string(bchar[0])
        self.octal = "%.2X" % bchar[0 ]
        

    def create16bits(self):
        #Signed Char
        short = self.readConvers(2)

        #self.hboxshort = QHBoxLayout()
        #self.hshortsigned = QHBoxLayout()
        shortlabel = QLabel("Signed 16 bit")
        self.grid.addWidget(shortlabel, 0, 4)
        #self.hshortsigned.addWidget(shortlabel)
        

        self.editShortSigned = QLineEdit()
        #self.editShortSigned.setFixedSize(QSize(100,  25))
        
        #DO Unpack 
        bshort = struct.unpack('h',  short)
        shortedit = "%.0d" % bshort
        self.editShortSigned.insert(shortedit)
        self.editShortSigned.setReadOnly(True)
        self.grid.addWidget(self.editShortSigned, 0, 5)
        #self.hshortsigned.addWidget(self.editShortSigned)
        
        #self.vbox.addLayout(self.hshortsigned)
        #self.hboxshort.addLayout(self.hshortsigned)
        
        #UnSigned Char
        #self.hshortusigned = QHBoxLayout()
        shortlabel = QLabel("Unsigned 16 bit")
        self.grid.addWidget(shortlabel, 0, 6)

#self.hshortusigned.addWidget(shortlabel)
        self.edituShortSigned = QLineEdit()
        #self.edituShortSigned.setFixedSize(QSize(100,  25))
        
        #DO Unpack 
        bshort = struct.unpack('H',  short)
        shortedit = "0x"
        shortedit += "%.0X" % bshort
        self.edituShortSigned.insert(shortedit)
        self.edituShortSigned.setReadOnly(True)
        self.grid.addWidget(self.edituShortSigned, 0, 7)
        #self.hshortusigned.addWidget(self.edituShortSigned)
        
        #self.vbox.addLayout(self.hshortusigned)
        #self.hboxshort.addLayout(self.hshortusigned)
        #self.vbox.addLayout(self.hboxshort)


    def create32bits(self):
        #Signed Char
        int = self.readConvers(4)

        #self.hboxint = QHBoxLayout()
        #self.hintsigned = QHBoxLayout()
        intlabel = QLabel("Signed 32 bit")
        self.grid.addWidget(intlabel, 1, 0)
        #self.hintsigned.addWidget(intlabel)
        

        self.editIntSigned = QLineEdit()
        #self.editIntSigned.setFixedSize(QSize(100,  25))
        
        #DO Unpack 
        bint = struct.unpack('i',  int)
        intedit = "%.0d" % bint
        self.editIntSigned.insert(intedit)
        self.editIntSigned.setReadOnly(True)
        self.grid.addWidget(self.editIntSigned, 1, 1)
        #self.hintsigned.addWidget(self.editIntSigned)
        
        #self.vbox.addLayout(self.hintsigned)
        #self.hboxint.addLayout(self.hintsigned)
        
        #UnSigned Int
        #self.hintusigned = QHBoxLayout()
        intlabel = QLabel("Unsigned 32 bit")
        self.grid.addWidget(intlabel, 1, 2)
        #self.hintusigned.addWidget(intlabel)
        self.edituIntSigned = QLineEdit()
        #self.edituIntSigned.setFixedSize(QSize(100,  25))
        
        #DO Unpack 
        bint = struct.unpack('I',  int)
        intedit = "0x"
        intedit += "%.0X" % bint
        self.edituIntSigned.insert(intedit)
        self.edituIntSigned.setReadOnly(True)
        self.grid.addWidget(self.edituIntSigned, 1, 3)
        #self.hintusigned.addWidget(self.edituIntSigned)
        
        #self.vbox.addLayout(self.hintusigned)
        #self.hboxint.addLayout(self.hintusigned)
        #self.vbox.addLayout(self.hboxint)

    def createBinOctal(self):
        char = self.readConvers(1)
        #self.hbinoct = QHBoxLayout()
        
        #self.hbin = QHBoxLayout()
        label = QLabel("Binary")
        self.grid.addWidget(label, 1, 4)
        #self.hbin.addWidget(label)
        self.editBinary = QLineEdit()
        #self.editBinary.setFixedSize(QSize(100,  25))
        self.editBinary.insert(self.binary)
        self.editBinary.setReadOnly(True)
        self.grid.addWidget(self.editBinary, 1, 5)
        #self.hbin.addWidget(self.editBinary)
        
        #self.vbox.addLayout(self.hbin)
        #self.hbinoct.addLayout(self.hbin)
        
        #self.hoct = QHBoxLayout()
        label = QLabel("Hexadecimal")
        self.grid.addWidget(label, 1, 6)
        #self.hoct.addWidget(label)
        self.editOctal = QLineEdit()
        #self.editOctal.setFixedSize(QSize(100,  25))
        self.editOctal.insert(self.octal)
        self.editOctal.setReadOnly(True)
        self.grid.addWidget(self.editOctal, 1, 7)
        #self.hoct.addWidget(self.editOctal)
        
        #self.vbox.addLayout(self.hoct)
        #self.hbinoct.addLayout(self.hoct)
        #self.vbox.addLayout(self.hbinoct)


    def byte_to_bits_string(self, x):
      return "".join(map(lambda y:str((x>>y)&1), range(7, -1, -1)))

    #Return buffer with read size
    
    def update(self):
        char = self.readConvers(1)
        short = self.readConvers(2)
        int = self.readConvers(4)
        
        bint = struct.unpack('i',  int)
        intedit = "%.0d" % bint
        self.editIntSigned.clear()
        self.editIntSigned.insert(intedit)
        bint = struct.unpack('I',  int)
        intedit = "0x"
        intedit += "%.0X" % bint
        self.edituIntSigned.clear()
        self.edituIntSigned.insert(intedit)
        
        bshort = struct.unpack('h',  short)
        shortedit = "%.0d" % bshort
        self.editShortSigned.clear()
        self.editShortSigned.insert(shortedit)
        bshort = struct.unpack('H',  short)
        shortedit = "0x"
        shortedit += "%.0X" % bshort
        self.edituShortSigned.clear()
        self.edituShortSigned.insert(shortedit)
        
        bchar = struct.unpack('b',  char)
        charedit = "%.0d" % bchar
        self.editCharSigned.clear()
        self.editCharSigned.insert(charedit)
        bchar = struct.unpack('B', char)
        charedit = "0x"
        charedit += "%.0X" % bchar
        self.edituCharSigned.clear()
        self.edituCharSigned.insert(charedit)
        
        self.binary = self.byte_to_bits_string(bchar[0])
        self.octal = "%.2X" % bchar[0 ]
        self.editBinary.clear()
        self.editBinary.insert(self.binary)
        self.editOctal.clear()
        self.editOctal.insert(self.octal)
        
    

    def readConvers(self,  size):
        try:
            self.hexedit.file.seek(self.hexedit.CurrentOffset)
            buff = self.hexedit.file.read(size)
            return buff
        except vfsError,  e:
            print "error Conversion read"
