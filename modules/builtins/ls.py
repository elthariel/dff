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
from api.module.script import *

class LS(Script):
  def __init__(self) :
    Script.__init__(self, "ls")
    self.vfs = vfs.vfs()

  def start(self, args):
    self.node = args.get_node('node')
    self.long = args.get_bool('long')
    self.rec = args.get_bool('recursive')
    if self.node == None:
      self.node = self.vfs.getcwd()
    self.res = self.launch()

  def launch(self):
     if self.rec:
       self.recurse(self.node)
     else :
       self.ls(self.node)

  def recurse(self, cur_node):
     if not cur_node.next.empty():
	 self.ls(cur_node)
     next = cur_node.next
     for next_node in next:
       if not next_node.next.empty():
         self.recurse(next_node)

  def ls(self, node):
     buff = ""
     next = node.next
     for n in next:
        print self.display_node(n)

  def display_node(self, node):
    if self.long:
      return self.display_node_long(node)
    else:
      return self.display_node_simple(node)

  def display_node_long(self, node):
    buff = node.path + '/' + node.name
    if not node.next.empty():
      buff += "/" 
    if node.is_file:
      buff += '\t' + str(node.attr.size)
    return buff

  def display_node_simple(self, node):
    buff = ''	
    buff = node.name
    if not node.next.empty():
     buff += "/"
    return buff

class ls(Module):
  def __init__(self):
   """List file and directory"""
   Module.__init__(self, "ls", LS)
   self.conf.add("node", "node", True)
   self.conf.add("long", "bool", True)
   self.conf.add("recursive", "bool", True)
   self.tags = "builtins"
