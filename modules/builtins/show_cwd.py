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
from api.module import *

class SHOW_CWD(Script):
  def __init__(self):
    Script.__init__(self, "show_cwd")
    self.vfs = vfs.vfs()

  def start(self, args):
    cwd = self.vfs.getcwd()
    print cwd.path + "/" + cwd.name

class show_cwd(Module):
  def __init__(self):
    Module.__init__(self, "show_cwd", SHOW_CWD)
    self.tags = "builtins"
