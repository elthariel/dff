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
import ui.history as hist

class HISTORY(Script):
  def __init__(self):
    Script.__init__(self, "history")
    self.h = hist.history()

  def start(self, args):
    try :	
      if args.get_bool("clear"):
         self.h.clear()
      else :	
        for i in range(0, len(self.h.hist)):
  	  print (str(i) + '\t' + self.h.hist[i]).strip('\n')
    except envError:
       pass	

class history(Module):
  def __init__(self):
   Module.__init__(self, "history", HISTORY)
   self.conf.add("clear", "bool", True)
   self.tags = "builtins"
