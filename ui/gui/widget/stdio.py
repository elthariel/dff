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
#  Solal Jacob <sja@digital-forensic.org>
#

from PyQt4.QtGui import QDockWidget, QAction, QApplication, QTextEdit, QWidget, QHBoxLayout, QTabWidget
from PyQt4.QtCore import Qt, SIGNAL, QThread
from ui.redirect import RedirectIO
import os, sys


class CIO(QThread):
  def __init__(self, IOout, fd, sig):
      QThread.__init__(self)
      self.ioOut = IOout
      self.pipe = os.pipe()
      os.close(fd)
      os.dup2(self.pipe[1], fd)   
      self.sig = sig	 

  def run(self):
      while (True):
        try :
  	  buff = os.read(self.pipe[0], 4096)
          self.ioOut.emit(SIGNAL(self.sig), buff)
        except OSError:
	  pass
   
class IO(QDockWidget):
   def __init__(self, mainWindow):
	super(IO, self).__init__()
	self.__mainWindow = mainWindow
	self.addAction()
	self.configure()
	self.io = self.initIO()
	self.sigout = "IOOUTputtext"
        self.connect(self, SIGNAL(self.sigout), self.puttextout)
	self.sigerr = "IOERRputtext"
        self.connect(self, SIGNAL(self.sigerr), self.puttexterr)
	self.redirect = RedirectIO(self)
	self.cioout = CIO(self, sys.__stdout__.fileno(), self.sigout)     
	self.cioout.start()
	self.cioerr = CIO(self, sys.__stderr__.fileno(), self.sigerr)     
	self.cioerr.start()

   def configure(self):
        self.setAllowedAreas(Qt.AllDockWidgetAreas)
        self.setObjectName("dockWidgetBrowser")
        self.setWindowTitle(QApplication.translate("Log", "Log", None, QApplication.UnicodeUTF8))
 
   def addAction(self):
        self.__action = QAction(self)
        self.__action.setCheckable(True)
        self.__action.setChecked(True)
        self.__action.setObjectName("actionCoreInformations")
        self.__action.setText(QApplication.translate("MainWindow", "Log", None, QApplication.UnicodeUTF8))
        self.__mainWindow.menuWindow.addAction(self.__action)
        self.connect(self.__action,  SIGNAL("triggered()"),  self.changeVisibleInformations)
     
   def changeVisibleInformations(self):
        if not self.isVisible() :
            self.setVisible(True)
            self.__action.setChecked(True)
        else :
            self.setVisible(False)
            self.__action.setChecked(False)

   def visibilityChanged(self,  bool):
        if not self.isVisible() :
            self.__action.setChecked(False)
        else :
            self.__action.setChecked(True)

   def initIO(self):
        self.iowidget = QWidget(self)        
        self.layout = QHBoxLayout(self.iowidget)
        self.iowidget.setLayout(self.layout)
        self.tabwidget = QTabWidget(self)
        self.tabwidget.setElideMode(Qt.ElideRight)

	self.textOut = QTextEdit(self)
	self.textOut.setReadOnly(1)
	self.textOut.name = "output"
        self.setWidget(self.textOut)
	self.tabwidget.addTab(self.textOut, "Output")

	self.textErr = QTextEdit(self)
	self.textErr.setReadOnly(1)
	self.textErr.name = "error"
        self.setWidget(self.textErr)
	self.tabwidget.addTab(self.textErr, "Error")
	
	self.layout.addWidget(self.tabwidget)
        self.setWidget(self.iowidget)

   def puttextout(self, text):
 	self.textOut.append(text)

   def puttexterr(self, text):
        self.textErr.append(text)
