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

from api.module.script import *
from api.taskmanager.taskmanager import *
from api.module.module import *

def cb_pp(node):
  tm = TaskManager()
  args = libenv.argument("post_process")
#check node name, != file
  args.add_node("file", node)
  tm.add(mod, args, ["console", "thread"])
  return 

class POST_PROCESS(Script):
  def __init__(self):
    Script.__init__(self, "post_process")
    self.vfs = VFS.Get()

  def start(self, args):
#if add script -> add to list func x
#if arg script -> del -> del func x
    global mod
    mod = args.get_string("modules")
    self.vfs.set_callback("post_process", cb_pp)
    return

class post_process(Module):
  """Process a command on each new file created on the vfs"""
  def __init__(self):
    Module.__init__(self, "post_process", POST_PROCESS)
    self.conf.add("modules", "string")
    self.tags = "process"
