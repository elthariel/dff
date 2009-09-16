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
from time import *

class TEST(Script):
  def __init__(self):
    Script.__init__(self, "statest")

  def start(self, args):
    for i in range(0, 100):
	sleep(1)
	self.stateinfo = str(i) + "%"	
    self.res.add_const("result",  "change path to " + node.path + "/" + node.name)

    	 

class statest(Module):
  def __init__(self):
   Module.__init__(self, "statest", TEST)
   self.tags = "test"
