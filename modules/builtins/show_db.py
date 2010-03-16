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
from api.module.script import *
from api.env import *
from api.module.module import *

class SHOW_DB(Script):
  def __init__(self):
     Script.__init__(self, "show_db")
     self.env = env.env() 

  def get_dbinfo(self, key):
      res = ""
      try :
        desc = self.env.vars_db[key].descr_l
        val = self.env.vars_db[key].val_l
      except IndexError:
        return "Key " + key + " not found"
      res +=  key + "\n"
      res += "\tvar :\n"
      for d in desc :
        res+=  "\t\t" + "" + d.type + " from " + d._from + "\n" 
      res += "\tvalues :\n"
      for v in val:
        if v.type == "int":
         res+= "\t\t"    + v.type  + "=" + str(v.get_int()) + " from " + v._from + "\n"
        elif v.type == "string":
         res+= "\t\t" +  v.type  + "=" + v.get_string() + " from " + v._from + "\n"
        elif v.type == "node":
	 node = v.get_node() 
	 if node: 
           res += "\t\t" + v.type  + "=" + node.path + "/" + node.name + " from " + v._from + "\n"
	elif v.type == "path":
	   res += "\t\t" + v.type  + "=" + v.get_path().path + " from " + v._from + "\n" 
      return res

  def start(self, args):
    res = "Variable DB\n"
    try :
      key = args.get_string('key')
      res += self.get_dbinfo(key)
    except envError, e:
     for i in self.env.vars_db:
	res += self.get_dbinfo(i)
    print res

class show_db(Module):
  def __init__(self):
    """Show DFF Data-Base from a key-centric view"""
    Module.__init__(self, "show_db", SHOW_DB)
    self.tags = "builtins"
    self.conf.add("key", "string", True)
