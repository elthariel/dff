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
#  Francois Percot <percot@gmail.com>
# 

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QApplication, QIcon, QMenu, QWidget
from PyQt4.QtCore import QSize

from utils.menu import MenuTags
    
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.ApplicationModal)
        MainWindow.resize(QtCore.QSize(QtCore.QRect(0,0,1014,693).size()).expandedTo(MainWindow.minimumSizeHint()))
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Digital Forensic Framework ", None, QtGui.QApplication.UnicodeUTF8))
        
        font = QtGui.QFont()
        font.setFamily("Metal")
        font.setWeight(70)
        font.setBold(False)
        MainWindow.setFont(font)
        MainWindow.setAnimated(True)
        MainWindow.setDockNestingEnabled(True)
        #MainWindow.setDockOptions(QtGui.QMainWindow.AllowNestedDocks|QtGui.QMainWindow.AllowTabbedDocks|QtGui.QMainWindow.AnimatedDocks|QtGui.QMainWindow.VerticalTabs)
        MainWindow.setDockOptions(QtGui.QMainWindow.AllowNestedDocks|QtGui.QMainWindow.AllowTabbedDocks|QtGui.QMainWindow.AnimatedDocks)
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0,0,1014,32))
        self.menubar.setDefaultUp(False)
        self.menubar.setObjectName("menubar")

        # MENU FILE
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuFile.setTitle(QtGui.QApplication.translate("MainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))

        # MENU EDIT
        #self.menuEdit = QtGui.QMenu(self.menubar)
        #self.menuEdit.setObjectName("menuEdit")
        #self.menuEdit.setTitle(QtGui.QApplication.translate("MainWindow", "Edit", None, QtGui.QApplication.UnicodeUTF8))
    
        # MENU MODULES
        self.menuModules = QtGui.QMenu(self.menubar)
        self.menuModules.setObjectName("menuModules")
        self.menuModules.setTitle(QtGui.QApplication.translate("MainWindow", "Modules", None, QtGui.QApplication.UnicodeUTF8))
 
        # MENU WINDOWS
        self.menuWindow = QtGui.QMenu(self.menubar)
        self.menuWindow.setObjectName("menuWindow")
        self.menuWindow.setTitle(QtGui.QApplication.translate("MainWindow", "Window", None, QtGui.QApplication.UnicodeUTF8))
        
        # MENU ?
        self.menuAbout = QtGui.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        self.menuAbout.setTitle(QtGui.QApplication.translate("MainWindow", "About", None, QtGui.QApplication.UnicodeUTF8))        
        
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setSizeGripEnabled(False)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.toolBarMain = QtGui.QToolBar(MainWindow)
        self.toolBarMain.setObjectName("CaseToolBar")
        self.toolBarMain.setWindowTitle(QtGui.QApplication.translate("MainWindow", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea,self.toolBarMain)
    
        self.setupActions(MainWindow)
    
        self.menuFile.addAction(self.actionNew_Dump)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        #self.menuEdit.addAction(self.actionConfigure)
        self.menuModules.addAction(self.actionLoad)
        self.menuModules.addSeparator()
        self.MenuTags = MenuTags(self, self)
        #self.menuWindow.addAction(self.actionCoreInformations)
        self.menuWindowMenuList = QMenu("List")
        self.menuWindow.addMenu(self.menuWindowMenuList)
        self.menuAbout.addAction(self.actionAbout)

        self.menubar.addAction(self.menuFile.menuAction())
       # self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuModules.menuAction())
        self.menubar.addAction(self.menuWindow.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())

        #self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.actionExit,QtCore.SIGNAL("triggered()"),MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    
    def setupActions(self, MainWindow):
        # MENU FILE
        self.actionNew_Dump = QtGui.QAction(MainWindow)
        self.actionNew_Dump.setEnabled(True)
        self.actionNew_Dump.setObjectName("actionNew_Dump")
        self.actionNew_Dump.setIcon(QIcon(":add.png"))
        self.actionNew_Dump.setIconText(QApplication.translate("MainWindow", "Add Dump", None, QApplication.UnicodeUTF8))
        self.actionNew_Dump.setText(QtGui.QApplication.translate("MainWindow", "Add Dump", None, QtGui.QApplication.UnicodeUTF8))
        
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionExit.setIcon(QIcon(":exit.png"))
        self.actionExit.setIconText(QApplication.translate("MainWindow", "Exit", None, QApplication.UnicodeUTF8))
        self.actionExit.setText(QtGui.QApplication.translate("MainWindow", "Exit", None, QtGui.QApplication.UnicodeUTF8))
        
        # MENU CONFIGURE
        self.actionConfigure = QtGui.QAction(MainWindow)
        self.actionConfigure.setObjectName("actionConfigure")
        self.actionConfigure.setIcon(QIcon(":configure.png"))
        self.actionConfigure.setIconText(QApplication.translate("MainWindow", "Configure", None, QApplication.UnicodeUTF8))
        self.actionConfigure.setText(QtGui.QApplication.translate("MainWindow", "Configure", None, QtGui.QApplication.UnicodeUTF8))
        
        #MENU MODULES
        self.actionLoad = QtGui.QAction(MainWindow)
        self.actionLoad.setEnabled(True)
        self.actionLoad.setObjectName("actionLoad")
        self.actionLoad.setText(QtGui.QApplication.translate("MainWindow", "Load", None, QtGui.QApplication.UnicodeUTF8))

        # MENU ABOUT
        self.actionAbout = QtGui.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionAbout.setText(QtGui.QApplication.translate("MainWindow", "?", None, QtGui.QApplication.UnicodeUTF8))
        
        #self.actionUnload = QtGui.QAction(MainWindow)
        #self.actionUnload.setEnabled(False)
        #self.actionUnload.setObjectName("actionUnload")
#        self.actionUnload.setText(QtGui.QApplication.translate("MainWindow", "Unload", None, QtGui.QApplication.UnicodeUTF8))
#        self.actionExtract = QtGui.QAction(MainWindow)
#        self.actionExtract.setObjectName("actionExtract")
#        self.actionExtract.setText(QtGui.QApplication.translate("MainWindow", "Extract", None, QtGui.QApplication.UnicodeUTF8))
#        self.ActionApplyDriverOnFile = QtGui.QAction(MainWindow)
#        self.ActionApplyDriverOnFile.setObjectName("ActionApplyDriverOnFile")
#        self.ActionApplyDriverOnFile.setText(QtGui.QApplication.translate("MainWindow", "Apply Driver", None, QtGui.QApplication.UnicodeUTF8))
#        self.actionExtractOnFile = QtGui.QAction(MainWindow)
#        self.actionExtractOnFile.setObjectName("actionExtractOnFile")
#        self.actionExtractOnFile.setText(QtGui.QApplication.translate("MainWindow", "Extract", None, QtGui.QApplication.UnicodeUTF8))

#        self.actionManage = QtGui.QAction(MainWindow)
#        self.actionManage.setObjectName("actionManage")
#        self.actionManage.setText(QtGui.QApplication.translate("MainWindow", "Manage", None, QtGui.QApplication.UnicodeUTF8))
        
#        self.actionExtractOnThumb = QtGui.QAction(MainWindow)
#        self.actionExtractOnThumb.setObjectName("actionExtractOnThumb")
#        self.actionExtractOnThumb.setText(QtGui.QApplication.translate("MainWindow", "Extract", None, QtGui.QApplication.UnicodeUTF8))
        self.actionTools = QtGui.QAction(MainWindow)
        self.actionTools.setCheckable(True)
        self.actionTools.setChecked(True)
        self.actionTools.setObjectName("actionTools")
#
#        self.actionViewers = QtGui.QAction(MainWindow)
#        self.actionViewers.setCheckable(True)
#        self.actionViewers.setChecked(True)
#        self.actionViewers.setObjectName("actionViewers")
#
#        self.actionProperty = QtGui.QAction(MainWindow)
#        self.actionProperty.setObjectName("actionProperty")
#
#        self.actionPropertyBrowser = QtGui.QAction(MainWindow)
#        self.actionPropertyBrowser.setObjectName("actionPropertyBrowser")

#        self.actionInfos = QtGui.QAction(MainWindow)
#        self.actionInfos.setCheckable(True)
#        self.actionInfos.setObjectName("actionInfos")
        
        self.actionApplyModule = QtGui.QAction(MainWindow)
        self.actionApplyModule.setObjectName("actionApplyModule")
        self.actionApplyModule.setIcon(QIcon(":applydriver.png"))
        self.actionApplyModule.setIconText(QApplication.translate("MainWindow", "Open With", None, QApplication.UnicodeUTF8))
        self.actionApplyModule.setText(QtGui.QApplication.translate("MainWindow", "Apply Module", None, QtGui.QApplication.UnicodeUTF8))
        
        self.actionShell = QtGui.QAction(MainWindow)
        self.actionShell.setObjectName("actionShell")
        self.actionShell.setIcon(QIcon(":shell.png"))
        self.actionShell.setIconText(QApplication.translate("MainWindow", "Open Shell", None, QApplication.UnicodeUTF8))
        self.actionShell.setText(QtGui.QApplication.translate("MainWindow", "Shell", None, QtGui.QApplication.UnicodeUTF8))
        
        self.actionInterpreter = QtGui.QAction(MainWindow)
        self.actionInterpreter.setObjectName("actionInterpreter")
        self.actionInterpreter.setIcon(QIcon(":interpreter.png"))
        self.actionInterpreter.setIconText(QApplication.translate("MainWindow", "Open Interpreter", None, QApplication.UnicodeUTF8))
        self.actionInterpreter.setText(QtGui.QApplication.translate("MainWindow", "Interpreter", None, QtGui.QApplication.UnicodeUTF8))
        
        self.actionList_Files = QtGui.QAction(MainWindow)
        self.actionList_Files.setObjectName("actionList_Files")
        self.actionList_Files.setIcon(QIcon(":list.png"))
        self.actionList_Files.setIconText(QApplication.translate("MainWindow", "Open List", None, QApplication.UnicodeUTF8))
        self.actionList_Files.setText(QtGui.QApplication.translate("MainWindow", "List Files", None, QtGui.QApplication.UnicodeUTF8))
        
    
        
        
#        self.actionBrowser.setText(QtGui.QApplication.translate("MainWindow", "Browser", None, QtGui.QApplication.UnicodeUTF8))
        
        
#        self.actionTools.setText(QtGui.QApplication.translate("MainWindow", "Tools", None, QtGui.QApplication.UnicodeUTF8))
#        self.actionViewers.setText(QtGui.QApplication.translate("MainWindow", "Viewer", None, QtGui.QApplication.UnicodeUTF8))
#        self.actionProperty.setText(QtGui.QApplication.translate("MainWindow", "Property", None, QtGui.QApplication.UnicodeUTF8))
#        self.actionPropertyBrowser.setText(QtGui.QApplication.translate("MainWindow", "Property", None, QtGui.QApplication.UnicodeUTF8))
#        self.actionInfos.setText(QtGui.QApplication.translate("MainWindow", "Infos", None, QtGui.QApplication.UnicodeUTF8))
        
