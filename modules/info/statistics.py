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
from api.magic.filetype import *
from api.module.script import *
from api.module.module import *

class STATISTICS(Script):
  def __init__(self):
    Script.__init__(self, "statistics")
    self.vfs = vfs.vfs()
    self.dtype = {}
    self.ftype = FILETYPE()

  def start(self, args):
    node = args.get_node("parent")    
    self.getstat(node)
    res = self.print_stat_result()
    self.res.add_const("result", res)

  def getstat(self, node):
    if node.is_file: 
      self.ftype.filetype(node) 
      file_type = node.attr.smap["mime-type"]
      if file_type not in self.dtype:
        self.dtype[file_type] = 1
      else:
        self.dtype[file_type] += 1
    list = node.next
    buff = ""
    for i in list:
        buff +=  self.getstat(i)
    return buff

  def print_stat_result(self):
    buff = ""
    for k, v in self.dtype.iteritems():
        buff += str(v) + " " + str(k) + "\n"
    return buff


class statistics(Module):
  def __init__(self):
    """Show statistics of filetype for a file or a directory, use cwd by default
ex: statistics
ex: statistics /mydump/"""
    Module.__init__(self, "statistics", STATISTICS)
    self.conf.add('parent', 'node')
    self.tags = "information"


