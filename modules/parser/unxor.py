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
from api.env import *
from api.exceptions.libexceptions import *

class UNXOR(Script):
  def __init__(self):
    Script.__init__(self, "unxor")
    self.vfs = vfs.vfs()
    self.touch = TOUCH().touch

  def start(self, args):
    file = args.get_node('file')
    key = args.get_string('key')
    res = self.unxor(file, key)
    self.res.add_const("result", res)

  def unxor(self, node, key):
    dfilename = node.path + "/" + node.name +  "/decrypted"
    dfile = self.touch(dfilename).open()
    file = node.open()
    decrypt = ""
    ki = 0
    try:
      buff = file.read(4096)
    except vfsError, e:
      return "error"
    while len(buff) > 0:
      for x in range(len(buff)):
        dfile.write(chr(ord(buff[x]) ^ ord(key[ki])))
        ki = (ki + 1) % len(key)
      try:
        buff = file.read(4096)
      except vfsError, e:
        file.close()
        dfile.close()
      return dfilename + " decrypted"
    file.close()
    dfile.close()
    return dfilename + " decrypted" 

class unxor(Module):
  """Decrypt a XORed file
ex: unxor /myfile key"""
  def __init__(self):
    Module.__init__(self, "unxor", UNXOR)
    self.conf.add("file", "node")  
    self.conf.add("key", "string")
    self.tags = "crypto"
