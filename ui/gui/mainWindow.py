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
#  Francois Percot <percot@gmail.com>
# 

import os

# Form Custom implementation of MAINWINDOW
from PyQt4.QtGui import QAction,  QApplication, QDockWidget, QFileDialog, QIcon, QMainWindow, QMessageBox
from PyQt4.QtCore import QEvent, Qt,  SIGNAL, QModelIndex, QSettings

# Import the template generate by QtDesigner
from _mainWindow import Ui_MainWindow 

# CORE
from api.env import *
from api.taskmanager import *
from api.loader import *
from api.type import *

from api.vfs import *

# CONFIGURATION
from configuration.configureDFF import DFF_ConfigureDFF
from configuration.Config import DFF_Conf
from configuration.Translator import DFF_Translator

# ENV
from widget.info import Info

# IDE
from ide.DFF_Ide import DFF_Ide
#from ide.toolBar import DFF_ToolBar_Ide

# INTERPRETER
from widget.shell import Shell
from widget.interpreter import Interpreter
from widget.stdio import IO

# SCHEDULER
from api.taskmanager.taskmanager import * 

# UTILS
from utils.utils import DFF_Utils
from api.gui.dialog.selectnodes import SelectNodes

from api.gui.dialog.applymodule import ApplyModule
from api.gui.widget.nodetree import NodeTree
from api.gui.dialog.property import Property

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
        self.QApplyModule = ApplyModule(self)
        self.QConfigureDFF = DFF_ConfigureDFF(self)
        self.QPropertyDialog = Property(self)
        self.QSelectNodes = SelectNodes(self)
    
        self.initDockWidgets()
        # Init Callbacks
        self.setupCallback()    
        # Init ToolBar
        self.initToolBars()

        self.readSettings()

    ###############
    ## DOCK WIDGETS ##
    ##############
    def initDockWidgets(self):
        """Init Dock in application and init DockWidgets"""
        #self.setCorner(Qt.TopLeftCorner, Qt.LeftDockWidgetArea)
        self.setCorner(Qt.BottomLeftCorner, Qt.BottomDockWidgetArea)
        self.setCorner(Qt.TopRightCorner, Qt.TopDockWidgetArea)
        self.setCorner(Qt.BottomRightCorner, Qt.RightDockWidgetArea)

        NodeTree(self)
        self.dockWidget = {}
        self.listDockWidget = []
        
        self.dockNodeTree = NodeTree.instance
        self.dockInfo = Info(self)
        self.dockShell = None
        self.dockInterpreter = None
        self.dockIO = IO(self)

        self.dockWidget["Interpreter"] = None
        self.dockWidget["IDE"] = None

        self.dockWidget["Resultat"] = None
        self.dockWidget["I/O"] = self.dockIO 
        self.dockWidget["Info"] = self.dockInfo
                	
        self.addNewDockWidgetTab(Qt.BottomDockWidgetArea, self.dockWidget["I/O"])
        self.addNewDockWidgetTab(Qt.BottomDockWidgetArea, self.dockWidget["Info"])
 

        self.dockWidget["NodeTree"] = NodeTree.instance
        self.setCentralWidget(self.dockWidget["NodeTree"])

        dock = self.dockNodeTree.addList()
        self.dockNodeTree.setChild(dock.widget)
        
    def addNewDockWidgetTab(self, dockArea, dockWidget):
        if dockWidget is None :
            return

        for i in range(0, len(self.listDockWidget)) :
            area = self.dockWidgetArea(self.listDockWidget[i])
            if area == dockArea :
                self.addDockWidget(dockArea, dockWidget)
                self.tabifyDockWidget(self.listDockWidget[i], dockWidget)
                return

        self.listDockWidget.append(dockWidget)
        self.addDockWidget(dockArea, dockWidget)
    
    def addResultatDockWidget(self, dockWidget):
        if self.dockWidget["NodeTree"] is None :
            self.dockWidget["NodeTree"] = dockWidget


    ################
    ## ADD DOCKWIDGET ##
    ################
    def addShell(self):
        if self.dockShell is None :
            self.dockShell = Shell(self)
            self.addNewDockWidgetTab(Qt.RightDockWidgetArea, self.dockShell)
        if not self.dockShell.isVisible() :
            self.dockShell.show()

    def addInterpreter(self):
        if self.dockInterpreter is None :
            self.dockInterpreter = Interpreter(self)
            self.addNewDockWidgetTab(Qt.RightDockWidgetArea, self.dockInterpreter)
        if not self.dockInterpreter.isVisible() :
            self.dockInterpreter.show()
 
    #####################
    ## INIT AND CONNECT ACTION ##
    #####################
    def setupCallback(self):
        """ Init Actions """        
        # MENU FILE
        self.connect(self.actionNew_Dump, SIGNAL("triggered()"),  self.openAddDump)

        # MENU 
        self.connect(self.actionLoad, SIGNAL("triggered()"),  self.openLoadDriver)
        
        # MENU ABOUT
        self.connect(self.actionAbout,  SIGNAL("triggered()"),  self.openAbout)
      
        # DOCKWIDGET

        # TOOLBAR
        self.connect(self.actionApplyModule, SIGNAL("triggered()"),  self.openApplyModule)
        self.connect(self.actionShell, SIGNAL("triggered()"),  self.addShell)
        self.connect(self.actionInterpreter, SIGNAL("triggered()"),  self.addInterpreter)
        self.connect(self.actionList_Files, SIGNAL("triggered()"),  self.dockNodeTree.addList)

    
    #############
    ## INIT TOOLBAR ##
    #############
    def initToolBars(self):
        """ Init Toolbar"""
        self.toolBarMain.addAction(self.actionNew_Dump)        

        self.toolBarMain.addSeparator()

        self.toolBarMain.addAction(self.actionApplyModule)
        self.toolBarMain.addAction(self.actionShell)
        self.toolBarMain.addAction(self.actionInterpreter)
        self.toolBarMain.addAction(self.actionList_Files)

        self.addToolBar(Qt.TopToolBarArea, self.ideActions.maintoolbar)

    #####################
    ## CALLBACK FOR ALL ACTIONS #
    #####################
            
    ## MENU 
    #### NEW DUMP 
    def openAddDump(self):
        """ Open a Dialog for select a file and add in VFS """
        sFileName = QFileDialog.getOpenFileNames(self, QApplication.translate("MainWindow", "Add Dumps", None, QApplication.UnicodeUTF8),  os.path.expanduser('~'))
        for name in sFileName:
            arg = self.env.libenv.argument("gui_input")
            arg.thisown = 0
            arg.add_node("parent",  self.dockNodeTree.treeItemModel.rootItem.node)
	    arg.add_path("path", str(name))
	    exec_type = ["thread", "gui"]
            self.taskmanager.add("local", arg, exec_type)
            
    ## MENU 
    #### ABOUT 
    def openAbout(self):
        """ Open a About Dialog """
        QMessageBox.information(self,  QApplication.translate("MainWindow", "About", None, QApplication.UnicodeUTF8),  QApplication.translate("MainWindow", "<b>Digital Forensics Framework</b> (version 0.5)<br><br> If you have any troubles, please visit our <a href=\"http://wiki.digital-forensic.org\"> support page</a><br>IRC channel: freenode #digital-forensic<br>More information: <a href=\"ht\
tp://www.digital-forensic.org\"> digital-forensic </a><br><br>Software developed by <a href=\"http://arxsys.fr\"> ArxSys</a>", None, QApplication.UnicodeUTF8))
        
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
        self.QApplyModule.deleteAllArguments()
    
    def openLoadDriver(self):
        sFileName = QFileDialog.getOpenFileName(self, QApplication.translate("MainWindow", "Add Dump", None, QApplication.UnicodeUTF8),  "/home",  "Modules(*.so *.py *.dll *.mod);; driver(*.so *.dll);; script(*.py)")
        if (sFileName) :
            self.loader.do_load(str(sFileName))

    def closeEvent(self, e):
        settings = QSettings("ArxSys", "DFF-0.5")
	settings.setValue("geometry", self.saveGeometry())
	settings.setValue("windowState", self.saveState())

    def readSettings(self):
	settings = QSettings("ArxSys", "DFF-0.5")
	self.restoreGeometry(settings.value("geometry").toByteArray())
	self.restoreState(settings.value("windowState").toByteArray())
          
