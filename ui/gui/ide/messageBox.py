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

class messageBoxWarningSave(QMessageBox):
    def __init__(self,  parent,  message):
        super(messageBoxWarningSave,  self).__init__(parent)
        self.ide = parent
        self.message = message
        self.g_display()
        self.initCallback()
        
    def g_display(self):
        self.setText(self.message)
        self.yes = QPushButton("yes")
        self.addButton(self.yes,  QMessageBox.YesRole)
        self.no = QPushButton("no")
        self.addButton(self.no,  QMessageBox.NoRole)
        self.setIcon(QMessageBox.Warning)
        
    def initCallback(self):
        self.connect(self.yes, SIGNAL("clicked()"),self.accept)
        self.connect(self.no, SIGNAL("clicked()"),self.reject)
        
    def accept(self):
        self.ide.saveasactBack()
        self.destroy()
        
    def reject(self):
        self.destroy()


class messageBoxErrorSave(QMessageBox):
    def __init__(self,  parent,  message):
        super(messageBoxErrorSave,  self).__init__(parent)
        self.ide = parent
        self.message = message
        self.g_display()
        self.initCallback()
        
    def g_display(self):
        self.setText(self.message)
        self.ok = QPushButton("Ok")
        self.addButton(self.ok,  QMessageBox.AcceptRole)
        self.setIcon(QMessageBox.Critical)
        
    def initCallback(self):
        self.connect(self.ok, SIGNAL("clicked()"),self.accept)
        
    def accept(self):
        self.destroy()
        
