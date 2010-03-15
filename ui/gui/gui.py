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

import sys

from PyQt4.QtGui import QApplication, QSplashScreen, QPixmap
from PyQt4.QtCore import Qt

from mainWindow import DFF_MainWindow
from configuration.Translator import DFF_Translator
from api.loader.loader import loader

# import Resource QT
import gui_rc

class gui():
    def __init__(self):
        """Launch GUI"""
        #translator = DFF_Translator()
        self.app = QApplication(sys.argv)
        #app.installTranslator(translator)
        pixmap = QPixmap(":splash.png")
        self.splash = QSplashScreen(pixmap, Qt.WindowStaysOnTopHint)
        self.splash.setMask(pixmap.mask()) 

    def launch(self, modPath):
        self.splash.show()
        self.loader = loader()
        self.loader.do_load(modPath, self.splash.showMessage)
        mainWindow = DFF_MainWindow(self.app)
        mainWindow.show()

        self.splash.finish(mainWindow)
        sys.exit(self.app.exec_())

