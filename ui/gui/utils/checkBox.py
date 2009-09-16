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

from PyQt4.QtGui import QCheckBox
from PyQt4.QtCore import QObject, QSize, Qt, SIGNAL

class DFF_CheckBoxWidgetEnable(QCheckBox):
    def __init__(self, parent, label, value,  browser = None):
        QCheckBox.__init__(self)
        #QCheckBox.__init__(self, parent)
        self.__label = label
        self.__value = value
        self.__browser= browser
        self.configure()
        self.initCallback()
    
    def configure(self):
        self.setFixedSize(QSize(20, 20))
        self.__value.setEnabled(0)
        self.__label.setEnabled(0)
        if self.__browser:
            self.__browser.setEnabled(0)
    
    def initCallback(self):
        self.connect(self, SIGNAL("stateChanged(int )"), self.stateChangedWidget)
        self.connect(self, SIGNAL("destroyed(QObject *)"), self.destroyMe)
    
    def destroyMe(self, obj):
	pass       
 
    def stateChangedWidget(self,  state):
        if state == Qt.Checked :
            self.__value.setEnabled(1)
            self.__label.setEnabled(1)
            if self.__browser :
                self.__browser.setEnabled(1)
        else :
            self.__value.setEnabled(0)
            self.__label.setEnabled(0)
            if self.__browser :
                self.__browser.setEnabled(0)
