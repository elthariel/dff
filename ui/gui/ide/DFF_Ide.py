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

from PyQt4 import QtCore
from PyQt4.QtGui import QAction, QApplication, QDockWidget, QWidget, QVBoxLayout, QIcon
from PyQt4.QtCore import QSize, Qt, SIGNAL
from Ide import Ide

class DFF_Ide(QDockWidget):
    def __init__(self,  mainWindow):
        super(DFF_Ide,  self).__init__(mainWindow)
        self.type = "ide"
        self.icon = QIcon(":gnome-run.png")
        self.name = "ide"
        self.__mainWindow = mainWindow
        self.addAction(mainWindow)
        self.g_display()
        self.configure()
        self.setMaximumSize(QSize(3000, 3000))
        
    def configure(self):
        self.setAllowedAreas(Qt.AllDockWidgetAreas)
        self.setObjectName("IDE")
        self.setWindowTitle(QApplication.translate("IDE", "IDE", None, QApplication.UnicodeUTF8))

    def addAction(self, mainWindow):
        self.__action = QAction(self)
        self.__action.setCheckable(True)
        self.__action.setChecked(True)
        self.__action.setObjectName("actionCoreInformations")
        self.__action.setText(QApplication.translate("MainWindow", "List Files", None, QApplication.UnicodeUTF8))
        mainWindow.menuWindowMenuList.addAction(self.__action)
        self.connect(self.__action,  SIGNAL("triggered()"),  self.changeVisibleInformations)
    
    def changeVisibleInformations(self):
        if not self.isVisible() :
            self.setVisible(True)
            self.__action.setChecked(True)
        else :
            self.setVisible(False)
            self.__action.setChecked(False)            
        
    def g_display(self):
        self.ide = Ide(self)
        self.ide.g_display()
    
        self.setWidget(self.ide)
    

    def getParent(self):
        return self.__mainWindow
