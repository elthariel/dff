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

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from api.vfs import *
from api.module.module import *
from api.module.script import *

class CAT(QTextEdit, Script):
  def __init__(self):
    Script.__init__(self, "cat")
    self.vfs = vfs.vfs()
    self.env = env.env()
    self.type = "cat"
    self.icon = None
  
  def start(self, args):
    self.args = args
    self.node = args.get_node("file")
    self.cat(self.node)

  def g_display(self):
    QTextEdit.__init__(self, None)
    self.setReadOnly(1)
    self.append(self.buff)

  def cat(self, args):
    file = self.node.open()
    fsize = self.node.attr.size
    size = 0
    self.buff = ""
    while size < fsize:
      try:
       tmp = file.read(4096)
      except vfsError, e:
        file.close()
        return self.buff
      size += len(tmp)
      self.buff += tmp
      print tmp
    file.close()
    if len(self.buff): 
     return self.buff

class cat(Module):
  def __init__(self):
    """Show file content
ex:cat /myfile.txt"""
    Module.__init__(self, "cat", CAT)
    self.conf.add("file", "node")
    self.tags = "viewer"
    self.flags = ["console", "gui"]	
