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

from PyQt4.QtGui import QAbstractItemView, QApplication, QCursor, QFileDialog, QFont, QHeaderView, QIcon,  QMenu, QMessageBox, QTreeView
from PyQt4.QtCore import QModelIndex,  Qt, SIGNAL

from ui.gui.utils.menu import MenuModules, MenuTags
from ui.gui.utils.utils import DFF_Utils

class DirView(QTreeView):
    # TAKE :        None
    def __init__(self, parent,  mainWindow, model):
        super(DirView,  self).__init__(parent)
        self.__model = model
        self.__mainWindow = mainWindow
        self.__parent = parent
        self.__childForIndex = None
        
        self.configure()
        self.initCallback()
        self.createSubMenu()
        
    def configure(self):
        self.setAnimated(1)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setItemsExpandable(True)
        self.setUniformRowHeights(True)
        self.header().setClickable(True)
        #self.header().setHighlightSections(True)
        
        font = QFont()
        font.setPointSize(8)
        self.setFont(font)

    def initCallback(self):
        self.connect(self,  SIGNAL("expanded(const QModelIndex &)"), self.itemExpanded)
        #self.connect(self.header(),  SIGNAL("sectionClicked(int)"), self.clickOnHeader)
    
    def itemExpanded(self, index):
        self.resizeAllColumn()
        
    #deprecated
    def clickOnHeader(self,  index):
        self.clearSelection()
        self.changeDirectory(self.model().rootItem.nodeVFS, None)
        self.setCurrentIndex(self.header().rootIndex())
    
    def getCurrentItem(self):
        currentIndexBrowser = self.selectionModel().currentIndex()
        if currentIndexBrowser :
            currentItemBrowser = self.model().getItem(currentIndexBrowser)
            return currentItemBrowser
        return False
    
    def getCurrentNode(self):
        currentIndexBrowser = self.selectionModel().currentIndex()
        if currentIndexBrowser :
            currentItemBrowser = self.model().getItem(currentIndexBrowser)
            return currentItemBrowser.nodeVFS
        return False
    
    ##
    ## Overload Functions
    ## 
    def currentChanged(self,  currentIndex,  previousIndex):
        #child = self.__parent.getChild()
        #if currentIndex == previousIndex :
        #if currentIndex == previousIndex and str(child) == str(self.__childForIndex):
            #return 
        #self.__childForIndex = child
        itemClicked = self.model().getItem(currentIndex)
        self.changeDirectory(itemClicked.nodeVFS, currentIndex)
        self.scrollTo(currentIndex)
    
    def mouseDoubleClickEvent(self, e):
        indexClicked = self.indexAt(e.pos())
        if indexClicked.isValid():
            if self.isExpanded(indexClicked):
                self.setExpanded(indexClicked, False)
            else :
                if self.model().hasChildren(indexClicked) == True:
                    self.setExpanded(indexClicked, True)
        return
                
    def mousePressEvent(self, event):
        indexClicked = self.indexAt(event.pos())
        
        if  not indexClicked:
            return
        if not indexClicked.isValid():
            return
        itemClicked = self.model().getItem(indexClicked)
                
        # check If the click is on the Cross of ItemClicked
        if self.itemsExpandable() and itemClicked.childCount() <> 0 and self.itemDecorationAt(itemClicked,  event):
            if (not self.isExpanded(indexClicked)) :
                self.setExpanded(indexClicked,  True)
            else :
                self.setExpanded(indexClicked,  False)
            return
        
        #self.changeDirectory(itemClicked.nodeVFS,  indexClicked)
        self.setCurrentIndex(indexClicked)
            
        # RIGHT CLICK
        if event.button() == Qt.RightButton:
            self.submenuFile.popup(QCursor.pos())
            self.submenuFile.show()
            return 
    
    def resizeAllColumn(self):
        for i in range(0, self.model().columnCount(0)):
            self.resizeColumnToContents(i)

    ## Check if the click is on the cross
    def itemDecorationAt(self,  itemClicked,  event):
        indentation = (itemClicked.getLevel() - 1) * self.indentation()
        scrollbar = self.horizontalScrollBar()
        resultat = scrollbar.value() + event.x() - indentation
        if resultat <= 15 and resultat >= 4:
            return True
        else :
            return False
        
    def changeDirectory(self, itemClicked,  index,  force = None):
        self.emit(SIGNAL("changeDirectory"), itemClicked, index, force)

    def setCurrentIndexForChild(self, child, index):
        if str(self.__parent.getChild()) <> str(child):
            self.__parent.setChild(child)
        self.setCurrentIndex(index)
        
    def setIndexAndExpand(self,  child, index):
        if str(self.__parent.getChild()) <> str(child):
            self.__parent.setChild(child)

        if index <> None and index.isValid():
            if self.currentIndex() <> index :
                self.setCurrentIndex(index)
            else :
                itemClicked = self.model().getItem(index)
                self.changeDirectory(itemClicked.nodeVFS, index)
            self.expandAllIndex(index)
        else :
            self.setCurrentIndex(QModelIndex())
            self.clearSelection()
                
    def expandAllIndex(self, index):
        if not index : 
            return

        parent = self.model().parent2(index)
        while (parent <> False) :
            if (not self.isExpanded(parent)) :
                self.setExpanded(parent,  True)
            parent = self.model().parent2(parent)
    
    def createSubMenu(self):
        self.submenuFile = QMenu()
        self.submenuOpenIn = self.submenuFile.addMenu("Open in")
        self.submenuOpenIn.addAction(QApplication.translate("MainWindow", "List Files", None, QApplication.UnicodeUTF8),  self.parent().addList, "mainWindow")
        self.submenuFile.addSeparator()
        self.submenuFile.addAction(QIcon(":shell.png"), QApplication.translate("MainWindow", "Shell", None, QApplication.UnicodeUTF8),  self.__mainWindow.addShell)
        self.submenuFile.addAction(QIcon(":interpreter.png"), QApplication.translate("MainWindow", "Interpreter", None, QApplication.UnicodeUTF8),  self.__mainWindow.addInterpreter)
        self.submenuFile.addSeparator()
        self.menuModules = self.submenuFile.addMenu(QIcon(":applydriver.png"), QApplication.translate("ListView", "Open With", None, QApplication.UnicodeUTF8))
        self.menuTags = MenuTags(self, self.__mainWindow, self.getCurrentNode)	
