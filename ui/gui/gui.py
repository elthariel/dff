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

from PyQt4.QtGui import QApplication

from mainWindow import DFF_MainWindow
from configuration.Translator import DFF_Translator

# import Resource QT
import gui_rc

class gui():
    def __init__(self):
        """Launch GUI"""
        #translator = DFF_Translator()
    
        app = QApplication(sys.argv)
        #app.installTranslator(translator)
        mainWindow = DFF_MainWindow(app)
        mainWindow.show()
        sys.exit(app.exec_())
