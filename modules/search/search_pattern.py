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
from api.module.script import *
from api.module.module import *

class SEARCH(Script):
  def __init__(self):
    Script.__init__(self, "search")
    self.vfs = vfs.vfs()
 
  def start(self, args):
    node = args.get_node("file")
    pattern = args.get_string("pattern")
    f  = node.open()
    if not f:
       return "Can't open node"
    size = 0
    buff = f.read(4096)
    find = ""
##XXX first read, not parsed !  
    while len(buff) > 0:
      try:
        buff = f.read(4096)
      except vfsError:
         if len(find):
           return find + "\n read error "
         else:
	   return "read error"
      n = buff.find(pattern) 
      size += len(buff)
      if n != -1:
        find += "found  at offset: %x\n" % (n + size)
    if not len(find):
      self.res.add_const("error", "Nothing found")
    else: 
      self.res.add_const("result", find)  

class search_pattern(Module):
  def __init__(self):
   Module.__init__(self, "search", SEARCH)
   self.conf.add("file", "node")
   self.conf.add("pattern", "string")
   self.tags = "search"