#        self.submenuFile.addSeparator()
#        self.submenuFile.addAction(QIcon(":extract.png"), QApplication.translate("MainWindow", "Extract", None, QApplication.UnicodeUTF8),  self.extractFolder, "mainWindow")
        self.submenuFile.addSeparator()
        self.submenuFile.addAction(QIcon(":info.png"), QApplication.translate("MainWindow", "Property", None, QApplication.UnicodeUTF8),  self.propertyFolder, "mainWindow")
    
    
    #################
    ## CALLBACK SUBMENU ##
    #################
    def extractFolder(self):
        if self.__mainWindow.DFF_CONFIG.extractFolder == "" :
            sDirName = QFileDialog.getExistingDirectory(self, QApplication.translate("MainWindow", "Choose Your Directory For Extraction", None, QApplication.UnicodeUTF8),  "/home",  QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
            if (sDirName) :
                self.__mainWindow.DFF_CONFIG.extractFolder = sDirName
            else :
                return
        tmp = [self.getCurrentNode()]
        DFF_Utils().execExtract(tmp, self.__mainWindow.DFF_CONFIG.extractFolder)
    
    def propertyFolder(self):
        if not self.__mainWindow.QPropertyDialog.isVisible():
            listNode = [self.getCurrentNode()]
            self.__mainWindow.QPropertyDialog.fillInfo(self.getCurrentItem().parentItem.nodeVFS, listNode)
            iReturn = self.__mainWindow.QPropertyDialog.exec_()
        else:
            QMessageBox.critical(self, "Erreur", u"This box is already open.")
