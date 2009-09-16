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
from api.exceptions.libexceptions import *

class CD(Script):
  def __init__(self):
    Script.__init__(self, "cd")

  def start(self, args):
    node = args.get_node("dir")
    if not node:
      self.res.add_const("error", "Can't find file")
      return	
    if node.next.empty():
      self.res.add_const("error", "Can't change current directory on file")
      return 
    self.vfs.setcwd(node)
    self.res.add_const("result",  "change path to " + node.path + "/" + node.name)


class cd(Module):
  def __init__(self):
   Module.__init__(self, "cd", CD)
   self.conf.add("dir", "node")
   self.tags = "builtins"
