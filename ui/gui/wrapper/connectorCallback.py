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
from Queue import *
from PyQt4.QtCore import QObject, Qt, SIGNAL
from PyQt4.QtGui import QDockWidget, QTextEdit

from api.taskmanager import *
from api.vfs.libvfs import *

from ui.gui.utils.utils import DFF_Utils

class DFFText(QTextEdit):
  def __init__(self, proc):
      QTextEdit.__init__(self)
      self.setReadOnly(1)
      self.icon = 0
      self.name = proc.name 
      self.type = "autogen"
      self.proc = proc 
      proc.widget = self
      self.connect(self, SIGNAL("puttext"), self.puttext)

  def puttext(self, text):
      self.append(text)		

class ConnectorCallback():
    class __ConnectorCallback(QObject):
        def __init__(self, mainWindow):
            QObject.__init__(self)
            self.__mainWindow = mainWindow
            self.sched = scheduler.sched
	    self.vfs = VFS.Get()            
            self.initSignals()
            self.initCallback()

        def initCallback(self):
            self.sched.set_callback("refresh_tree", self.refreshNode)
            self.sched.set_callback("add_qwidget", self.qwidgetResult)
            self.sched.set_callback("add_str", self.strResult)
	    self.vfs.set_callback("refresh_tree", self.refreshNode)
            
        def initSignals(self):
            self.connect(self, SIGNAL("qwidgetResultView"), self.qwidgetResultView)
            self.connect(self, SIGNAL("strResultView"), self.strResultView)
        
        def refreshNode(self, node):
            self.emit(SIGNAL("reload"))

        def qwidgetResult(self, qwidget):
            self.emit(SIGNAL("qwidgetResultView"), qwidget)
            
        def qwidgetResultView(self, proc):
	    try :
              proc.inst.g_display()
              self.addDockWidget(proc.inst)
	    except :
		trace = sys.exc_info()
	        proc.error(trace)
            proc.inst.updateWidget()
	    proc.error() 

        def strResult(self, proc):
	   self.emit(SIGNAL("strResultView"), proc)
 

        def strResultView(self, proc):
	   widget = DFFText(proc)
	   try :
	      res = ''
	      txt = proc.stream.get(0)
	      res += txt	
	      while txt:
	        txt = proc.stream.get(0)   
		res += txt
	   except Empty:
	      pass   
	   if res and res != '':
	     widget.emit(SIGNAL("puttext"), res)
             self.addDockWidget(widget)

        def addDockWidget(self, widget):
            dockwidget = QDockWidget(self.__mainWindow)
            dockwidget.setAllowedAreas(Qt.AllDockWidgetAreas)
            dockwidget.setWindowTitle(widget.name)
            dockwidget.setWidget(widget)
            QObject.connect(dockwidget, SIGNAL("resizeEvent"), widget.resize)
            self.__mainWindow.addNewDockWidgetTab(Qt.RightDockWidgetArea, dockwidget)

    instance = None
    
    def __init__(self,  mainWindow = None):
        if not ConnectorCallback.instance :
            if mainWindow :
                ConnectorCallback.instance = ConnectorCallback.__ConnectorCallback(mainWindow)
            else :
                print "Class ConnectorCallback don't create. Need mainWindow for first instanciation. Thanks"
    
    def __getattr__(self, attr):
        return getattr(self.instance, attr)

    def __setattr__(self, attr, val):
        return setattr(self.instance, attr, val)
