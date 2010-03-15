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

from PyQt4.QtGui import QComboBox

class StringComboBox(QComboBox):
    def __init__(self, parent):
        QComboBox.__init__(self,  parent)
        
    def addPathAndSelect(self, path):
        for i in range(0, self.count()):
            if self.itemText(i) == path :
                self.setCurrentIndex(i)
                return False
        self.addItem(path)
        self.setCurrentIndex(self.count() - 1)
        return True
    
    def addPath(self, path):
        for i in range(0, self.count()):
            if self.itemText(i) == path :
                return False
        self.addItem(path)
        return True
        

