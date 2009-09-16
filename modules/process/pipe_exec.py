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
from subprocess import *

class PIPE_EXEC(Script):
  def __init__(self):
     self.vfs = vfs.vfs()

  def start(self, args):
     cmd = args.get_string("command")
     node = args.get_node("file")
     file = node.open()
     buff = file.read()
     file.close()
     Popen(cmd,1, shell=1, stdin=PIPE).communicate(buff)

class pipe_exec(Module):
  """open a file and pipe it to an external command
ex: exec_pipe /file.txt less"""
  def __init__(self):
   Module.__init__(self, "pipe_exec", PIPE_EXEC)
   self.conf.add("file", "node")
   self.conf.add("command", "string")
   self.tags = "process"	
