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

import os, sys
import imp
import re
import traceback

from api.loader.libloader import *
from api.module.module import *
from api.module.libcmodule import *
from stat import *

class loader():
    cmodules_db = Loader.Get().cmodules_db
    class __loader():
        def LoadCModules(self, args):
            print "loading ", args
	    try:
              self.libloader.LoadCModule(args)
	      db = self.libloader.cmodules_db
	      for drvname in db:
		try:
	          self.modules[drvname]
		except:
                  self.modules[drvname] = Module(drvname, self.libloader.cmodules_db[drvname])
	    except LoaderError, e:
               print e.error
	       return e.error
	       		
	def UnloadCModules(name):
	   try:
	      self.libloader.UnloadCModules(name)
	   except LoaderError, e:
	      return e.error

	def getcmodulemap(self):
	     return(self.libloader.cmodules_db)
	
	def getcmodule(self, name):
	   try :
	     cmodule = self.libloader.cmodules_db[name]
	   except IndexError :
             return "key " + name + " not found"
           return (cmodule)

        def LoadFile(self, module_path):
            filename = module_path[module_path.rfind("/")+1:]
            path = module_path[:module_path.rfind("/")+1]
            if filename.rfind(".py") != -1:
                sys.path.append(path)
                self.ModuleImport(module_path, filename[:filename.rfind(".py")])
            elif filename.rfind(".mod") != -1 and filename[-1] == "d":
                self.LoadCModules(module_path)

        def LoadDir(self, module_path):
            files = os.listdir(module_path)
            if module_path[len(module_path) - 1] != "/":
                module_path += "/"
            for filename in files:
                if not filename.startswith(".") and not filename.startswith("__") and not filename.startswith("#"):
                    try:
                        mode = os.stat(module_path+filename)[ST_MODE]
                    except:
                        print "File doesn't exist"
                    if mode:
                        if S_ISDIR(mode):
                            self.LoadDir(module_path+filename)
                        else:
                            self.LoadFile(module_path+filename)

        def Load(self, args):
            module_path = args
            mode = None
            try:
	      print "LOADING FROM " + module_path
              mode = os.stat(module_path)[ST_MODE]
            except:
              print "File doesn't exist"
            if mode:
              if S_ISDIR(mode):
                self.LoadDir(module_path)
              elif S_ISREG(mode):
                self.LoadFile(module_path)
              else:
               print "unsupported stat type"

        def ModuleImport(self, module_path, modname):
            start = False
            init = False
            type = False
            
	    if modname == "loader":
		return 
            f = open(module_path, 'r')
            flag = 0
            for line in f:
	      if line.find("(Module)") != -1:
		  flag = 1
            f.close()
	    if flag == 0:
	       return 
	    else :
	      flag = 0
            if modname in sys.modules:
              module = sys.modules[modname]
              del module
            file, pathname, description = imp.find_module(modname)
            try:
               module = imp.load_module(modname, file, pathname, description)
               cl = getattr(module, modname)
	       self.modules[modname] = cl()
               print "loading", modname, "from", pathname,  "[OK]"
               sys.modules[modname] = module
            except:
               print "\nloading", modname, "from", pathname, "[!!]"
               exc_type, exc_value, exc_traceback = sys.exc_info()
               traceback.print_exception(exc_type, exc_value, exc_traceback, None, sys.stdout)
               print ""
            else:
                pass

        def GetScripts(self):
            return self.scripts

        def GetBuiltins(self):
            return self.builtins

        def GetCModules(self):
            return self.cmodules

        def __init__(self):
            self.cmodules = {}
            self.scripts = {}
            self.builtins = {}
	    self.modules = {}
            self.libloader = Loader.Get()
            

    __instance = None

    def __init__(self):
        if loader.__instance is None:
            loader.__instance = loader.__loader()

    def __setattr__(self, attr, value):
        setattr(self.__instance, attr, value)

    def __getattr__(self, attr):
        return getattr(self.__instance, attr)

    def getcmodule(self, arg):
        return self.__instance.getcmodule(arg)

    def getcmodulemap(self):
        return self.__instance.getcmodulemap()

    def do_load(self, args):
        path = args
	if os.name == "nt":
	  if args[1] != ":":
            path = os.getcwd() + "/" + args
    	else:	
          if args[0] != "/":
            path = os.getcwd() + "/" + args
        self.__instance.Load(path)

    def help_load(self):
        print "load [path/[file]]"
    
    def do_lsmod(self, args):
        """List loaded modules"""
        return []

    def do_unloadmodule(name):
        """Unload modules"""
        self.__instance.UnloadCModules(name) 

    def get_builtins(self):
        return self.__instance.GetBuiltins()

    def get_cmodules(self):
        return self.__instance.GetCModules()
