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

from api.magic.filetype import *
from api.vfs import *
from api.env import *
from api.loader import *
from api.module.module import *
from api.module.script import *

class FILEINFO(Script): 
  def __init__(self):
      Script.__init__(self, "fileinfo")
      self.ft = FILETYPE()
  def start(self, args):
    buff = ""
    node = args.get_node("file")
    buff += "File " + node.path + "/" + node.name
    if not node.next.empty():
      buff += " is linked to\n" + str(node.next.size()) + " files\n" 
    elif node.is_file == 1:
      buff += " as data content\n"
      buff += "Size:" + str(node.attr.size) + " \n"
    elif not node.next.empty() and node.is_dir: 
      buff += " as data content and is linked to " + (node.next.size()) + " files\n"        
      buff += "Size:" + str(node.attr.size) + " \n"
    self.ft.filetype(node)
    map =  node.attr.smap
    for i in map:
      buff += i + ":" + map[i] + "\n"
    map =  node.attr.imap
    for i in map:
      buff += i + ":" + str(map[i]) + "\n"
    map =  node.attr.time
    for i in map:
      buff += i + ":" + str(map[i].get_time()) + "\n"
    if node.is_file == 1:
      n = self.ft.findcompattype(node)
      if len(n):
        buff += "Compatible drivers:\n"
        for i in n:
          buff += i + "\n"
    self.res.add_const("result", buff)

class fileinfo(Module):
  def __init__(self):
    Module.__init__(self, "fileinfo",  FILEINFO)
    self.conf.add("file", "node")
    self.tags = "information"
