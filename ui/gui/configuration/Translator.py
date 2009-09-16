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

import sys
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QTranslator
# Import Singleton for CONF
from Config import DFF_Conf

class DFF_Translator(QTranslator):
    __instance = None
     
    def __new__(cls): 
        if cls.__instance is None:
            cls.__instance = QTranslator.__new__(cls)
        return cls.__instance
    
    def __init__(self):
        QTranslator.__init__(self)
        self.Conf = DFF_Conf()
        self.loadLanguage()
        
    def loadLanguage(self):
        if self.Conf.language == "FR" :
            return self.load(":Dff_fr")
        else:
            return self.load(":Dff_en")
