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

from api.vfs.libvfs import *
from api.env import *
from modules.search.find import *
from api.module.module import *
from api.module.script import *
from api.taskmanager.taskmanager import *

class BATCH(Script):
  def __init__(self):
    Script.__init__(self, "batch")
    self.vfs = vfs.vfs()
    self.tm = TaskManager()   
 
  def start(self, args):
   script = args.get_string("modules")
   f = FIND()
   nodelist = f.find(args)
   x = 0
   for node in nodelist:
     args = libenv.argument("batch")
#XXX check node name, != file as name
     args.add_node("file", node)
     self.tm.add(script, args, ["console","thread"])
     x += 1
   self.res.add_const("result",  str(x) + " jobs scheduled")


class batch(Module):
  """Process a command or a batch of command in background
exemple: process decodesms *.sms
find all .sms file and execute decode_sms on each"""
  def __init__(self):
   Module.__init__(self, "batch", BATCH)
   self.conf.add("modules", "string")
#only module with one node as arg
   self.conf.add("pattern", "string")
   self.tags = "process"
