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


import sys
import os
import getopt
from api.loader.loader import loader 
from console.console import console
from gui.gui import *
from redirect import RedirectIO
   
class ui():
  def __init__(self, type):
   self.type = type
   RedirectIO()
   self.modPath = sys.path[0] + "/modules/"

  def launch(self):
   if self.type == "gui":
     self.g = gui()
     self.g.launch(self.modPath)
   if self.type == "console":
     try :
      self.c.cmdloop()
     except AttributeError:
       loader().do_load(self.modPath)
       self.c = console()
       self.c.cmdloop()

  def cmd(self, command):
    try :
     self.c.onecmd(command) 
    except AttributeError:
     loader().do_load(self.modPath)
     self.c = console()
     self.c.onecmd(command) 

class usage():
   PROGRAM_USAGE = """DFF\nDigital Forensic Framework\n
Usage: """ + sys.argv[0] + """ [options]
Options:
  -g      --graphical                launch graphical interface
  -t      --test=NAME	             start a specific test
  -h,     --help                     display this help message
"""
   def __init__(self, argv):
     self.argv = argv
     self.graphical = 0
     self.test = ""
     self.main()

   def main(self):
    """Check command line argument"""
    try:
        opts, args = getopt.getopt(self.argv, "gdht:", [ "graphical",  "debug", "help", "test="])
    except getopt.GetoptError:
        self.usage()
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            self.usage()
        elif opt in ("-g", "--graphical"):
            self.graphical = 1
        elif opt in ("-t", "--test"):
            self.test = arg
    return

   def usage(self):
    """Show usage"""
    print self.PROGRAM_USAGE
    sys.exit(2)
