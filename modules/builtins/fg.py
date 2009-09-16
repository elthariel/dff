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

from api.vfs import *
from api.module.module import *
from api.taskmanager.taskmanager import *
from api.module.script import *

class FG(Script):
  def __init__(self):
    Script.__init__(self, "fg")
    self.tm = TaskManager()
    	
  def start(self, args):	
    self.lprocessus = self.tm.lprocessus
    jobs = args.get_int("pid")
    for proc in self.lprocessus:
      if jobs == proc.pid:
       print "Displaying processus: " + str(proc.pid) + " name:" + str(proc.name) + " state:" + str(proc.state) + "\n"
       try :
	  text = self.lprocessus[jobs].stream.get(0)
#bufferiser en cas de gros output ?
	  while text:
	    print text
	    text = self.lprocessus[jobs].stream.get(0)
       except Empty:
	 pass
       #if is finish ? 	 	
       try :
	 for type, name, val in self.env.get_val_map(proc.res.val_m):
	     print name + ":" + "\n" + val
       except AttributeError:
	  pass

class fg(Module):
  def __init__(self):
   Module.__init__(self, "fg", FG)
   self.conf.add("pid", "int")
   self.tags = "builtins"
   self.flags = ["console"]
