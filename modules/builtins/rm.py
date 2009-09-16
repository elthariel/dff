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
from api.env import *
from api.driver import *
from api.loader import *
from api.script import *
from api.exceptions.libexceptions import *

tags="script"

def init():
  c = script.Script("closedump", start)
  c.conf.add("parent", "node")
  r = script.Script("rm", rm)
  r.conf.add("parent", "node")

def rm(args):
  node =  args.get_node("parent")
  if not node:
     return script.Result("STRING", "Error can't find node")
  v = vfs.vfs()
  v.deletenode(node) 
  return

def start(args):
   node = args.get_node("parent")
   if not node:
     return script.Result("STRING", "Error can't find node")
   l = loader.loader()
   drvname = node.fsobj.drvname
   drv = l.drivers_db[drvname]
   try :
     drv.CloseDump(node.fsobj)
   except vfsError, err:
      return script.Result("STRING", err.error)
   return script.Result("STRING", "Dump close succefully")
