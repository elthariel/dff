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

from PyQt4.QtGui import QWidget, QTextTable,  QTextEdit, QTextDocument,  QTextCursor,  QTextTableFormat,  QGridLayout,  QLayout

class TextTable(QLayout):
    def __init__(self,  mainWindow,  parent):
        super(TextTable,  self).__init__(parent)
        
        self.Grid = QGridLayout()
        
        #Create Document
        self.Document = QTextDocument(self)
        self.TFormat = QTextTableFormat()
        
        self.CreateShape()
        
    def CreateShape(self):
        self.CreateOffset()
        self.CreateHex()
        self.CreateAscii()
        
    def CreateOffset(self):
        #TextEdit
        self.Offset = QTextEdit("")
        self.Offset.setReadOnly(True)
        self.Offset.setDocument(self.Document)
        
        self.Grid.addWidget(self.Offset, 0, 0, 0)
        
        #Cursor
        self.OffCursor = QTextCursor(self.OffDocument)
        self.OffCursor.movePosition(QTextCursor.Start)
        self.TOffset = self.OffCursor.insertTable(1,  1, self.TFormat)
        
        
    
    def CreateHex(self):
        #TextEdit
        self.Hex = QTextEdit("")
        self.Hex.setReadOnly(True)
        self.Hex.setDocument(self.Document)
        
        self.Grid.addWidget(self.Hex, 0, 1, 0)
        
        #Cursor
        self.HexCursor = QTextCursor(self.Document)
        self.HexCursor.movePosition(QTextCursor.Start)
        self.THex = self.HexCursor.insertTable(1,  16, self.TFormat)
        
    
    def CreateAscii(self):
        #TextEdit
        self.Ascii = QTextEdit("")
        self.Ascii.setReadOnly(True)
        self.Ascii.setDocument(self.Document)
        
        self.Grid.addWidget(self.Ascii, 0, 2, 0)
        
        #Cursor
        self.TAscii = self.AsciiCursor.insertTable(1,  16, self.TFormat)
        self.AsciiCursor.movePosition(QTextCursor.Start)
        self.AsciiCursor = QTextCursor(self.Document)
        
    
    def FillOffset(self):
        pass
        
