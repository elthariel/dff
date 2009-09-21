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
#  Jeremy Mounier <jmo@digital-forensic.org>
# 

import sys

class generateCode():
    def __init__(self):
        pass
    
    def set_header(self, fname, lname, mail):
        self.fname = fname
        self.lname = lname
        self.mail = mail

    def generate_header(self):
        buff="# DFF -- An Open Source Digital Forensics Framework\n\
#\n\
# This program is free software, distributed under the terms of\n\
# the GNU General Public License Version 2. See the LICENSE file\n\
# at the top of the source tree.\n\
# \n\
# See http://www.digital-forensic.org for more information about this\n\
# project. Please do not directly contact any of the maintainers of\n\
# DFF for assistance; the project provides a web site, mailing lists\n\
# and IRC channels for your use.\n\
# \n\
# Author(s):\n\
#  " + self.fname + " "+ self.lname +" < " + self.mail + ">\n\
#\n\
\n"
        return buff

    def generate_script(self,  scriptname):
        buff = self.generate_header()
        buff += "from api.vfs import *\n\
from api.module.module import *\n\
\n\
class " + scriptname.upper() + "(Script):\n\
    def __init__(self):\n\
	#Module init stuff goes here\n\
	Script.__init__(self, \"" + scriptname + "\")\n\
\n\
    def c_display(self):\n\
	#You can add console display function here\n\
	#like ncurses func or others display func\n\
	#ex: print \"buff\"\n\
	pass\n\
\n\
    def start(self, args):\n\
        #get your arg here, ex : args.get_node('filename')\n\
        #do some stuff, ex: print \"Hello\"\n\
	#you can set your state too, ex : self.stateinfo = \"Processing file\"\n\
        #return your result, ex: self.res.add_const(\"result\", \"no problem\")\n\
        print \"Hello World !\"\n\
\n\
\n\
class " + scriptname + "(Module):\n\
  def __init__(self):\n\
    Module.__init__(self, \"" + scriptname + "\", " + scriptname.upper() + ")\n\
    #Add your argument and tags here\n\
    #self.conf.add(\"filename\", \"node\")\n\
    #Add your const here\n\
    #self.conf.add_const(\"mime-type\", \"JPEG\")\n\
    #self.tags = \"test\"\n"
        return buff

    def generate_script_gui(self,  scriptname):
        buff = self.generate_header()
	buff += "from PyQt4 import QtCore, QtGui\n\
from PyQt4.QtCore import *\n\
from PyQt4.QtGui import *\n\
from api.module.module import *\n\
\n\
class " + scriptname.upper() + "(QTextEdit, Script):\n\
    def __init__(self):\n\
	#Module init stuff goes here\n\
	Script.__init__(self, \"" + scriptname + "\")\n\
\n\
    def c_display(self):\n\
	#You can add console display function here\n\
	#like ncurses func or others display func\n\
	print self.buff\n\
\n\
    def g_display(self):\n\
	#This function must init a QWidget\n\
	QTextEdit.__init__(self, None)\n\
        self.append(self.buff)\n\
\n\
\n\
    def updateWidget(self):\n\
	#you can put your refresh on resize func here\n\
	pass\n\
\n\
    def start(self, args):\n\
        #get your arg here, ex : args.get_node('filename')\n\
        #do some stuff, ex: print \"Hello\"\n\
	#you can set your state too, ex : self.stateinfo = \"Processing file\"\n\
        #return your result, ex: self.res.add_const(\"result\", \"no problem\")\n\
	self.buff = \"Hello world !\"\n\
\n\
class " + scriptname + "(Module):\n\
  def __init__(self):\n\
    Module.__init__(self, \"" + scriptname + "\"," + scriptname.upper() + ")\n\
    #Add your argument and tags here\n\
    #self.conf.add(\"filename\", \"node\")\n\
    #self.tags = \"test\"\n"
        return buff	


    def generate_drivers(self,  drivername):
        buff = self.generate_header()
        buff += "from api.vfs import *\n\
from api.module.module import *\n\
from api.type.libtype import *\n\
from api.vfs.libvfs import *\n\
from api.env.libenv import *\n\
from api.exceptions.libexceptions import *\n\
\n\
class " + drivername + "(Module):\n\
  def __init__(self):\n\
     Module.__init__(self, \"" + drivername + "\", " + drivername.upper() +")\n\
     self.conf.add(\"parent\", \"node\")\n\
     self.tags = \"fs\"\n\
     self.flags = [\"\"]\n\
\n\
\n\
class " + drivername.upper() + "(fso):\n\
   def __init__(self):\n\
      fso.__init__(self)\n\
      self.vfs = vfs.vfs()\n\
      self.name = \"" + drivername + "\"\n\
      setattr(self, \"vopen\", self.vopen)\n\
      setattr(self, \"vread\", self.vread)\n\
      setattr(self, \"vwrite\", self.vwrite)\n\
      setattr(self, \"vseek\", self.vseek)\n\
      setattr(self, \"vclose\", self.vclose)\n\
      self.res = results(self.name)\n\
    \n\
   def start(self, args):\n\
      self.parent = args.get_node('parent')\n\
      #you can use fdmanager\n\
      #self.fdm = fdmanager()\n\
      #self.fdm.InitFDM()\n\
      attr = attrib()\n\
      attr.thisown = 0\n\
      attr.size = len('Hello world!')\n\
      attr.handle = Handle(\"Hello\")\n\
      name = \"Hello\"\n\
      root = self.CreateNodeFile(self.parent, name, attr)\n\
\n\
   def vopen(self, handle):\n\
      #return fd or raise a vfsError\n\
      return 1\n\
    \n\
   def vread(self, fd, buff, size):\n\
      #return a tuple (size, buffer) where size is the number of bytes read\n\
      #on error raise a vfsError\n\
      buff = \"Hello world !\"\n\
      return (len(buff), buff)\n\
    \n\
   def vseek(self, fd,  pos, whence):\n\
      #return -1 for error or new offset position\n\
      return 0\n\
    \n\
   def vwrite(self, fd,  buff, size):\n\
      #raise a vfsError if you don't use this functions (forensic drivers)\n\
      raise vfsError(\"Can't write\")\n\
    \n\
   def vclose(self, fd):\n\
      #return 0 on success\n\
      return 0\n\
    \n\
   def status(self):\n\
      #return 0 if all fd are closed\n\
      return 0\n"
     
        return buff
