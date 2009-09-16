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
#  Frederic B. <fba@digital-forensic.org>
#

from api.exceptions.libexceptions import *

class env():
  class __env():
    def __init__(self):
      pass
  __instance = None

  def __setattr__(self, attr, value):
    setattr(self.__instance, attr, value)

  def __getattr__(self, attr):
    getattr(self.__instance, attr)

  def __init__(self):
    if env.__instance is None:
      env.__instance = env.__env()

  def getValuesInDb(self, vardb_name, type):
    value = []
    for i in self.vars_db:
      if str(i) == vardb_name:
        val = self.vars_db[i].val_l
        for v in val:
          if v.type == type :
            if v.type == "int":
              value.append(v.get_int())
            elif v.type == "string":
              value.append(v.get_string())
            elif v.type == "node": 
              value.append(v.get_node())
	    elif v.type == "path":
	      value.append(v.get_path().path)
    return value
  
  def get_val_list(self, vlist):
    # return a list of tupple [(type, name, value, _from)]
    # ex: for type, name, val in get_val_list(val_m):
    #     print type, name, val, _from
    res = [] 
    for i in  vlist:
      if i.type == "string":
       res += [(i.type, i.name, i.get_string(), i._from)]
      elif i.type == "int":
       res += [(i.type, i.name, str(i.get_int()), i._from)]
      elif i.type == "node" and i.get_node() :
       res += [(i.type, i.name, i.get_node().path + "/" + i.get_node().name, i._from)]
      elif i.type == "path":
       res += [(i.type, i.name, i.get_path().path, i._from)]		
    return res

  def get_val_map(self, map):
    # return a list of tupple [(type, name, value)]
    # ex: for type, name, val in get_val_map(val_m):
    #     print type, name, val
    res = [] 
    for i in map:
      a = map[i]
      if a == None:
	pass 
      elif a.type == "int":
	res += [(a.type, i, str(a.get_int()))]
      elif a.type == "string":
	res += [(a.type, i, str(a.get_string()))]
      elif a.type == "node" and a.get_node():
	res += [(a.type, i,  a.get_node().path + "/" + a.get_node().name)]
      elif a.type == "path":
	res += [(a.type, i, a.get_path().path)]
    return res
 
  import libenv
  vars_db = libenv.env.Get().vars_db
