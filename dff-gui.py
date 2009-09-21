#!/usr/bin/python 
"""@package dff
Digital-forensic framework launcher
"""
import sys
import getopt
import os

graphical = 0
test = ""
operating_sys = ""
if os.name == "posix":  # It Checks OS
  try:
    import dl
    sys.setdlopenflags(sys.getdlopenflags() | dl.RTLD_GLOBAL)
  except ImportError:
      import ctypes
      sys.setdlopenflags(sys.getdlopenflags() | ctypes.RTLD_GLOBAL)
elif os.name == "nt":
    graphical = 0 

from api.exceptions import *
from api.type import *
from api.env import *
env = env.env()
from api.vfs import *
vfs = vfs.vfs()
from api.loader import *
loader = loader.loader()
from api.module import *

from ui.console.console import *
from ui.gui.gui import *
from test import *
from api.loader import *
from ui.redirect import RedirectIO

PROGRAM_USAGE = """DFF\nDigital Forensic Framework\n
Usage: """ + sys.argv[0] + """ [options]
Options:
  -g      --graphical                launch graphical interface
  -t      --test=NAME	             start a specific test
  -h,     --help                     display this help message
"""


def usage():
    print PROGRAM_USAGE
    sys.exit(2)

def main(argv):
    global graphical
def usage():
    """Show usage"""
    print PROGRAM_USAGE
    sys.exit(2)

def main(argv):
    """Check command line argument"""
    global graphical
    global test
    
    try:
        opts, args = getopt.getopt(argv, "w:gc:dht:", ["working-case=", "graphical", "config-file=", "debug", "help", "test="])
    except getopt.GetoptError:
        usage()
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
        elif opt in ("-g", "--graphical"):
            graphical = 1
        elif opt in ("-c", "--config-file"):
            conf = arg
            print conf
        elif opt in ("-w", "--working-case"):
            case = arg
        elif opt in ("-t", "--test"):
            test = arg
    return

def fg():
    """Launch shell loop"""
    c.cmdloop()

if __name__ == "__main__":
    """You can place some script command here for testing purpose"""
    main(sys.argv[1:])
    l = loader.loader()
    if os.name == "posix":
      l.do_load(sys.path[0] + "/modules/")
    else :
      l.do_load("modules/")
    c = console() 
    RedirectIO()
    gui()
