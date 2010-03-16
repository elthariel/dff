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
from api.module import *
from api.env import *
from api.taskmanager.taskmanager import *
from SHM import *

class TOUCH(Script):
  class __Touch(Script):
    def __init__(self):
      Script.__init__(self, "touch")
      self.vfs = vfs.vfs()
      self.shm = SHM().create()

    def start(self, arg):
      fname = arg.get_string("filename")
      if self.touch(fname):
        self.res.add_const("result", "SHM create file " + fname)
      else:        
        self.res.add_const("error", "Can't find path")

    def touch(self, fname):
      plist = fname.split('/')
      snode = ''
      for path in plist:
        if path != '':
          snode += '/'
          node = self.vfs.getnode(snode)
	  if not self.vfs.getnode(snode  + path):
            node = self.shm.addnode(node, path)
	  snode += path 	
      return node     
#    if not fname.count('/'):
#      parent = self.vfs.getcwd().path + "/" + self.vfs.getcwd().name
#      filename = fname
#    else:
#      f = fname.rfind('/')
#      parent = fname[:f+1]
#      filename = fname[f+1:]
#    return node
  __instance = None
  def __init__(self):
   if TOUCH.__instance is None:
     TOUCH.__instance = TOUCH.__Touch()

  def __setattr__(self, attr, value):
   setattr(self.__instance, attr, value)

  def __getattr__(self, attr):
   return getattr(self.__instance, attr)

class touch(Module):
  def __init__(self):
    Module.__init__(self, "touch", TOUCH)
    self.tags = "shared memory"
    self.conf.add("filename", "string")

