#!/usr/bin/python -i
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

"""@package dff
Digital-forensic framework launcher
"""
import os, sys, getopt

if os.name == "posix": 
    try :
        import dl
        sys.setdlopenflags(sys.getdlopenflags() | dl.RTLD_GLOBAL)
    except ImportError:
        import ctypes
        sys.setdlopenflags(sys.getdlopenflags() | ctypes.RTLD_GLOBAL)

from api.manager.manager import ApiManager
from ui.ui import ui, usage

def fg():
    """Launch shell loop"""
    global ui
    ui.c.cmdloop()

if __name__ == "__main__":
    """You can place some script command here for testing purpose"""
    argv = usage(sys.argv[1:])
    ui = ui('gui')
    ui.launch()
