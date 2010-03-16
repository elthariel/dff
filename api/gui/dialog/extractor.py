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
#  Frederic Baguelin <fba@digital-forensic.org>


import os

from PyQt4.QtCore import QSize, SIGNAL, pyqtSignature
from PyQt4.QtGui import QDockWidget, QWidget, QVBoxLayout, QHBoxLayout, QIcon, QComboBox, QPushButton, QSortFilterProxyModel
from PyQt4.Qt import *


#Need some APIs functionnalities
class Extractor(QDialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        self.nodes = None
        self.grid = QGridLayout()
        self.vbox = QVBoxLayout()
        self.vbox.addLayout(self.grid)
        self.hbox = QHBoxLayout()
        self.setLayout(self.vbox)
        self.vbox.addLayout(self.hbox)
        self.actions()
        self.showArgs()
        self.path = ""
        self.hide()
        self.selectedNodes = []

    def launch(self, nodes):
        self.nodes = nodes
        self.show()


    def getArgs(self):
        args = {}
        args["nodes"] = self.selectedNodes
        args["recurse"] = self.recurseCheck.isChecked()
        args["path"] = self.path
        return args

    def actions(self):
        self.validate = QPushButton("Ok")
        self.cancel = QPushButton("Cancel")
        self.hbox.addWidget(self.validate)
        self.hbox.addWidget(self.cancel)
        self.connect(self.validate, SIGNAL("clicked()"), self.verify)
        self.connect(self.cancel, SIGNAL("clicked()"), self.close)


    def verify(self):
        if self.syspathLine.text() != "":
            self.checkIfExist()
            self.close()
            self.emit(SIGNAL("filled"))
        else:
            msg = QMessageBox(self)
            msg.setText("Extraction path is mandatory")
            msg.setIcon(QMessageBox.Warning)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

    def showArgs(self):
        self.syspathLabel = QLabel("destination folder")
        self.syspathLine = QLineEdit()
        self.syspathLine.setReadOnly(True)
        self.syspathBrowse = QPushButton("Browse")
        self.recurseCheck = QCheckBox("recursive mode")
        self.connect(self.syspathBrowse, SIGNAL("clicked()"), self.getExtractFolder)
        self.grid.addWidget(self.syspathLabel, 0, 0)
        self.grid.addWidget(self.syspathLine, 0, 1)
        self.grid.addWidget(self.syspathBrowse, 0, 2)
        self.grid.addWidget(self.recurseCheck, 1, 0)


    def getExtractFolder(self):
        dialog = QFileDialog(self, QApplication.translate("MainWindow", "Chose the destination folder for extraction", None, QApplication.UnicodeUTF8),  "/home")
        dialog.setFileMode(QFileDialog.DirectoryOnly)
        dialog.setViewMode(QFileDialog.Detail)
        ret = dialog.exec_()
        if ret:
            self.path = str(dialog.selectedFiles()[0])
            self.syspathLine.setText(self.path)
        return ret


    def removeIdentical(self, toRemove):
        res = []
        for node in self.nodes:
            if node.name not in toRemove:
                res.append(node)
        return res


    def checkIfExist(self):
        same = []
        content = os.listdir(self.path)
        for node in self.nodes:
            if node.name in content:
                same.append(str(node.name))
        if len(same) > 0:
            msg = QMessageBox(self)
            msg.setText("Some selected files or folders already exist in the destination folder\n" + str(self.path))
            msg.setInformativeText("Overwrite with selected ones ?")
            msg.setIcon(QMessageBox.Warning)
            items = "".join(s.join(["", "\n"]) for s in same)
            msg.setDetailedText(items)
            msg.setStandardButtons(QMessageBox.NoToAll | QMessageBox.YesToAll)
            msg.setDefaultButton(QMessageBox.NoToAll)
            ret = msg.exec_()
            if ret == QMessageBox.NoToAll:
                self.selectedNodes = self.removeIdentical(same)
            else:
                self.selectedNodes = self.nodes
        else:
            self.selectedNodes = self.nodes


