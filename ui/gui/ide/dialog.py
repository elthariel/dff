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

class dialog(QDialog):
    def __init__(self,  parent):
        super(dialog,  self).__init__(parent)
        self.ide = parent
        self.g_display()
        self.error = False
        
    def g_display(self):
        self.setWindowModality(Qt.ApplicationModal)

class newDialog(dialog):
    def __init__(self,  parent):
        dialog.__init__(self, parent)
        #self.g_display()
        self.initCallback()

    def g_display(self):
        self.newlayout = QGridLayout()
        lab = QLabel("Script name: ")
        self.scriptEdit = QLineEdit()
        
        label = QLabel("Language: ")
        self.langBox = QComboBox()
        self.langBox.addItem("Python")
        
        typelabel = QLabel("Type: ")
        self.typeBox = QComboBox()
        self.typeBox.addItem("Script")
        self.typeBox.addItem("Driver")
        self.typeBox.addItem("Graphical")
        self.typeBox.addItem("Empty")
        
        
        loclabel = QLabel("Location: ")
        self.brwButton = QPushButton("Browse")
        self.brwEdit = QLineEdit()
        self.brwEdit.setReadOnly(True)
        
        #self.newButton = QPushButton("Ok")
        #self.newButton.connect(self.newButton,  SIGNAL("clicked()"),  self.createScriptBack)
        
        self.buttonBox = QDialogButtonBox()
        self.buttonBox.setGeometry(QRect(9,403,403,28))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.NoButton|QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        
        self.newlayout.addWidget(lab,  0,  0)
        self.newlayout.addWidget(self.scriptEdit,  0,  1)
        self.newlayout.addWidget(label,  1,  0)
        self.newlayout.addWidget(self.langBox,  1,  1)
        self.newlayout.addWidget(typelabel,  2,  0)
        self.newlayout.addWidget(self.typeBox,  2,  1)
        self.newlayout.addWidget(self.brwEdit,  3,  1)
        self.newlayout.addWidget(self.brwButton,  3,  2)
        self.newlayout.addWidget(self.buttonBox,   4,  1)
        #self.newlayout.addWidget(self.newButton,  4,  2)
        self.setLayout(self.newlayout)

    def initCallback(self):
        self.connect(self.buttonBox, SIGNAL("accepted()"),self.accept)
        self.connect(self.buttonBox, SIGNAL("rejected()"),self.reject)
        self.connect(self.brwButton, SIGNAL("clicked()"),  self.browsLocationBack)
        
    def browsLocationBack(self):
        dirName = QFileDialog.getExistingDirectory(self, QApplication.translate("MainWindow", "Location", None, QApplication.UnicodeUTF8))
        self.brwEdit.setText(dirName)
        
    def getValues(self):
        values = []
        values.append(self.scriptEdit.text())
        values.append(self.brwEdit.text())
        values.append(self.langBox.currentText())
        values.append(self.typeBox.currentText())
        return  values
        
