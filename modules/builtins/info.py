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

from api.vfs import *
from api.env import *
from api.module.script import *
from api.loader import *
from api.module.module import *
from api.taskmanager.taskmanager import *

class INFO(Script):
  def __init__(self):
    Script.__init__(self, "info")
    self.loader = loader.loader()
    self.tm = TaskManager()
    self.lproc = self.tm.lprocessus
    self.env = env.env()

  def show_config(self, conf):
    dlist = conf.descr_l
    res = ""
    for i in dlist:
     if len(i.info):
       res += "\n\t" + i.type + "\t" + i.name  +  "(" + i.info  + ")"
     else:
       res += "\n\t" + i.type + "\t" + i.name
    for type, name, val, _from in self.env.get_val_list(conf.val_l):
      res += "\n\t" + type + "\t" + name + "=" + val
    return res

  def show_arg(self, arg):
    res = ""
    for type, name, val in self.env.get_val_map(arg.val_m):
      res += "\n\t" + type + "\t" + name + "=" + val
    return res

  def show_res(self, result):
    res = ""
    for type, name, val in self.env.get_val_map(result.val_m):
      res += "\n\t" + type + "\t" + name + "=" + val
    return res
  
  def c_display(self):
     print self.info  

  def getmodinfo(self, mname):
     self.info +=  "\n" +  mname + "\n\tConfig: \t" + self.show_config(self.modl[mname].conf)
     for proc in self.lproc:
       if proc.mod.name == mname:
     	  self.info += "\n\tArguments: \t" + self.show_arg(proc.args)
          self.info += "\n\tResults: \t" + self.show_res(proc.res)
 
  def start(self, args):
    self.modl = self.loader.modules
    self.info = ""
    try :
      mname = args.get_string('modules')	
      self.getmodinfo(mname)
    except envError, e:
      for mname in self.modl:
	 self.getmodinfo(mname)

class info(Module):
  """Show info on loaded drivers: configuration, arguments, results
  """
  def __init__(self):
    Module.__init__(self, "info", INFO)
    self.tags = "builtins"
    self.conf.add("modules", "string", True) 
