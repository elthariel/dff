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

import re

from api.vfs import *
from api.module.script import *
from api.module.module import *

class FIND(Script):
  def __init__(self):
    self.vfs = vfs.vfs()
    Script.__init__(self, "find")
    self.fres = []

  def start(self, args):
    fres = self.find(args)
    if not fres:
      self.res.add_const("error", "Can't find file")
      return 
    buff = "Found " + str(len(fres)) + " files\n"
    for i in fres:
      buff += i.path + "/" + i.name + "\n" 
    return	

  def c_display(self):
    buff = "Found " + str(len(self.fres)) + " files\n"
    for i in self.fres:
      for i in self.fres:
        buff += i.path + "/" + i.name + "\n" 
    print buff
	
 
  def find(self, args):
# toto*.kp 
# toto.*
    filename = args.get_string("pattern")
    starred = 0
    if filename[-1] == '*':
      name = filename[0:-1]
      n = re.compile(r'\A' + name + '[a-zA-Z0-9]*', re.IGNORECASE)
      starred = 1
# *.jpg
    elif filename[0] == '*':
      name = filename[1:]
      n = re.compile(r'' + name + '\Z[a-zA-Z0-9]*', re.IGNORECASE)
      starred = 1
    list = self.vfs.gettree()
    for i in list:
     if starred:
       if n.findall(i.name):
         self.fres.append(i)
     elif i.name == filename :
         self.fres.append(i)
    return self.fres


class find(Module):
  def __init__(self):
    """Search file on the vfs, * wildcard accepted
ex: find *.sms"""
    Module.__init__(self, "find", FIND)
    self.conf.add("pattern", "string")
    self.tags = "search"


