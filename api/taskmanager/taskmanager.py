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
#  Solal J. <sja@digital-forensic.org>
#

from api.taskmanager.scheduler import sched 
from api.taskmanager.processus import *
from api.env import *
from api.loader import *
from api.exceptions.libexceptions import *
import threading

class TaskManager:
  class __TaskManager():
    def __init__(self):
      self.loader = loader.loader()
      self.sched = sched
      self.lprocessus = []
      self.npid = 0
      self.env = env.env() 
      self.current_proc = None

    def add(self, cmd, args, exec_flags):
      task = self.loader.modules[cmd] 
      proc = Processus(task, self.npid, args, exec_flags)
      self.lprocessus.append(proc)
      self.npid += 1
      if "thread" in exec_flags:
        sched.enqueue(proc)
      else:
	try :
           if "gui" in proc.mod.flags and not "console" in proc.mod.flags:
             print "This script is gui only"
	     self.lprocessus.remove(proc)
	     return 
	except AttributeError:
	      pass
	thread = threading.Thread(target = proc.launch)
	self.current_proc = proc
        thread.start()
	while (thread.isAlive()):
	  pass
	self.current_proc = None
       	try :
          for type, name, val in self.env.get_val_map(proc.res.val_m):
	        print name + ":" +"\n"  + val
        except AttributeError:
          pass
#        return proc.res
  __instance = None

  def __init__(self):
    if TaskManager.__instance is None:
       TaskManager.__instance = TaskManager.__TaskManager()

  def __setattr__(self, attr, value):
	setattr(self.__instance, attr, value)
  def __getattr__(self, attr):
	return getattr(self.__instance, attr) 

  def add(self, cmd, args, exec_flags):
       return self.__instance.add(cmd, args, exec_flags)
