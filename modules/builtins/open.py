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
from api.module.module import *
from api.exceptions.libexceptions import *
from api.magic.filetype import *
from api.loader import *
from api.taskmanager.taskmanager import *
from api.env import *


class Open(Script):
  def __init__(self):
    Script.__init__(self, "open")
    self.loader = loader.loader()
    self.lmodules = self.loader.modules
    self.taskmanager = TaskManager()
    self.env = env.env()

  def start(self, args):
    node = args.get_node("file")
    self.open(node)

  def open(self, node):
    arg = self.env.libenv.argument("gui_input")
    arg.thisown = 0 
    ft = FILETYPE()
    try:
      mod = ft.findcompattype(node)[0]
      if self.lmodules[mod]:
        conf = self.lmodules[mod].conf
        cdl = conf.descr_l
        for a in cdl:
          if a.type == "node":
             arg.add_node(a.name, node)
      self.taskmanager.add(mod, arg, ["thread", "gui"])       
    except IndexError: 
      print  "No module register type " + self.node.attr.string["type"]
    print  "applying module " + mod + " on " + node.path + "/" + node.name

class open(Module):
  def __init__(self):
   Module.__init__(self, "open", Open)
   self.conf.add("file", "node")
   self.tags = "builtins"
