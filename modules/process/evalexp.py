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

class EVAL(Script):
  def __init__(self):
    Script.__init__(self, "eval")

  def start(self, args):
    expr = args.get_string("expression")
    hex = args.get_bool("hex")
    buff = eval(expr)
    if hex:
      self.res.add_const("result", "0x%x" % buff)
    else:
      self.res.add_const("result", buff)
 
class evalexp(Module):
  def __init__(self):
    Module.__init__(self, "eval", EVAL)
    self.conf.add("expression", "string")
    self.conf.add("hex", "bool")
    self.tags = "process"

