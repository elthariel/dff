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
from PyQt4.QtGui import QLayout

class UiProperty(object):
    def setupUi(self, PropertyDialog):
        PropertyDialog.setObjectName("PropertyDialog")
        PropertyDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        PropertyDialog.resize(QtCore.QSize(QtCore.QRect(0,0,405,160).size()).expandedTo(PropertyDialog.minimumSizeHint()))
        PropertyDialog.setMinimumSize(QtCore.QSize(405,160))

        self.widget = QtGui.QWidget(PropertyDialog)
        self.widget.setGeometry(QtCore.QRect(2,5,401,153))
        self.widget.setObjectName("widget")

        self.vboxlayout = QtGui.QVBoxLayout(self.widget)
        self.vboxlayout.setSpacing(-1)
        self.vboxlayout.setObjectName("vboxlayout")
        self.vboxlayout.setSizeConstraint(QLayout.SetMinAndMaxSize)
        
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setObjectName("hboxlayout")

        self.labelName = QtGui.QLabel(self.widget)
        self.labelName.setMinimumSize(QtCore.QSize(92,22))
        self.labelName.setMaximumSize(QtCore.QSize(92,22))

        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.labelName.setFont(font)
        self.labelName.setObjectName("labelName")
        self.hboxlayout.addWidget(self.labelName)

        self.valueName = QtGui.QLabel(self.widget)
        self.valueName.setMinimumSize(QtCore.QSize(300,22))
        self.valueName.setMaximumSize(QtCore.QSize(16777215,22))
        self.valueName.setObjectName("valueName")
        self.hboxlayout.addWidget(self.valueName)
        self.vboxlayout.addLayout(self.hboxlayout)

        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setObjectName("hboxlayout1")

        self.labelType = QtGui.QLabel(self.widget)
        self.labelType.setMinimumSize(QtCore.QSize(92,22))
        self.labelType.setMaximumSize(QtCore.QSize(92,22))

        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.labelType.setFont(font)
        self.labelType.setObjectName("labelType")
        self.hboxlayout1.addWidget(self.labelType)

        self.valueType = QtGui.QLabel(self.widget)
        self.valueType.setMinimumSize(QtCore.QSize(300,22))
        self.valueType.setMaximumSize(QtCore.QSize(16777215,22))
        self.valueType.setObjectName("valueType")
        self.hboxlayout1.addWidget(self.valueType)
        self.vboxlayout.addLayout(self.hboxlayout1)

        self.hboxlayout2 = QtGui.QHBoxLayout()
        self.hboxlayout2.setObjectName("hboxlayout2")

        self.labelPath = QtGui.QLabel(self.widget)
        self.labelPath.setMinimumSize(QtCore.QSize(92,22))
        self.labelPath.setMaximumSize(QtCore.QSize(92,22))

        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.labelPath.setFont(font)
        self.labelPath.setObjectName("labelPath")
        self.hboxlayout2.addWidget(self.labelPath)

        self.valuePath = QtGui.QLabel(self.widget)
        self.valuePath.setMinimumSize(QtCore.QSize(300,22))
        self.valuePath.setMaximumSize(QtCore.QSize(16777215,22))
        self.valuePath.setObjectName("valuePath")
        self.hboxlayout2.addWidget(self.valuePath)
        self.vboxlayout.addLayout(self.hboxlayout2)

        self.hboxlayout3 = QtGui.QHBoxLayout()
        self.hboxlayout3.setObjectName("hboxlayout3")

        self.labelSize = QtGui.QLabel(self.widget)
        self.labelSize.setMinimumSize(QtCore.QSize(92,22))
        self.labelSize.setMaximumSize(QtCore.QSize(92,22))

        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.labelSize.setFont(font)
        self.labelSize.setObjectName("labelSize")
        self.hboxlayout3.addWidget(self.labelSize)

        self.valueSize = QtGui.QLabel(self.widget)
        self.valueSize.setMinimumSize(QtCore.QSize(300,22))
        self.valueSize.setMaximumSize(QtCore.QSize(16777215,22))
        self.valueSize.setObjectName("valueSize")
        self.hboxlayout3.addWidget(self.valueSize)
        self.vboxlayout.addLayout(self.hboxlayout3)

        self.buttonClose = QtGui.QPushButton(self.widget)
        self.buttonClose.setMinimumSize(QtCore.QSize(70,28))
        self.buttonClose.setMaximumSize(QtCore.QSize(70,28))
        self.buttonClose.setObjectName("buttonClose")
        self.vboxlayout.addWidget(self.buttonClose)

        self.retranslateUi(PropertyDialog)
        QtCore.QObject.connect(self.buttonClose,QtCore.SIGNAL("clicked()"),PropertyDialog.accept)
        QtCore.QMetaObject.connectSlotsByName(PropertyDialog)

    def retranslateUi(self, PropertyDialog):
        PropertyDialog.setWindowTitle(QtGui.QApplication.translate("PropertyDialog", "Property", None, QtGui.QApplication.UnicodeUTF8))
        self.labelName.setText(QtGui.QApplication.translate("PropertyDialog", "Name :", None, QtGui.QApplication.UnicodeUTF8))
        self.labelType.setText(QtGui.QApplication.translate("PropertyDialog", "Type :", None, QtGui.QApplication.UnicodeUTF8))
        self.labelPath.setText(QtGui.QApplication.translate("PropertyDialog", "Location :", None, QtGui.QApplication.UnicodeUTF8))
        self.labelSize.setText(QtGui.QApplication.translate("PropertyDialog", "Contents :", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonClose.setText(QtGui.QApplication.translate("PropertyDialog", "Close", None, QtGui.QApplication.UnicodeUTF8))

