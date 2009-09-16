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
from PyQt4.QtGui import *

from DFF_Ide import DFF_Ide

class DFF_ToolBar_Ide(QToolBar):
    def __init__(self,  parent,  ide = None):
        super(DFF_ToolBar_Ide,  self).__init__(parent)
        self.ide = ide
        self.mainWindow = parent
        self.g_display()
        self.initCallback()
        self.initCallbackOptional()
        
    def g_display(self):
        self.newact = QAction(QIcon(":script-new.png"),  "New",  self)
        self.addAction(self.newact)
        
        self.openact = QAction(QIcon(":script-open.png"),  "Open",  self)
        self.addAction(self.openact)
        
        self.saveact = QAction(QIcon(":script-save.png"),  "Save",  self)
        self.addAction(self.saveact)
    
        self.saveasact = QAction(QIcon(":script-save-as.png"),  "Save as",  self)
        self.addAction(self.saveasact)
        
        self.runact = QAction(QIcon(":script-run.png"),  "Load script",  self)
        self.addAction(self.runact)
        
        self.undoact = QAction(QIcon(":script-undo.png"),  "Undo",  self)
        self.addAction(self.undoact)
        
        self.redoact = QAction(QIcon(":script-redo.png"),  "Redo",  self)
        self.addAction(self.redoact)
        
    def initCallback(self):
        self.newact.connect(self.newact,  SIGNAL("triggered()"), self.newScript)
        self.openact.connect(self.openact,  SIGNAL("triggered()"), self.openScript)
        
    def initCallbackOptional(self):
        if self.ide:
            self.saveact.setEnabled(True)
            self.saveasact.setEnabled(True)
            self.runact.setEnabled(True)
            self.undoact.setEnabled(True)
            self.redoact.setEnabled(True)
            
            self.saveact.connect(self.saveact,  SIGNAL("triggered()"), self.ide.ide.saveactBack)
            self.saveasact.connect(self.saveasact,  SIGNAL("triggered()"), self.ide.ide.saveasactBack)
            self.runact.connect(self.runact,  SIGNAL("triggered()"), self.ide.ide.runactBack)
            self.undoact.connect(self.undoact,  SIGNAL("triggered()"), self.ide.ide.undoactBack)
            self.redoact.connect(self.redoact,  SIGNAL("triggered()"), self.ide.ide.redoactBack)
        else:
            self.saveact.setEnabled(False)
            self.saveasact.setEnabled(False)
            self.runact.setEnabled(False)
            self.undoact.setEnabled(False)
            self.redoact.setEnabled(False)
            
            
    def newScript(self):
        if not self.ide:
            self.ide =DFF_Ide(self.mainWindow)
            self.initCallbackOptional()
            self.mainWindow.addNewDockWidgetTab(Qt.RightDockWidgetArea, self.ide)
        self.ide.ide.newactBack()
        #self.mainWindow.QTabCentralWidget.selectTypeWidget("ide")
        
    def openScript(self):
        if not self.ide:
            self.ide =DFF_Ide(self.mainWindow)
            self.initCallbackOptional()
            self.mainWindow.addNewDockWidgetTab(Qt.RightDockWidgetArea, self.ide)
        self.ide.ide.openactBack()
        #self.mainWindow.QTabCentralWidget.selectTypeWidget("ide")
