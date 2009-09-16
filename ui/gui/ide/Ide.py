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
from PyQt4.Qsci import *

from dialog import newDialog
from generateCode import generateCode
from messageBox import messageBoxWarningSave,  messageBoxErrorSave
from DFF_Editor import Editor

from api.loader import *

class Ide(QWidget):
    def __init__(self, parent):
        super(Ide,  self).__init__(parent)
        self.loader = loader.loader()
        #self.scripts = []
        self.pages = []
        
    def g_display(self):
        self.vbox = QVBoxLayout()
        self.newdialog = newDialog(self)
        self.createSplitter()
        self.setLayout(self.vbox)

    def createTabWidget(self):
        self.scripTab = QTabWidget()
        self.buttonCloseTab = QPushButton("")
        self.buttonCloseTab.setFixedSize(QSize(23,  23))
        self.buttonCloseTab.setIcon(QIcon(":closetab.png"))
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
        if not self.newdialog.isVisible():
            iReturn = self.newdialog.exec_()

            if iReturn :
                values = self.newdialog.getValues()
                scriptname = values[0]
                if scriptname == "":
                    scriptname = "Untitled"
                location = values[1]
                ext = values[2]
                if ext == "Python":
                    scriptname += ".py"
                elif ext == "C++":
                    scriptname += ".cpp"
                type = values[3]

                name = scriptname.split('.')
                if type == "Script":
                    generate = generateCode()
                    print "name generate ", name[0]
                    buffer = generate.generate_script(str(name[0]))
                    scin = self.createPage(buffer)
                elif type == "Driver":
                    generate = generateCode()
                    buffer = generate.generate_drivers(str(name[0]))
                    scin = self.createPage(buffer)
                elif type == "Graphical":
                    generate = generateCode()
                    buffer = generate.generate_script_gui(str(name[0]))
                    scin = self.createPage(buffer)
                elif type == "Empty":
                    scin = self.createPage("")
                        
                scin.setName(scriptname)
                path = location + scriptname
                scin.setScriptPath(path)
                self.scripTab.addTab(scin,  scriptname)
                self.buttonCloseTab.setEnabled(True)
    
    def openactBack(self):
        #POSIX
        sFileName = QFileDialog.getOpenFileName(self, QApplication.translate("MainWindow", "open", None, QApplication.UnicodeUTF8),"/home")
        if sFileName:
            file = open(sFileName,  "r")
            scin = self.createPage("")
            #self.scripts.append(sFileName)
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
            #current = self.scripTab.currentWidget()
            #filename = self.scripts[index]
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
            print sFileName
            #current = self.scripTab.currentWidget()
            page = self.pages[index]
            file = open(str(sFileName),"w")
            file.write(page.text())
            file.close()
        
    def runactBack(self):
        if self.scripTab.count() > 0:
            index = self.scripTab.currentIndex()
            #path = self.scripts[index]
            page = self.pages[index]
            self.saveactBack()
            path = page.getScriptPath()
            self.loader.do_load(str(path))
            
    def undoactBack(self):
        if self.scripTab.count() > 0:
            index = self.scripTab.currentIndex()
            #path = self.scripts[index]
            page = self.pages[index]
            page.undo()

    def redoactBack(self):
        if self.scripTab.count() > 0:
            index = self.scripTab.currentIndex()
            #path = self.scripts[index]
            page = self.pages[index]
            page.redo()

    def closeTabWidget(self):
        if self.scripTab.count() > 0:
            index = self.scripTab.currentIndex()
            currentPage = self.scripTab.currentWidget()
            warning = messageBoxWarningSave(self,  "Save document?")
            warning.exec_()
            self.scripTab.removeTab(index)
            currentPage.destroy()
            if self.scripTab.count() == 0:
                self.buttonCloseTab.setEnabled(False)

   
