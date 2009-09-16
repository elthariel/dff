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

import string

from api.vfs import *
from api.module.script import*
from api.module.module import *
from api.module.libcmodule import *

from api.env import *
from api.env.libenv import *
from api.type.libtype import *
from api.module import *
from api.vfs.libvfs import *
from api.exceptions.libexceptions import *

class streamstrings(Module):
  def __init__(self):
    Module.__init__(self, "streamstrings", streamfs)
    self.conf.add("parent", "node")
    self.tags = "fs"
    self.flags  = [""]

class streamfs(fso):
  def __init__(self):
    fso.__init__(self)
    self.vfs = vfs.vfs()
    self.name = "streamstrings" 
    setattr(self, "vopen", self.vopen) 
    setattr(self, "vread", self.vread) 
    setattr(self, "vwrite", self.vwrite) 
    setattr(self, "vseek", self.vseek) 
    setattr(self, "vclose", self.vclose)
    self.res = results(self.name)
 
  def start(self, args):
    parent = args.get_node('parent')
    attr  = attrib()
    attr.thisown = 0 
    self.size = parent.attr.size
    attr.size = parent.attr.size 
    attr.handle = Handle("strings")
    self.parent = parent.open()
    self.fdm = fdmanager()
    self.fdm.InitFDM()
    name = "strings"
    root = self.CreateNodeFile(parent, name, attr)
 
  def vopen(self, handle):
    fi = FDInfo()
    fi.thisown = 0
    fd = self.fdm.AllocFD(fi)
    self.fdm.UpdateFD(fd, 0)
    return fd

  def vread(self, fd, buff, size):
    fi = self.fdm.GetFDInfo(fd)
    try:
      self.parent.seek(fi.current)
      pbuff = self.parent.read(size)
    except vfsError, e:
      raise vfsError("streamstrings read parent" + e.error)
    if len(pbuff) == 0:
      raise vfsError("streamstrings end of parent file")
    self.fdm.UpdateFD(fd, self.parent.tell())
    b = stringify(pbuff)
    if len(b) == 0:
      return (0, "")
    return (len(b), b)

  def vseek(self, fd,  pos, whence):
    if (pos < self.size): 
      self.fdm.UpdateFD(fd, pos)
    else :
      raise vfsError("Can't seek")
    return pos 

  def vwrite(self, fd,  buff, size):
    raise vfsError("Can't write")

  def vclose(self, fd):
    self.fdm.ClearFD(fd)
    return 0

  def status(self):
    return 0
 
def stringify(buff):
    newline = 0
    flag = 0
    tmp = ""
    lstring = ""
    for c in buff:
        if c in string.printable: 
          tmp = tmp + c
          if c == '\n':
            newline = 81
          flag = 1
        if flag:
          if newline >= 80:
            if newline == 80:
              lstring = lstring + tmp + '\n'
            else:
              lstring = lstring + tmp
            tmp = ""
            newline = 0
          else:
            newline += 1
          flag = 0 
    return lstring

