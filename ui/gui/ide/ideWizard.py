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

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from ideWizardPages import *

class ideWizard(QWizard):
    def __init__(self, mainWindow, title):
        super(ideWizard,  self).__init__(mainWindow)
        self.main = mainWindow
        self.setWindowTitle("Integrated Development Environment Wizard")

        self.setOrder()        
        self.setPages()

    def setOrder(self):
        self.porder = {}
        self.porder['INTRO'] = 0
        self.porder['AUTH'] = 1
        #self.porder['COC'] = 2


    def setPages(self):
        self.PIntro = WIntroPage(self)
        self.PAuth = WAuthorPage(self)
        #self.PCOC = WCOCPage(self)

        self.setPage(self.porder['INTRO'], self.PIntro)
        self.setPage(self.porder['AUTH'], self.PAuth)
        #self.setPage(self.porder['COC'], self.PCOC)
        
        
    def nextId(self):
        current = self.currentId()
        if current == self.porder['INTRO']:
            return self.porder['AUTH']
        else:
            return -1

    def getIntro(self):
        #return list of informations
        pass
