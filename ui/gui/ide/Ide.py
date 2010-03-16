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
from PyQt4.Qsci import *

#wizard
from ideWizard import ideWizard

from generateCode import generateCode
from messageBox import messageBoxWarningSave,  messageBoxErrorSave
from DFF_Editor import Editor

from api.loader import *

class Ide(QWidget):
    def __init__(self, parent):
        super(Ide,  self).__init__(parent)
        self.loader = loader.loader()
        self.parent = parent
        self.actions = parent.actions

        self.pages = []
        self.mainWindow = self.parent.getParent()
        
    def initActions(self):
        self.actions.saveact.connect(self.actions.saveact,  SIGNAL("triggered()"), self.saveactBack)
        self.actions.saveasact.connect(self.actions.saveasact,  SIGNAL("triggered()"), self.saveasactBack)
        self.actions.runact.connect(self.actions.runact,  SIGNAL("triggered()"), self.runactBack)
        self.actions.undoact.connect(self.actions.undoact,  SIGNAL("triggered()"), self.undoactBack)
        self.actions.redoact.connect(self.actions.redoact,  SIGNAL("triggered()"), self.redoactBack)

    def g_display(self):
        self.vbox = QVBoxLayout()
        self.createSplitter()
        self.setLayout(self.vbox)

        self.setToolbars()

        self.initActions()

    def setToolbars(self):

        self.actions.idetoolbar.setVisible(True)

        self.mainWindow.addToolBar(self.actions.idetoolbar)
        self.mainWindow.insertToolBarBreak(self.actions.idetoolbar)
        self.actions.enableActions()


    def createTabWidget(self):
        self.scripTab = QTabWidget()
        self.buttonCloseTab = QPushButton("")
        self.buttonCloseTab.setFixedSize(QSize(23,  23))
        self.buttonCloseTab.setIcon(QIcon(":cancel.png"))
        self.buttonCloseTab.setEnabled(False)
        self.scripTab.setCornerWidget(self.buttonCloseTab,  Qt.TopRightCorner)
        self.scripTab.connect(self.buttonCloseTab, SIGNAL("clicked()"), self.closeTabWidget)

    def createSplitter(self):
        self.splitter = QSplitter()
        self.createTabWidget()
        self.splitter.addWidget(self.scripTab)
        self.vbox.addWidget(self.splitter)

    def createPage(self,  buffer):
        page = Editor(self.scripTab)
        page.insertBuffer(buffer)
        self.pages.append(page)
        return page

    ######################
    ##       Scintilla creation             #
    ######################   
    def newactBack(self):
        #prepare for wizard        
        self.ideWiz = ideWizard(self, "New script")
#        self.ideWiz.exec_()
        #XXX cancel 
        ret = self.ideWiz.exec_()
        if ret > 0:
        #First page fields
            scriptname = self.ideWiz.field("name").toString()
            path = self.ideWiz.field("path").toString()
        #Get script type
            stype = self.ideWiz.field("typeS").toBool()
            gtype = self.ideWiz.field("typeG").toBool()
            dtype = self.ideWiz.field("typeD").toBool()

        #Get author's informations from wizard
            authfname = self.ideWiz.field("authFName").toString()
            authlname = self.ideWiz.field("authLName").toString()
            authmail = self.ideWiz.field("authMail").toString()
        #Generate script
            generate = generateCode()
            generate.set_header(authfname, authlname, authmail)
            if stype == True:
                buffer = generate.generate_script(str(scriptname))
                scin = self.createPage(buffer)
            if gtype == True:
                buffer = generate.generate_drivers(str(scriptname))
                scin = self.createPage(buffer)
            if dtype == True:
                buffer = generate.generate_script_gui(str(scriptname))
                scin = self.createPage(buffer)
            
            filename = scriptname + ".py"
                
            scin.setName(filename)

            if path[-1] != "/":
                path += "/"
            lpath = path + filename
            scin.setScriptPath(lpath)
            self.scripTab.addTab(scin,  filename)
            self.buttonCloseTab.setEnabled(True)
        else:
            if len(self.pages) == 0:
                self.mainWindow.removeDockWidget(self.mainWindow.dockWidget["IDE"])
                self.mainWindow.dockWidget["IDE"] = None
                self.actions.ide = self.mainWindow.dockWidget["IDE"]
                self.actions.idetoolbar.setVisible(False)

#            self.mainWindow.removeToolBar(self.actions.idetoolbar)
#            self.actions.disableActions()
    
    def openactBack(self):
        #POSIX
        sFileName = QFileDialog.getOpenFileName(self, QApplication.translate("MainWindow", "open", None, QApplication.UnicodeUTF8),"/home")
        if sFileName:
            file = open(sFileName,  "r")
            scin = self.createPage("")
            buffer = QString()
            buffer = file.read()
            scin.insert(buffer)
            
            #XXXX POSIX
            script = sFileName.split("/")
            
            scriptname = script[len(script) - 1]
            scin.setName(scriptname)
            
            scin.setScriptPath(sFileName)
            self.scripTab.addTab(scin,  scriptname)
            self.buttonCloseTab.setEnabled(True)
            file.close
        
    ######################
    ######################   
    
    def saveactBack(self):
        index = self.scripTab.currentIndex()
        page = self.pages[index]
        path = page.scriptPath
        if not path.isEmpty():
            file = open(path,  "w")
            file.write(page.text())
            file.close()
        else:
            self.saveasactBack()
            
    def saveasactBack(self):
        index = self.scripTab.currentIndex()
        title = self.scripTab.tabText(index)
        if title:
            sFileName = QFileDialog.getSaveFileName(self, QApplication.translate("MainWindow", "Save as", None, QApplication.UnicodeUTF8),title)
            page = self.pages[index]
            file = open(str(sFileName),"w")
            file.write(page.text())
            file.close()
        
    def runactBack(self):
        if self.scripTab.count() > 0:
            index = self.scripTab.currentIndex()
            page = self.pages[index]
            self.saveactBack()

            path = page.getScriptPath()
            self.loader.do_load(str(path))
        else:
            print "No script found"
        
    def undoactBack(self):
        if self.scripTab.count() > 0:
            index = self.scripTab.currentIndex()
            page = self.pages[index]
            page.undo()

    def redoactBack(self):
        if self.scripTab.count() > 0:
            index = self.scripTab.currentIndex()
            page = self.pages[index]
            page.redo()

    def closeTabWidget(self):
        if self.scripTab.count() > 0:
            index = self.scripTab.currentIndex()
            currentPage = self.scripTab.currentWidget()
            warning = messageBoxWarningSave(self,  "Save document?")
            warning.exec_()

            self.scripTab.removeTab(index)
            page = self.pages[index]
            self.pages.remove(page)
            currentPage.destroy(True, True)
            if self.scripTab.count() == 0:
                self.buttonCloseTab.setEnabled(False)
#                self.mainWindow.Ide_toolBar.disableToolbar()

   
