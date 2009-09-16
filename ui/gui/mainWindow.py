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

import os

# Form Custom implementation of MAINWINDOW
from PyQt4.QtGui import QAction,  QApplication, QDockWidget, QFileDialog, QIcon, QMainWindow, QMessageBox
from PyQt4.QtCore import QEvent, Qt,  SIGNAL, QModelIndex

# Import the template generate by QtDesigner
from _mainWindow import Ui_MainWindow 

# CORE
from api.env import *
from api.taskmanager import *
from api.loader import *
from api.type import *

# CONFIGURATION
from configuration.configureDFF import DFF_ConfigureDFF
from configuration.Config import DFF_Conf
from configuration.Translator import DFF_Translator

# ENV
from widget.info import Info

# IDE
from ide.DFF_Ide import DFF_Ide
from ide.toolBar import DFF_ToolBar_Ide

# INTERPRETER
from widget.shell import Shell
from widget.interpreter import Interpreter
from widget.stdio import IO

# SCHEDULER
from scheduler.applyModule import DFF_ApplyModule
from api.taskmanager.taskmanager import * 

# UTILS
from utils.utils import DFF_Utils
from utils.selectNode import DFF_SelectNodes

# VFS
from vfs.treeDir.Browsers import DFF_Browsers
#from vfs.ListFolder.ListFiles import DFF_ListFiles
from vfs.propertyDialog import DFF_PropertyDialog
#from vfs.listFolder.refreshViewer import T_RefreshViewer

# Wrapper VFS
from wrapper.connectorCallback import ConnectorCallback

# The MAIN QWindow for DFF application a
class DFF_MainWindow(QMainWindow,  Ui_MainWindow):
    def __init__(self,  app):
        super(DFF_MainWindow,  self).__init__()
        self.setupUi(self)
        self.app = app
        self.DFF_CONFIG = DFF_Conf()
        self.taskmanager = TaskManager() 
        # QMenu List
        self.DFF_QMenu = {}
        
        # Custon MainWindow
        self.setWindowIcon(QIcon(":newlogo.jpg"))

        # Init VFS
        self.DFF_Callback = ConnectorCallback(self)
        self.env = env.env()
        self.tm = TaskManager()
        self.loader = loader.loader()
        
        # Init DFF_QDialogs
        self.QApplyModule = DFF_ApplyModule(self)
        self.QConfigureDFF = DFF_ConfigureDFF(self)
        self.QPropertyDialog = DFF_PropertyDialog(self)
        self.QSelectNodes = DFF_SelectNodes(self)
    
        self.initDockWidgets()
        #self.QTabCentralWidget = DFF_TabCentralWidget(self)
        #self.fillCentralWidget()
        
        # Init Callbacks
        self.setupCallback()
    
        # Init ToolBar
        self.initToolBars()

    ###############
    ## DOCK WIDGETS ##
    ##############
    def initDockWidgets(self):
        """Init Dock in application and init DockWidgets"""
        #self.setCorner(Qt.TopLeftCorner, Qt.LeftDockWidgetArea)
        self.setCorner(Qt.BottomLeftCorner, Qt.BottomDockWidgetArea)
        self.setCorner(Qt.TopRightCorner, Qt.TopDockWidgetArea)
        self.setCorner(Qt.BottomRightCorner, Qt.RightDockWidgetArea)
        
        #self.dockBrowser = DFF_Browsers(self, self.actionBrowser)
        
        DFF_Browsers(self)
        self.dockWidget = {}
        self.listDockWidget = []
        
        self.dockBrowser = DFF_Browsers.instance
        self.dockInfo = Info(self)

        self.dockShell = None
        self.dockInterpreter = None
        
        self.dockWidget["Info"] = self.dockInfo
        #self.dockInfoVFS.setVisible(False)
        #self.actionCoreInformations.setChecked(False)
        
        self.dockWidget["Interpreter"] = None
        self.dockWidget["IDE"] = None
        self.dockWidget["Resultat"] = None

        self.dockIO = IO(self)
        self.dockWidget["I/O"] = self.dockIO 
        	
