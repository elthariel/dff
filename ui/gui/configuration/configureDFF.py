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

# Form Custom implementation of CONFIGUREDFF
from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QApplication, QDialog, QFileDialog

# Import the template generate by QtDesigner
from _configureDFF import Ui_ConfigureDFF 

# Import Singleton for CONF
from Config import DFF_Conf

# QDialog for Fill the information about the newCase
class DFF_ConfigureDFF(QDialog,  Ui_ConfigureDFF):
    def __init__(self,  parent):
        QDialog.__init__(self,  parent)
        Ui_ConfigureDFF.__init__(self)
        self.setupUi(self)
        self.Conf = DFF_Conf()
        self.initLanguage()
        self.connect(self.buttonSelectWorkspace,  SIGNAL("clicked()"), self.selectWorkspace)
    
    def initLanguage(self):
        if self.Conf.language == "FR" :
            self.LanguageBox.addItem(QApplication.translate("DFF_ConfigureDFF", "French", None, QApplication.UnicodeUTF8))
            self.LanguageBox.addItem(QApplication.translate("DFF_ConfigureDFF", "English", None, QApplication.UnicodeUTF8))
        else :
            self.LanguageBox.addItem(QApplication.translate("DFF_ConfigureDFF", "English", None, QApplication.UnicodeUTF8))
            self.LanguageBox.addItem(QApplication.translate("DFF_ConfigureDFF", "French", None, QApplication.UnicodeUTF8))
        
    # Get the information about the config
    def getAllInfo(self):
        lParam = []
        lParam.append(self.LanguageBox.currentIndex())
        lParam.append(self.valueWorkspace.text())
        return lParam
        
    def selectWorkspace(self):
        sDirPath = QFileDialog.getExistingDirectory(self, QApplication.translate("DFF_ConfigureDFF", "Choose Your Directory For Extraction", None, QApplication.UnicodeUTF8),  "/home")
        if (sDirPath) :
            self.valueWorkspace.setText(sDirPath)
