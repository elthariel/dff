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

class WIntroPage(QWizardPage):
    def __init__(self, parent):
        QWizardPage.__init__(self, parent)
        self.setInformations()
        self.createShape()

    def setInformations(self):
        self.setTitle("Script Informations")
        self.setSubTitle("Fill all script information such as name, type and location")

    def createShape(self):
        self.grid = QGridLayout()
        
        ##
        lname = QLabel("Script name:")
        self.name = QLineEdit()

        ##
        ltype = QLabel("Select script type:")
        self.type_script = QRadioButton("Script")
        self.type_graphical = QRadioButton("Graphical")
        self.type_driver = QRadioButton("Driver")
        self.type_script.setChecked(True)
        
        ##
        lpath = QLabel("Select script location:")
        self.path = QLineEdit()
        self.brwButton = QPushButton("Browse")
        self.connect(self.brwButton, SIGNAL("clicked()"),  self.browseBack)

        self.path = QLineEdit()
        self.path.setReadOnly(True)
        
        ## Register Fields
        self.registerField("typeS", self.type_script)
        self.registerField("typeG", self.type_graphical)
        self.registerField("typeD", self.type_driver)
        self.registerField("name*", self.name)
        self.registerField("path*", self.path)

        #Draw shape
        self.grid.addWidget(lname, 0, 0)
        self.grid.addWidget(self.name, 1, 0)

        self.grid.addWidget(ltype, 3, 0)
        self.grid.addWidget(self.type_script, 4, 0)
        self.grid.addWidget(self.type_graphical, 5, 0)
        self.grid.addWidget(self.type_driver, 6, 0)

        self.grid.addWidget(lpath, 8, 0)
        self.grid.addWidget(self.path, 9, 0)
        self.grid.addWidget(self.brwButton, 9, 1)
        
        self.setLayout(self.grid)

    def browseBack(self):
        dirName = QFileDialog.getExistingDirectory(self, QApplication.translate("MainWindow", "Location", None, QApplication.UnicodeUTF8))
        self.path.setText(dirName)



class WAuthorPage(QWizardPage):
    def __init__(self, parent):
        QWizardPage.__init__(self, parent)
        self.setInformations()
        self.createShape()
        self.setFinalPage(True)

    def setInformations(self):
        self.setTitle("Author Informations")
        self.setSubTitle("Fill all author's informations in order to complete header")

    def createShape(self):
        self.grid = QGridLayout()
        
        ##
        lfname = QLabel("Author's first name:")
        self.auth_fname = QLineEdit()

        ##
        llname = QLabel("Author's last name:")
        self.auth_lname = QLineEdit()
        
        lmail = QLabel("Author's electronic mail:")
        self.auth_mail = QLineEdit()
        
        ## Register Fields
        self.registerField("authFName*", self.auth_fname)
        self.registerField("authLName*", self.auth_lname)
        self.registerField("authMail*", self.auth_mail)

        #Draw shape
        self.grid.addWidget(lfname, 0, 0)
        self.grid.addWidget(self.auth_fname, 1, 0)

        self.grid.addWidget(llname, 2, 0)
        self.grid.addWidget(self.auth_lname, 3, 0)

        self.grid.addWidget(lmail, 4, 0)
        self.grid.addWidget(self.auth_mail, 5, 0)

        self.setLayout(self.grid)

    def browseBack(self):
        dirName = QFileDialog.getExistingDirectory(self, QApplication.translate("MainWindow", "Location", None, QApplication.UnicodeUTF8))
        self.path.setText(dirName)
