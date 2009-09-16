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

from PyQt4.QtCore import QThread, SIGNAL, QVariant, QWaitCondition
from ui.gui.utils.standardItem import DFF_StandardItem
from PyQt4.QtGui import QApplication, QIcon, QStandardItemModel, QStandardItem
from PyQt4.Qt import *
from ui.gui.utils.utils import DFF_Utils
from time import sleep

class ListThread(QThread):
  def __init__(self, ListView, ListModel):
    QThread.__init__(self)  
    self.mutex = QMutex()
    self.condition = QWaitCondition()
    self.ListView = ListView	
    self.ListModel = ListModel
    self.restart = False
    self.abort = False	

  def __del__(self):
    self.mutex.lock()
    self.abort = True
    self.condition.wakeOne()
    self.mutex.unlock()
    self.wait()				

  def renderList(self, list, nodeParent):
    locker = QMutexLocker(self.mutex)	
    self.list = list 
    self.nodeParent = nodeParent
    if not self.isRunning():
	self.start(QThread.LowPriority)
    else:
        self.restart = True
        self.condition.wakeOne()
 
  def run(self):
     while(True):
       self.mutex.lock()
       self.currentNodeDir = self.nodeParent
       list = self.list
       self.mutex.unlock()
       for itemVFS in list:
       	    items = []
	    if self.restart:
		break
	    if self.abort:
		return 
            items.append(DFF_StandardItem(itemVFS))
            items[0].setText(QApplication.translate("MainWindow", str(itemVFS.name), None, QApplication.UnicodeUTF8))
            if not itemVFS.next.empty() or not itemVFS.is_file:
#XXX
                if not itemVFS.is_file :
                    icon = ":dff_folder.png"
                else :
                    icon = ":dff_folder.png"
#                    items[0].setIcon(QIcon(":dff_partition.png"))
            else :
                    icon = ":file.png"
            items.append(QStandardItem())
            if itemVFS.is_file == 0 :
                items[1].setText(QApplication.translate("ListModel", "", None, QApplication.UnicodeUTF8))
            else :
                items[1].setText(DFF_Utils.formatSize(itemVFS.attr.size))
            items.append(QStandardItem(""))
            items.append(QStandardItem(""))
            items.append(QStandardItem(""))
            items.append(QStandardItem(""))
            time = itemVFS.attr.time
            for i in time :
                items[self.ListModel.timeHeader[str(i)]].setText(str(time[i].get_time()))
	    items[5].setText(itemVFS.fsobj.name)           
	    for i in range(0, 6):
              items[i].setEditable(False)
              items[i].setCheckable(False)
            self.emit(SIGNAL("addItem"), items, icon)
	    sleep(0.001)	
       if not self.restart:
          self.emit(SIGNAL("resizeList"))
       self.mutex.lock()
       if not self.restart:
          self.condition.wait(self.mutex)
       self.restart = False
       self.mutex.unlock()		
