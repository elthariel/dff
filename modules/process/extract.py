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

import os
from api.vfs import *
from api.module.script import *
from api.exceptions.libexceptions import *
from api.module.module import *
import time


class EXTRACT(Script):
  def __init__(self):
    Script.__init__(self, "extract")
    self.vfs = vfs.vfs()
    self.total = 1
    self.current = 0
    self.debug = open("/home/udgover/extract/debug_read",'wb')

  def start(self, args):
    self.node = args.get_node('file')
    self.path = args.get_path('syspath').path
    self.unpath = self.node.path
    try :
      if self.unpath[-1] == '/':
	  self.unpath = self.unpath.rstrip('/')
    except IndexError:
	pass
    self.unpath = self.unpath.rsplit('/')[-1]
    self.rec = args.get_bool('recursive')
    res = self.launch()
    self.res.add_const("result", res)


  def launch(self):
    self.total += self.get_total_to_extract(self.node)
    res = self.extract(self.node)
    if self.rec or not self.node.next.empty():
      res += self.recurse(self.node)
    return res


  def get_total_to_extract(self, node):
    total = 0
    next = node.next

    for cur_node in next:
      if not cur_node.next.empty():
        if cur_node.attr.size > 0:
          total += 1
        total += self.get_total_to_extract(cur_node)
      else:
        total += 1
    return total


  def recurse(self, node):
    res = ""
    
    next = node.next
    for cur_node in next:
      if not cur_node.next.empty():
        if cur_node.attr.size > 0:
          res += self.extract(cur_node)
        res += self.recurse(cur_node)
      else:
        res += self.extract(cur_node)
    return res + "\n"


  def extract(self, node):
    res = ""
    
    syspath = self.path + node.path
    sysname = node.name
    if not node.next.empty():
      sysname += ".data"
    try:
      self.current += 1
      self.stateinfo = str(self.current) + " / " + str(self.total)# + "( " + node.path + "/"  + node.name + " )"
      self.debug.write(node.path + "/"  + node.name + " in " + syspath + "/" + sysname + "\n")
      vfile = node.open()
      path = syspath.rfind('/')
      if not os.path.exists(syspath):
        os.makedirs(syspath)
      sysfile = open(syspath + "/" + sysname,'wb')
      readsize = 8096
      buff = vfile.read(readsize)
      while len(buff):
        sysfile.write(buff)
        buff = vfile.read(readsize)

      vfile.close()
      sysfile.close()
      res +="extracted node: " + node.path + "/"  + node.name + " in " + syspath + "/" + sysname + "\n"
      return res
    except vfsError, e:
       return "extract: Can't open " + node.path + "/" + node.name + "\n"
    except OSError:
       return "extract: Can't create " + syspath + "\n"

class extract(Module):
  def __init__(self):
    Module.__init__(self, "extract", EXTRACT)
    self.conf.add("file", "node")
    self.conf.add("syspath", "path")
    self.conf.add("recursive", "bool", True)
    self.tags = "process"
