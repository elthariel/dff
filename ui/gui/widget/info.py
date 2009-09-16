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
#  Solal Jacob <sja@digital-forensic.org>
#
 
import time
from PyQt4.QtGui import QAction, QApplication, QDockWidget, QIcon,  QHBoxLayout, QPushButton, QTabWidget, QTreeWidget, QTreeWidgetItem, QWidget, QDialog, QGridLayout, QLabel, QComboBox, QMessageBox
from PyQt4.QtCore import QRect, QSize, Qt, SIGNAL, QTimer, QThread

from api.loader import *
from api.env import *
from api.taskmanager.taskmanager import *

from ui.gui.utils.utils import DFF_Utils
from ui.gui.wrapper.connectorCallback import *

class Info(QDockWidget):
    def __init__(self, mainWindow):
        super(Info,  self).__init__()
        self.__mainWindow = mainWindow
        self.loader = loader.loader()
        self.env = env.env()
        self.tm = TaskManager()
        self.addAction()
        self.configure()
        self.g_display()
        self.initCallback()
        self.Load()

    def configure(self):
        self.setAllowedAreas(Qt.AllDockWidgetAreas)
        self.setObjectName("dockWidgetBrowser")
        self.setWindowTitle(QApplication.translate("Info", "Info", None, QApplication.UnicodeUTF8))
    
    def addAction(self):
        self.__action = QAction(self)
        self.__action.setCheckable(True)
        self.__action.setChecked(True)
        self.__action.setObjectName("actionCoreInformations")
        self.__action.setText(QApplication.translate("MainWindow", "Info", None, QApplication.UnicodeUTF8))
        self.__mainWindow.menuWindow.addAction(self.__action)
        self.connect(self.__action,  SIGNAL("triggered()"),  self.changeVisibleInformations)
     
    def changeVisibleInformations(self):
        if not self.isVisible() :
            self.setVisible(True)
            self.__action.setChecked(True)
        else :
            self.setVisible(False)
            self.__action.setChecked(False)
        
    def g_display(self):
        self.Info = QWidget(self)
        self.layout = QHBoxLayout(self.Info)
        self.Info.setLayout(self.layout)
        self.tabWidget = QTabWidget(self)
        self.tabWidget.setElideMode(Qt.ElideRight)
        self.initTreeProcess()
        self.initTreeModule()
        self.initTreeEnv()
        self.layout.addWidget(self.tabWidget)
        self.setWidget(self.Info)

    def initCallback(self):
        self.connect(self, SIGNAL("visibilityChanged(bool)"), self.visibilityChanged)
        self.timer = QTimer(self)
	self.connect(self.timer, SIGNAL("timeout()"), self.refresh)
        self.timer.start(2000)      

    def visibilityChanged(self,  bool):
        if not self.isVisible() :
            self.__action.setChecked(False)
        else :
            self.__action.setChecked(True)

    def Load(self):
        self.LoadInfoProcess()
        self.LoadInfoModules()
        self.LoadInfoEnv()
	pass

    def refresh(self):
	self.LoadInfoProcess() 
        self.LoadInfoModules() 
	self.LoadInfoEnv()
	pass

    def deleteInfos(self):
        self.deleteInfoProcess()
        self.deleteInfoModule()
        self.deleteInfoEnv()

#MODULES
 
    def initTreeModule(self):
        self.treeModule = QTreeWidget(self)
        self.treeModule.setColumnCount(3)
        headerLabel = [QApplication.translate("Info", "Name", None, QApplication.UnicodeUTF8),  
        QApplication.translate("Info", "Key", None, QApplication.UnicodeUTF8), 
        QApplication.translate("Info", "Value", None, QApplication.UnicodeUTF8),
        QApplication.translate("Info", "Info", None, QApplication.UnicodeUTF8),
	QApplication.translate("Info", "Type", None, QApplication.UnicodeUTF8)]
        self.treeModule.setHeaderLabels(headerLabel)
        self.treeModule.setAlternatingRowColors(True)
        self.tabWidget.addTab(self.treeModule, "Modules")
        self.itemModuleDic = dict()
	self.itemListArgDic = dict()
	self.itemArgDic = dict()
	self.itemListResDic = dict()
	self.itemResDic = dict()

    def LoadInfoModules(self):
        modules = self.loader.modules
        for mod in modules :
	  try  :
	    itemModule = self.itemModuleDic[mod]
	  except KeyError:
	    itemModule = QTreeWidgetItem(self.treeModule)
	    self.itemModuleDic[mod] = itemModule
	    itemModule.setText(0, str(mod))
	    itemConfig = QTreeWidgetItem(itemModule)
	    itemConfig.setText(0, "Config")
	    cdesc = modules[mod].conf.descr_l
	    for key in cdesc:
	       itemConfKey = QTreeWidgetItem(itemConfig) 
	       itemConfKey.setText(0, "var")	
	       itemConfKey.setText(1, key.name)
	       itemConfKey.setText(4, key.type)
	       if len(key.description):
	         itemConfKey.setText(3, key.description)
	    for type, name, val, _from in self.env.get_val_list(modules[mod].conf.val_l): 
	       itemConfKey = QTreeWidgetItem(itemConfig)
	       itemConfKey.setText(0, "const")
	       itemConfKey.setText(1, name)
	       itemConfKey.setText(2, val)
	       itemConfKey.setText(4, type)	
	  for proc in self.tm.lprocessus:
	    if proc.mod.name == mod:
	     try :
	        itemListArg = self.itemListArgDic[mod]	
	     except KeyError:
	        itemListArg = QTreeWidgetItem(itemModule)
	        self.itemListArgDic[mod] = itemListArg
	        itemListArg.setText(0, "Arg")
	     for type, name, val in self.env.get_val_map(proc.args.val_m):
               try:
	         itemArgKey = self.itemArgDic[(type, name, val)]  		
	       except KeyError:
	         itemArgKey = QTreeWidgetItem(itemListArg)    
	         self.itemArgDic[(type, name, val)] = itemArgKey	
	         itemArgKey.setText(1, name)
	         itemArgKey.setText(2, val)
	         itemArgKey.setText(4, type)
	     try :
	        itemListRes = self.itemListResDic[mod]	
	     except KeyError:
	        itemListRes = QTreeWidgetItem(itemModule)
	        self.itemListResDic[mod] = itemListRes
	        itemListRes.setText(0, "Results")
	     for type, name, val in self.env.get_val_map(proc.res.val_m):
               try:
	         itemResKey = self.itemResDic[(type, name, val)]  		
	       except KeyError:
	         itemResKey = QTreeWidgetItem(itemListRes)    
	         self.itemResDic[(type, name, val)] = itemResKey	
	         itemResKey.setText(1, name)
	         itemResKey.setText(2, val)
	         itemResKey.setText(4, type)
	          		    	 	    		
    def deleteInfoModule(self):
	self.treeModule.clear()

