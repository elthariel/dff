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

import sys

from subprocess import *
from api.vfs import *
from api.module.script import *
from api.module.module import *

class PLAYER(Script):
  def __init__(self):
     Script.__init__(self, "player")
     self.vfs = vfs.vfs() 

  def start(self, args):
     node = args.get_node("file")
     file = node.open()
     buff = file.read()
     file.close()
     p = Popen("mplayer -", shell=1,stdin=PIPE,stdout=PIPE)
     out = p.communicate(buff)[0]
     p.wait()

class player(Module):
  def __init__(self):
   """Pipe a file to mplayer external command"""
   Module.__init__(self, "player", PLAYER)
   self.conf.add("file", "node")
   self.tags = "viewer"
