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

import sys
from api.module.script import *
from api.vfs import *
from api.module.module import *

from PyQt4.QtCore import QSize, SIGNAL
from PyQt4.QtGui import QWidget, QVBoxLayout, QIcon, QMessageBox
from ui.gui.utils.utils import DFF_Utils

from Heditor import Heditor

try :
  import nceditor
except ImportError:
  pass

class ViewerHexa(QWidget, Script):
    def __init__(self):
        Script.__init__(self, "hexedit")
        self.type = "hexedit"
#        self.icon = ":hexedit.png"
        
    def start(self, args) :
        self.args = args

    def c_display(self):
        node = self.args.get_node("file")
	try:
          nceditor.start(node)
	except NameError:
	  print "This functionality is not available on your operating system"	

    def g_display(self):
        QWidget.__init__(self)
        self.vlayout = QVBoxLayout(self)
        self.widget = Heditor(self)
        self.vlayout.addWidget(self.widget)
        node = self.args.get_node("file")
        self.name = "hexedit " + str(node.name)        
        if node.attr.size > 0:
          self.widget.init(node)
        else:
          msg = QMessageBox(QMessageBox.Critical, "Hexadecimal viewer", "Error: File is empty", QMessageBox.Ok)
          msg.exec_()
          
        
    def updateWidget(self):
        pass

    def initCallback(self):
        pass 
    
    def refresh(self):
        pass 

class hexeditor(Module):
  def __init__(self):
    Module.__init__(self, "hexedit", ViewerHexa)
    self.conf.add("file", "node")
    self.tags = "viewer"

