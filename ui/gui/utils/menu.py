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

from PyQt4.QtGui import QMenu
from PyQt4.QtCore import SIGNAL, SLOT

from api.loader import *

from action import DFF_Action

from ui.gui.utils.utils import DFF_Utils

class MenuTags():
   def __init__(self, parent, mainWindow, selectItem = None):
       """ Init menus"""
       self.parent = parent
       self.mainWindow = mainWindow
       self.selectItem = selectItem	
       self.Load()
       self.parent.menuModules.connect(self.parent.menuModules, SIGNAL("aboutToShow()"), self.refreshQMenuModules)
 
   def Load(self):   
       self.listMenuAction = []
       setags = DFF_Utils.getSetTags()
       for tags in setags:
          self.listMenuAction.append(self.parent.menuModules.addMenu(MenuModules(self.parent, self.mainWindow, tags, self.selectItem)))
        
   def refreshQMenuModules(self):
        setags = DFF_Utils.getSetTags()
	for menu in self.listMenuAction:
	   self.parent.menuModules.removeAction(menu)
	self.Load()
   
class MenuModules(QMenu):
    def __init__(self, parent, mainWindow, tags, selectItem = None):
        QMenu.__init__(self, tags,  parent)
	self.tags = tags       
        self.__mainWindow = mainWindow
        self.callbackSelected = selectItem
        self.loader = loader.loader()
        self.Load()
 
    def Load(self):
        modules = self.loader.modules
        actions = []
        for mod in modules :
	     m = modules[mod]
	     try :
	       if m.tags == self.tags:
                 actions.append(DFF_Action(self, self.__mainWindow, mod, self.tags))
             except AttributeError:
		pass
        for i in range(0,  len(actions)) :
            if actions[i].hasOneArg :
                self.addAction(actions[i])
        self.addSeparator()
        for i in range(0,  len(actions)) :
            if not actions[i].hasOneArg :
                self.addAction(actions[i])
                
    def refresh(self):
        self.clear()
        self.Load()

        