#        self.dockWidget["Error"] = None
        self.addNewDockWidgetTab(Qt.BottomDockWidgetArea, self.dockWidget["Info"])
        self.addNewDockWidgetTab(Qt.BottomDockWidgetArea, self.dockWidget["I/O"])       
 
        self.dockWidget["Browser"] = DFF_Browsers.instance
        self.setCentralWidget(self.dockWidget["Browser"])
        dock = self.dockBrowser.addList()
        self.dockBrowser.setChild(dock.widget)
        
    def addNewDockWidgetTab(self, dockArea, dockWidget):
        if dockWidget is None :
            return
        for i in range(0, len(self.listDockWidget)) :
            area = self.dockWidgetArea(self.listDockWidget[i])
            if area == dockArea :
                self.tabifyDockWidget(self.listDockWidget[i], dockWidget)
                self.listDockWidget.append(dockWidget)
                return
        self.listDockWidget.append(dockWidget)
        self.addDockWidget(dockArea, dockWidget)
    
    def addResultatDockWidget(self, dockWidget):
        if self.dockWidget["Browser"] is None :
            self.dockWidget["Browser"] = dockWidget

    ################
    ## ADD DOCKWIDGET ##
    ################
    def addShell(self):
        if self.dockShell is None :
            self.dockShell = Shell(self)
            self.addNewDockWidgetTab(Qt.BottomDockWidgetArea, self.dockShell)
        if not self.dockShell.isVisible() :
            self.dockShell.show()

    def addInterpreter(self):
        if self.dockInterpreter is None :
            self.dockInterpreter = Interpreter(self)
            self.addNewDockWidgetTab(Qt.BottomDockWidgetArea, self.dockInterpreter)
        if not self.dockInterpreter.isVisible() :
            self.dockInterpreter.show()
 
    def addIde(self):
        if self.dockIDE is None :
            self.dockIDE = DFF_Ide(self)
            self.addNewDockWidgetTab(Qt.RightDockWidgetArea, self.dockIDE)
        if not self.dockIDE.isVisible() :
            self.dockIDE.show()
        
    #####################
    ## INIT AND CONNECT ACTION ##
    #####################
    def setupCallback(self):
        """ Init Actions """
        
        # MENU FILE
        self.connect(self.actionNew_Dump,  SIGNAL("triggered()"),  self.openAddDump)
        
        # MENU EDIT
        self.connect(self.actionConfigure, SIGNAL("triggered()"),  self.openConfigure)
        
        # MENU 
        self.connect(self.actionLoad, SIGNAL("triggered()"),  self.openLoadDriver)
        
        # MENU ABOUT
        self.connect(self.actionAbout,  SIGNAL("triggered()"),  self.openAbout)
      
        # DOCKWIDGET

        
        # TOOLBAR
        self.connect(self.actionApplyModule, SIGNAL("triggered()"),  self.openApplyModule)
        self.connect(self.actionShell, SIGNAL("triggered()"),  self.addShell)
        self.connect(self.actionInterpreter, SIGNAL("triggered()"),  self.addInterpreter)
        self.connect(self.actionList_Files, SIGNAL("triggered()"),  self.dockBrowser.addList)

    
    #############
    ## INIT TOOLBAR ##
    #############
    def initToolBars(self):
        """ Init Toolbar"""
        self.toolBarMain.addAction(self.actionNew_Dump)
        self.toolBarMain.addAction(self.actionApplyModule)
        self.toolBarMain.addAction(self.actionConfigure)
        self.toolBarMain.addAction(self.actionShell)
        self.toolBarMain.addAction(self.actionInterpreter)
        self.toolBarMain.addAction(self.actionList_Files)
        
        self.Ide_toolBar = DFF_ToolBar_Ide(self, self.dockWidget["IDE"])
        self.addToolBar(Qt.TopToolBarArea,self.Ide_toolBar)

    #####################
    ## CALLBACK FOR ALL ACTIONS #
    #####################
            
    ## MENU 
    #### NEW DUMP 
    def openAddDump(self):
        """ Open a Dialog for select a file and add in VFS """
        sFileName = QFileDialog.getOpenFileName(self, QApplication.translate("MainWindow", "Add Dump", None, QApplication.UnicodeUTF8),  os.path.expanduser('~'))
        if (sFileName) :
            arg = self.env.libenv.argument("gui_input")
            arg.thisown = 0
            arg.add_node("parent",  self.dockBrowser.DirModel.rootItemVFS.nodeVFS)
            tmp = libtype.Path(str(sFileName))
            tmp.thisown = 0
            arg.add_path("path", tmp)
            #arg.add_string("driver", "local")
	    exec_type = ["thread", "gui"]
            self.taskmanager.add("local", arg, exec_type)
            
    ## MENU
    #### PREFERENCES
    def openConfigure(self):
        """ Open a Dialog for Configure Application """
        if not self.QConfigureDFF.isVisible():
            iReturn = self.QConfigureDFF.exec_()
        else :
            QMessageBox.critical(self, "Erreur", u"This box is already open")
        
        # if the return of Qdialog is accept We create case object and fill the tree
        if (iReturn):
            # Get then clear info in QDialog for New Case
            conf = DFF_Conf()
            trans = DFF_Translator()
            lConf = self.QConfigureDFF.getAllInfo()
            if (conf.backupConfig(lConf) == 1) :
                QMessageBox.information(self, QApplication.translate("MainWindow", "Information", None, QtGui.QApplication.UnicodeUTF8), QApplication.translate("MainWindow", "Restart your application to complete your change.", None, QApplication.UnicodeUTF8))
            trans.loadLanguage()
            self.retranslateUi(self)
            self.resetInputContext ()

    ## MENU 
    #### ABOUT 
    def openAbout(self):
        """ Open a About Dialog """
        QMessageBox.information(self,  QApplication.translate("MainWindow", "About", None, QApplication.UnicodeUTF8),  QApplication.translate("MainWindow", "Digital Forensic Framework.<br><br>More information on www.digital-forensic.org", None, QApplication.UnicodeUTF8))
        
    #### APPLY MODULE
    def openApplyModule(self,  nameModule = None, typeModule = None, nodesSelected = None):
        if(self.QApplyModule.isVisible()):
            QMessageBox.critical(self, "Erreur", u"This box is already open")
        else:
            self.QApplyModule.initAllInformations(nameModule, typeModule,  nodesSelected)
            iReturn = self.QApplyModule.exec_()
        if iReturn :
            type = self.QApplyModule.currentType()
            script = self.QApplyModule.currentModuleName()
            arg = self.QApplyModule.getDFFArguments()
	    #fait ds getDFFArguments -> percot ....
            #self.tm.add(str(script), arg, ["thread", "gui"])
        self.QApplyModule.deleteAllArguments()
    
    def openLoadDriver(self):
        sFileName = QFileDialog.getOpenFileName(self, QApplication.translate("MainWindow", "Add Dump", None, QApplication.UnicodeUTF8),  "/home",  "Modules(*.so *.py *.dll *.mod);; driver(*.so *.dll);; script(*.py)")
        if (sFileName) :
            self.loader.do_load(str(sFileName))
            #self.dockInfoVFS.refresh()
     
    #################################
    ## FUNCTIONS FOR VISIBLE/HIDE DOCK WIDGETS  ##
    #################################
#    def changeVisibleBrowser(self):
#        if not self.dockBrowser.isVisible() :
#            self.dockBrowser.setVisible(True)
#            self.actionBrowser.setChecked(True)
#        else :
#            self.dockBrowser.setVisible(False)
#            self.actionBrowser.setChecked(False)
            
