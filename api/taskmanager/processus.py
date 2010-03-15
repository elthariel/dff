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

from api.module.module import *
from api.vfs.libvfs import *
from api.taskmanager.scheduler import *
from api.type.libtype import *
from api.vfs import *

class Processus(Script):
  def __init__(self, mod, pid, args, exec_flags):
    self.vfs = vfs.vfs()
    self.mod = mod
    self.inst = mod.create()
    self.exec_flags = exec_flags
    self.state = "wait"
    self.pid =  pid 
    self.args = args
    self.stream = Queue()

  def launch(self):
    self.state = "exec"
    try :
      self.start(self.args)
      try :	
        if "gui" in self.exec_flags:
          if "gui" in self.mod.flags:
             for func in sched.event_func["add_qwidget"]:
	        func(self)
	if "console" in self.exec_flags:
	  if "console" in self.mod.flags:
		self.c_display()  
      except AttributeError:
	pass	
    except :
	 error = sys.exc_info()
         self.error(error)
    self.error()	

  def error(self, trace = None):
    if trace:
	 err_type, err_value, err_traceback = trace 
	 if issubclass(err_type, envError):
	    self.res.add_const("error", err_value.error)
            return
         elif issubclass(err_type, vfsError):
	    self.res.add_const("error", err_value.error)
	    return
 	 self.res.add_const("error", "Error in execution")
         err_typval = traceback.format_exception_only(err_type, err_value)
	 res = ""
         for err in err_typval:
            res += err
	 self.res.add_const("error type", err)
	 err_trace =  traceback.format_tb(err_traceback)
         for err in err_trace:
	   res += err
	   self.res.add_const("error trace", res)
           self.state = "fail"
         return
    try :
       if self.AddNodes():
         self.state = "wait"
	 return 
    except AttributeError:
	pass
    if "gui" in self.exec_flags and "gui" in self.mod.flags:
      self.state = "wait"
    else:
      self.state = "finish"

  def __getattr__(self, attr):
     return  getattr(self.inst, attr)
