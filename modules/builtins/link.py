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

class LINK(Script):
  def __init__(self):
    Script.__init__(self, "link")

  def start(self, args):
    dest = args.get_node("dest")
    node = args.get_node("file")
    if not node:
      self.res.add_const("error", "Can't find file")
      return	
    try :
      rename = args.get_string("rename")
    except envError:
       pass
    if rename:
       self.vfs.link(node, rename, dest)
    else:
       self.vfs.link(node, dest) 
    self.res.add_const("result",  "linked " + dest.path + "/" + node.name + " created")


class link(Module):
  def __init__(self):
   Module.__init__(self, "link", LINK)
   self.conf.add("file", "node")
   self.conf.add("dest", "node")
   self.conf.add("rename", "string", 1)
   self.tags = "builtins"
