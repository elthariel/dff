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

from PyQt4 import QtCore
from PyQt4.QtGui import QAction, QApplication, QDockWidget, QWidget, QVBoxLayout, QIcon
from PyQt4.QtCore import QSize, Qt, SIGNAL
from Ide import Ide

class DFF_Ide(QDockWidget):
    def __init__(self,  mainWindow, actions):
        super(DFF_Ide,  self).__init__(mainWindow)
        self.init(mainWindow, actions)
        self.initCallbacks()
        self.g_display()

        self.show()
        
    def init(self, mainWindow, actions):
        self.type = "ide"
        self.name = "ide"
        self.setMaximumSize(QSize(3000, 3000))
        self.actions = actions
        self.__mainWindow = mainWindow

        self.configure()

    def configure(self):
        self.setAllowedAreas(Qt.AllDockWidgetAreas)
        self.setObjectName("IDE")
        self.setWindowTitle(QApplication.translate("IDE", "IDE", None, QApplication.UnicodeUTF8))

    def g_display(self):
        self.ide = Ide(self)
        self.ide.g_display()    
        self.setWidget(self.ide)

    def initCallbacks(self):
        self.connect(self, SIGNAL("visibilityChanged(bool)"), self.visibility)

    def closeEvent(self, cEvent):
        self.actions.disableActions()
        self.actions.idetoolbar.setVisible(False)
        cEvent.accept()

    def visibility(self, bool):
        if bool == False:
            self.actions.disableActions()
            self.actions.idetoolbar.setVisible(False)
        else:
            self.actions.enableActions()
            self.actions.idetoolbar.setVisible(True)
                
    def getParent(self):
        return self.__mainWindow
