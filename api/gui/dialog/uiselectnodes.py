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

from PyQt4 import QtCore, QtGui

class UiSelectNodes(object):
    def setupUi(self, selectNode):
        selectNode.setObjectName("selectNode")
        selectNode.setWindowModality(QtCore.Qt.ApplicationModal)
        selectNode.resize(QtCore.QSize(QtCore.QRect(0,0,422,321).size()).expandedTo(selectNode.minimumSizeHint()))
        selectNode.setMinimumSize(QtCore.QSize(422,321))

        self.vboxlayout = QtGui.QVBoxLayout(selectNode)
        self.vboxlayout.setObjectName("vboxlayout")

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setObjectName("hboxlayout")

        self.label = QtGui.QLabel(selectNode)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(96,28))
        self.label.setMaximumSize(QtCore.QSize(96,28))
        self.label.setObjectName("label")
        self.hboxlayout.addWidget(self.label)

        self.topButton = QtGui.QPushButton(selectNode)
        self.topButton.setMinimumSize(QtCore.QSize(28,28))
        self.topButton.setMaximumSize(QtCore.QSize(28,28))
        self.topButton.setObjectName("topButton")
        self.hboxlayout.addWidget(self.topButton)
        self.vboxlayout.addLayout(self.hboxlayout)

        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setObjectName("hboxlayout1")

        self.currentSelectionEdit = QtGui.QLineEdit(selectNode)
        self.currentSelectionEdit.setReadOnly(True)
        self.currentSelectionEdit.setObjectName("currentSelectionEdit")
        self.hboxlayout1.addWidget(self.currentSelectionEdit)

        self.selectButton = QtGui.QPushButton(selectNode)
        self.selectButton.setMinimumSize(QtCore.QSize(75,28))
        self.selectButton.setMaximumSize(QtCore.QSize(75,28))
        self.selectButton.setObjectName("selectButton")
        self.hboxlayout1.addWidget(self.selectButton)
        self.vboxlayout.addLayout(self.hboxlayout1)

        self.hboxlayout2 = QtGui.QHBoxLayout()
        self.hboxlayout2.setObjectName("hboxlayout2")

        spacerItem = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout2.addItem(spacerItem)

        self.cancelButton = QtGui.QPushButton(selectNode)
        self.cancelButton.setMinimumSize(QtCore.QSize(75,28))
        self.cancelButton.setMaximumSize(QtCore.QSize(75,28))
        self.cancelButton.setObjectName("cancelButton")
        self.hboxlayout2.addWidget(self.cancelButton)
        self.vboxlayout.addLayout(self.hboxlayout2)

        self.retranslateUi(selectNode)
        QtCore.QObject.connect(self.selectButton,QtCore.SIGNAL("clicked()"),selectNode.accept)
        QtCore.QObject.connect(self.cancelButton,QtCore.SIGNAL("clicked()"),selectNode.reject)
        QtCore.QMetaObject.connectSlotsByName(selectNode)

    def retranslateUi(self, selectNode):
        selectNode.setWindowTitle(QtGui.QApplication.translate("selectNode", "Select a node", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("selectNode", "Look in :", None, QtGui.QApplication.UnicodeUTF8))
        self.selectButton.setText(QtGui.QApplication.translate("selectNode", "Select", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelButton.setText(QtGui.QApplication.translate("selectNode", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

