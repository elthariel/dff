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

from modules.fs.shm.touch import *
from api.module import *
from api.vfs import *

import mzipfile

class UNZIP(Script):
  def __init__(self):
    Script.__init__(self, "unzip")
    self.vfs = vfs.vfs()
    self.touch = TOUCH().touch
    pass

  def start(self, args):
      node = args.get_node('file')
      file = node.open()
      zf = mzipfile.ZipFile(file)
      for uzfile in zf.namelist():
          zinfo = zf.getinfo(uzfile)
          if zinfo.file_size > 0:
              dfilename = node.path + "/" + node.name + "/" + uzfile
              dnode = self.touch(dfilename)
              dfile = dnode.open()
              dfile.write(zf.read(uzfile))
              dfile.close()
      file.close()
      zf.close()

  def createpath(self, parent, new_dir):
      node = vfs.getnode(parent)
      attr = attrib()
      attr.thisown = 0

class unzip(Module):
  """unzip...
ex: unxor file"""
  def __init__(self):
    Module.__init__(self, "unzip", UNZIP)
    self.conf.add('file', 'node')
    self.conf.add_const('mime-type', 'Zip')
    self.tags = "archive"
