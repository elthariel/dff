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

from gif import *
from jpeg import * 
from pdf import * 
from api.vfs import *
from api.module.module import *
from api.module.script import *

##bufferiser read 
class CARVER(Script):
  def __init__(self):
    Script.__init__(self, "carver")

  def start(self, args):
    node  = args.get_node("file")
    nfilename = node.path + "/" + node.name + "/" + "carved" 

    self.buff = "Searching jpeg:\n"
    c = carv_jpeg()
    l = c.find(node)
    if not len(l):
     self.buff += "Can't find jpeg file\n"
    else :
      self.buff += "Found " + str(len(l)) + " jpeg files\n"
    c.create(node, nfilename, l)

    self.buff += "Searching gif:\n"
    c = carv_gif()
    l = c.find(node)
    if not len(l):
     self.buff += "Can't find gif file\n"
    else :
      self.buff += "Found " + str(len(l)) + " gif files\n"
    c.create(node, nfilename, l)

    self.buff += "Searching pdf:\n" 
    c = carv_pdf()
    l = c.find(node)
    if not len(l):
     self.buff += "Can't find pdf file\n"
    else :
     self.buff += "Found " + str(len(l)) + " pdf files\n"
    c.create(node, nfilename, l)
    self.res.add_const("result", self.buff)
#    return buff 

#XXX bufferised display
#  def c_display(self):
 #   return self.buff

class carver(Module):
  def __init__(self):
   Module.__init__(self, "carver", CARVER)
   self.conf.add("file", "node")
   self.tags = "parser"