#ENV
    def initTreeEnv(self):
        self.treeEnv = QTreeWidget(self)
        self.treeEnv.setColumnCount(3)
        headerLabel = [QApplication.translate("Info", "Key", None, QApplication.UnicodeUTF8), 
        QApplication.translate("Info", "Type", None, QApplication.UnicodeUTF8), 
        QApplication.translate("Info", "Value", None, QApplication.UnicodeUTF8), 
        QApplication.translate("Info", "From", None, QApplication.UnicodeUTF8)]
        self.treeEnv.setHeaderLabels(headerLabel)
        self.treeEnv.setAlternatingRowColors(True)
        self.tabWidget.addTab(self.treeEnv, "Environment")
	self.envItemDic = dict()
	self.envConfKeyDic = dict()
	self.envValKeyDic = dict()
 
    def LoadInfoEnv(self):
        db = self.env.vars_db
        for key in db : 
          try :
	    (itemEnv, itemVar, itemValues) = self.envItemDic[key]
	  except KeyError:
	    itemEnv = QTreeWidgetItem(self.treeEnv)
	    itemEnv.setText(0, key)
	    itemVar = QTreeWidgetItem(itemEnv)
            itemVar.setText(0, "var")
	    itemValues = QTreeWidgetItem(itemEnv)
	    self.envItemDic[key] = (itemEnv, itemVar, itemValues)
	  cdesc = db[key].descr_l
	  for vk in cdesc:
	    try:
	      itemConfKey = self.envConfKeyDic[(vk.type, vk._from)]	     
	    except KeyError:
	      itemConfKey = QTreeWidgetItem(itemVar) 
	      self.envConfKeyDic[(vk.type, vk._from)] = itemConfKey
	      itemConfKey.setText(1, vk.type)
	      itemConfKey.setText(3, vk._from)
          itemValues.setText(0, "values")
	  for type, name, val, _from in self.env.get_val_list(db[key].val_l): 
	   try:
	      itemValKey = self.envValKeyDic[(type, _from, val)]
	   except:
	      itemValKey = QTreeWidgetItem(itemValues)
              self.envValKeyDic[(type, _from, val)] = itemValKey
	      itemValKey.setText(1, type)
	      itemValKey.setText(2, val)
	      itemValKey.setText(3, _from)

    def deleteInfoEnv(self):
        self.treeEnv.clear()

#PROCESSUS

    def initTreeProcess(self):
        self.treeProcess = QTreeWidget(self)
        self.treeProcess.setColumnCount(3)
        headerLabel = [QApplication.translate("Info", "PID", None, QApplication.UnicodeUTF8),  
        QApplication.translate("Info", "Name", None, QApplication.UnicodeUTF8), QApplication.translate("Info", "State", None, QApplication.UnicodeUTF8), 
        QApplication.translate("Info", "Info", None, QApplication.UnicodeUTF8)] 
        self.treeProcess.setHeaderLabels(headerLabel)
        self.treeProcess.setAlternatingRowColors(True)
        self.tabWidget.addTab(self.treeProcess, "Task Manager")
 	self.connect(self.treeProcess, SIGNAL("itemDoubleClicked(QTreeWidgetItem*,int)"), self.procClicked)
	self.procItemDic = dict()
        self.procChildItemDic = dict()

    def procClicked(self, item, column):
	dial = procMB(self, item.text(0))
	dial.exec_()

    def LoadInfoProcess(self):
	lproc = self.tm.lprocessus
	for proc in lproc:
	  try:
	    item = self.procItemDic[proc]
	  except KeyError:
	    item = QTreeWidgetItem(self.treeProcess)
	    self.procItemDic[proc] = item
	    item.setText(0, str(proc.pid))
	    item.setText(1, str(proc.name))
          if item.text(2) != str(proc.state):
            item.setText(2, str(proc.state))
          if item.text(3) != str(proc.stateinfo):
	    item.setText(3, str(proc.stateinfo))

    def deleteInfoProcess(self):
        self.treeProcess.clear()
         
            
class procMB(QMessageBox):
  def __init__(self, parent,  pid):
   QMessageBox.__init__(self, parent)
   self.cb = ConnectorCallback() 
   self.tm = TaskManager()
   self.pid = pid
   self.env = env.env()
   res = ""
   for proc in self.tm.lprocessus:
     if str(proc.pid) == self.pid:
	try :
	  res += "\nResult:\n"
          for type, name, val in self.env.get_val_map(proc.res.val_m):
	        res += name + ": " + val
        except AttributeError:
              pass
        self.cb.emit(SIGNAL("strResultView"), proc)
   self.setText(res)
