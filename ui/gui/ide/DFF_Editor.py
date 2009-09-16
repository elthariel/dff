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

from PyQt4.QtCore import *
from PyQt4.Qsci import *

#TODO

class   Editor(QsciScintilla):
    def __init__(self,parent):
        QsciScintilla.__init__(self, parent)
        self.setOptions()
        self.initCallBacks()
        self.scriptPath = QString("")
        self.name = QString("")
        
    def insertBuffer(self,  buffer):
        self.insert(buffer)
        
    def initCallBacks(self):
        self.connect(self, SIGNAL("SCN_CHARADDED(int)"), self.__charAdded)
        self.connect(self, SIGNAL('cursorPositionChanged(int,int)'), self.__cursorPositionChanged)
        
    def createMargins(self):
        self.setMarginLineNumbers(1,  True)
        self.setMarginWidth(1, 30)
        self.setMarginLineNumbers(2,  False)
        self.setMarginWidth(2, 10)
        #self.setMarginColor(2)
        
    def setIndentationOptions(self):
        self.setAutoIndent(1)
        self.setIndentationGuides(1)
        self.setIndentationsUseTabs(0)
        self.setAutoCompletionThreshold(2)
        self.setTabIndents(True)
        self.setBackspaceUnindents(True)
        self.setIndentationWidth(4)
        
    def setLexerPython(self):
        self.lexpyth = QsciLexerPython()
        self.setLexer(self.lexpyth)
        
    def setOptions(self):
        self.setUtf8(1)
        self.createMargins()
        self.setIndentationOptions()
        self.setLexerPython()
    
    def setAutoCompletion(self):
        self.setAutoCompletionSource(AcsDocument)
    
    #return true / false
    def checkError(scriptBuffer):
        return false
    
    def setScriptPath(self,  path):
        self.scriptPath = path
        
    def getScriptPath(self):
        if self.scriptPath:
            return self.scriptPath
        else:
            return "error"
            
    def setName(self,  name):
        self.name = name
        
    def getName(self):
        if self.name:
            return self.name
        else:
            return "error"
        
    def __charAdded(self, charadded):
        #print "char added",  charadded
        #Transform to char
#        char added 40 = (
#        char added 41 = )
#        char added 58 = :
#        char added 34 = "
#        char added 46 = .
        char = "%c" % charadded
        toAdd = QString()
        if char == "(":
            toAdd.append(")")
            self.insert(toAdd)
        
    def __cursorPositionChanged(self,  line,  pos):
        pass
        #print "Position changeddd",  line , "Pos ",  pos
