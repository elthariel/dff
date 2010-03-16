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
#  Francois Percot <percot@gmail.com>
# 

from types import *

from api.loader import *
from api.env import *
from api.taskmanager.taskmanager import *
from api.type import *

class DFF_Utils():
    def __init__(self):
        pass

    @staticmethod
    def getSetTags():
	lmodules = loader.loader().modules
	setags = set()
	for mod in lmodules:
	  try:
	   setags.add(lmodules[mod].tags) 
	  except AttributeError:
	   pass
  	try :
	   setags.remove('')
	except KeyError:
	   pass
	return setags
	
    @staticmethod
    def formatSize(size):
        lsize = [" KB", " MB", " GB"]
        if size < 1024 :
            return str(size) + " bytes"
        
        for i in range(0, len(lsize)):
            tmp_size = size / 1024
            if (tmp_size < 1024):
                return str(tmp_size) + lsize[i]
            else:
                size = tmp_size

    @staticmethod
    def getPath(node):
        if not node :
            return ""
        if node.name == "":
            return str("/")
        else :
            return str(node.path) + "/" + str(node.name)

    @staticmethod
    def getValue(arg):
        if arg <> None:
            if arg.type == "int":
                return str(arg.get_int())
            elif arg.type == "string":
                return str(arg.get_string())
            elif arg.type == "node": 
                node = arg.get_node()
                return DFF_Utils.getPath(node)
            elif arg.type == "bool" :
                return str(arg.get_bool())
            elif arg.type == "path" :
                return str(arg.get_path().path)
        return "TYPE NOT DEFINE"
    
    @staticmethod
    def getArgsDriver(driver_name):
        l = loader.loader()
        return l.getdriver(driver_name).conf.descr_l
    
    @staticmethod
    def getArgs(modules_name):
        l = loader.loader()
        if type(modules_name) == StringType :
            return l.modules[modules_name].conf.descr_l
        else :
            return None
    
    @staticmethod
    def hasOneNodeArg(module, type):
        args = DFF_Utils.getArgs(module)
        if not args :
            return None
        if len(args) == 1 :
            if args[0].type == "node" :
                return args[0].name
        return None
        
    @staticmethod
    def execModule(name, type, nameArg, listNode):
        e = env.env()
        tm = TaskManager()
	if isinstance(listNode, Node):
	    arg = e.libenv.argument("gui_input")
            arg.add_node(str(nameArg), listNode)
            tm.add(str(name), arg, ["thread", "gui"])
	else:
          for i in range(0, len(listNode)) :
            arg = e.libenv.argument("gui_input")
            arg.add_node(str(nameArg), listNode[i])
            tm.add(str(name), arg, ["thread", "gui"])
        
