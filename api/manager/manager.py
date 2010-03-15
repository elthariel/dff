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
#  Frederic Baguelin <fba@digital-forensic.org>
#  Solal Jacob <sja@digital-forensic.org>


from api.type.libtype import Path
from api.env.env import env
from api.env.libenv import argument
from api.search import libsearch
from api.vfs import vfs, libvfs
from api.type import OS
from dircache import listdir
from api.loader import loader
from api.taskmanager.taskmanager import TaskManager
 
class ApiManager():
   class __ApiManager():
      def __init__(self):
         self.vfs = vfs.vfs
         self.TaskManager = TaskManager 	
         self.env = env
         self.argument = argument 
         self.loader = loader.loader
         self.Path = Path
         self.OS  = OS.OS

   __instance = None

   def __init__(self):
      if ApiManager.__instance is None:
         ApiManager.__instance = ApiManager.__ApiManager()
 
   def __setattr__(self, attr, value):
      setattr(self.__instance, attr, value)

   def __getattr__(self, attr):
      return getattr(self.__instance, attr) 
