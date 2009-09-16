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
#  Solal J. <sja@digital-forensic.org>
#

import magic
from api.vfs import *
from api.env import *

class etype:
    pass

class FILETYPE():
  def __init__(self, db = "./api/magic/magic.mime", db1 = "./api/magic/magic"):
        self.vfs = vfs.vfs()
        self.env = env.env()
        try:
            self.__db = db
            self.__db1 = db1
            self.__ms = magic.open(magic.MAGIC_NONE)
            if self.__ms == None:
                raise etype
            self.__run = 1
        except etype:
            self.__run = 0
  def quit(self):
        self.__ms.close()
        self.__run = 0
  def load_mdb(self, db):
        try:
            self.__ms.load(db)
        except etype:
            print self.__ms.error()

  def __type_m(self, buffer, db):
        try:
            self.load_mdb(db)
            file_type = self.__ms.buffer(buffer)
            err = self.__ms.error()
            if err != None:
                raise etype
        except etype:
            pass
        except:
            pass
            file_type = None
        return file_type

  def gettype(self, node):
        try:
            if self.__run == 0:
                raise etype
            f = node.open()
            buffer = f.read(0x2000)
            f.close()
            file_type = self.__type_m(buffer, self.__db1)
	    return file_type
        except etype:
            pass 
            return 
        except:
            return None
 
  def findcompattype(self, node):
      """find compatible drivers and script"""
      buff = [] 
      mtype = self.gettype(node)
      val = self.env.vars_db["mime-type"].val_l
      for v in val:
        if v.type == "string":
          if mtype.find(v.get_string()) > -1:
            buff.append(v._from)
      return buff
 
  def filetype(self, node):
	buff = ""
        try:
            if self.__run == 0:
                raise etype
            f = node.open()
            buffer = f.read(0x2000)
            f.close()
            file_type = self.__type_m(buffer, self.__db1)
            f.node.attr.smap["type"] = file_type
	    buff += "type : " + file_type + "\n"
            file_type = self.__type_m(buffer, self.__db)
            buff += "type-mime : " + file_type + "\n"
            f.node.attr.smap["type-mime"] = file_type
	    return buff
        except etype:
            return "Cannot run: " +  self.error + "\n"
        except:
            return "An error occured when testing file type\n"
        return buff 

