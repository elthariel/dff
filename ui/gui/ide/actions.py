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

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from DFF_Ide import DFF_Ide

class ideActions():
    def __init__(self, mainwindow, ide = None):
        self.mainwindow = mainwindow
        self.ide = ide

        self.init()
        self.initMainActions()
        self.initIdeActions()

        self.initMainToolbar()
        self.initIdeToolbar()

        self.setMenu()

        self.initMainCallBacks()

        self.disableActions()

    def init(self):
        self.mainActs = []
        self.ideActs = []

    def initMainActions(self):
        self.maintoolbar = QToolBar()

        self.newact = QAction(QIcon(":script-new.png"),  "New Script",  self.maintoolbar)
        self.mainActs.append(self.newact)

        self.openact = QAction(QIcon(":script-open.png"),  "Open Script",  self.maintoolbar)
        self.mainActs.append(self.openact)

    def initIdeActions(self):
        self.idetoolbar = QToolBar()

        self.saveact = QAction(QIcon(":script-save.png"),  "Save Script",  self.idetoolbar)
        self.ideActs.append(self.saveact)
    
        self.saveasact = QAction(QIcon(":script-save-as.png"),  "Save Script as",  self.idetoolbar)
        self.ideActs.append(self.saveasact)
        
        self.runact = QAction(QIcon(":script-run.png"),  "Load script",  self.idetoolbar)
        self.ideActs.append(self.runact)
        
        self.undoact = QAction(QIcon(":undo.png"),  "Undo",  self.idetoolbar)
        self.ideActs.append(self.undoact)
        
        self.redoact = QAction(QIcon(":redo.png"),  "Redo",  self.idetoolbar)
        self.ideActs.append(self.redoact)

    def initMainToolbar(self):
        self.maintoolbar.addAction(self.newact)
        self.maintoolbar.addAction(self.openact)
    
    def initIdeToolbar(self):
        self.idetoolbar.addAction(self.saveact)
        self.idetoolbar.addAction(self.saveasact)
        self.idetoolbar.addAction(self.runact)
        self.idetoolbar.addAction(self.undoact)
        self.idetoolbar.addAction(self.redoact)


    def initMainCallBacks(self):
        self.newact.connect(self.newact,  SIGNAL("triggered()"), self.newScript)
        self.openact.connect(self.openact,  SIGNAL("triggered()"), self.openScript)

    def enableActions(self):
        self.newact.setEnabled(True)
        self.openact.setEnabled(True)

        self.saveact.setEnabled(True)
        self.saveasact.setEnabled(True)
        self.runact.setEnabled(True)
        self.undoact.setEnabled(True)
        self.redoact.setEnabled(True)

    def disableActions(self):
        self.newact.setEnabled(True)
        self.openact.setEnabled(True)

        self.saveact.setEnabled(False)
        self.saveasact.setEnabled(False)
        self.runact.setEnabled(False)
        self.undoact.setEnabled(False)
        self.redoact.setEnabled(False)

    # CALLBACKS

    def newScript(self):
        if not self.ide:
            self.ide = DFF_Ide(self.mainwindow, self)
            self.mainwindow.dockWidget["IDE"] = self.ide
            self.mainwindow.addNewDockWidgetTab(Qt.RightDockWidgetArea, self.ide)
        self.ide.ide.newactBack()
        
    def openScript(self):
        if not self.ide:
            self.ide = DFF_Ide(self.mainwindow, self)
            self.mainwindow.dockWidget["IDE"] = self.ide
            self.mainwindow.addNewDockWidgetTab(Qt.RightDockWidgetArea, self.ide)
        self.ide.ide.openactBack()


    def setMenu(self):
        self.menu = QMenu(self.mainwindow.menubar)
        self.menu.setObjectName("menuIde")
        self.menu.setTitle(QApplication.translate("MainWindow", "Ide", None, QApplication.UnicodeUTF8))

        self.menu.addAction(self.newact)
        self.menu.addAction(self.openact)
        
        self.menu.addSeparator()

        self.menu.addAction(self.saveact)
        self.menu.addAction(self.saveasact)
        self.menu.addAction(self.runact)

        self.menu.addSeparator()

        self.menu.addAction(self.undoact)
        self.menu.addAction(self.redoact)

        
