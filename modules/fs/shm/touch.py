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
from api.module import *
from api.env import *
from api.taskmanager.taskmanager import *

class TOUCH(Script):
  def __init__(self):
    Script.__init__(self, "touch")
    self.vfs = vfs.vfs()
    self.arglist = libenv.argument("touch")
    self.tm = TaskManager()

  def start(self, arg):
    fname = arg.get_string("filename")
    self.touch(fname)

  def touch(self, fname):
    plist = fname.split('/')
    snode = ''
    for path in plist:
      if path != '':
        snode += '/'
        node = self.vfs.getnode(snode)
	if not self.vfs.getnode(snode  + path):
          self.createfile(path, node)
	snode += path 	
#    if not fname.count('/'):
#      parent = self.vfs.getcwd().path + "/" + self.vfs.getcwd().name
#      filename = fname
#    else:
#      f = fname.rfind('/')
#      parent = fname[:f+1]
#      filename = fname[f+1:]
#    node = self.vfs.getnode(parent)
#    if not node:
#      self.res.add_const("error", "Can't find path")
#      return
#    self.res.add_const("result", "SHM create file " + fname)
    return
 
  def createfile(self, filename, node): 
    self.arglist.add_string('filename', filename)
    self.arglist.add_node("parent", node)
    self.tm.add('shm', self.arglist, ["console"])

class touch(Module):
  def __init__(self):
    Module.__init__(self, "touch", TOUCH)
    self.conf.add("filename", "string")

