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

from PyQt4.QtGui import QApplication, QFileDialog, QPushButton
from PyQt4.QtCore import QSize, SIGNAL

# My QPushButton
# TargetResult
# type 0 Normal, 1 VFS
class DFF_BrowserButton(QPushButton):
    def __init__(self, parent, targetResult, arg_name, browseVFS = 0, nodeVFS = 0):
        QPushButton.__init__(self,  parent)
        self.targetResult = targetResult
        self.browseVFS = browseVFS
        self.nodeVFS = nodeVFS
        self.setObjectName("Button" + arg_name)
        self.setText(QApplication.translate("DFF_BrowserButton", "Browse", None, QApplication.UnicodeUTF8))
        self.setFixedSize(QSize(80,  28))
        self.connect(self,  SIGNAL("clicked()"), self.clickOnMe)
        
    def clickOnMe(self):
        if self.browseVFS == 0 :
            sFileName = QFileDialog.getOpenFileName(self, QApplication.translate("DFF_BrowserButton", "Add Dump", None, QApplication.UnicodeUTF8),  "/home")
            if (sFileName) :
                self.targetResult.addPathAndSelect(sFileName)
        else :
            if not self.browseVFS.isVisible():
                self.browseVFS.displayDirectory(self.nodeVFS)
                iReturn = self.browseVFS.exec_()
                if iReturn :
                    node = self.browseVFS.returnSelection()
                    if node :
                        self.targetResult.addPathAndSelect(node)
                    #self.targetResult.addPathAndSelect(node.path + "/" + node.name)
