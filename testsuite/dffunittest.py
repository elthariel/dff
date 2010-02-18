#!/usr/bin/python 
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
#  Christophe M. <cma@digital-forensic.org>
#

import unittest, sys, os, fcntl
from cStringIO import StringIO

sys.path.insert(0, sys.path[0] + '/../')

if os.name == "posix": 
   try :	
      import dl
      sys.setdlopenflags(sys.getdlopenflags() | dl.RTLD_GLOBAL)
   except ImportError:
      import ctypes
      sys.setdlopenflags(sys.getdlopenflags() | ctypes.RTLD_GLOBAL)
elif os.name == "nt":
    graphical = 0 

from ui.console.console import *
from api.loader import *
from api.vfs import vfs


class DffUnittest(unittest.TestCase):
    def setUp(self):
        """ Initialize framework
        Load modules
        Load console without loop
        Redirect stdout and stderr to readable fileobjects
        """
        sys.stdout = StringIO()
        sys.stderr = StringIO()

        l = loader.loader()

        self._hook_streams(sys.__stdout__.fileno(), sys.__stderr__.fileno())
        l.do_load('../modules/')
        self._restore_streams()
        
        self.ui = console()
        
        self.vfs = vfs.vfs()
        
        # Close and re '.. = StringIO()' to drop output from modules loader
        sys.stdout.close()
        sys.stderr.close()
        sys.stdout = StringIO()
        sys.stderr = StringIO()

    def tearDown(self):
        """ Restore stdout and stderr before end of each
        tests
        """
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

    def _set_nonblock(self, fileobj):
        """ Set a fileobject non-blocking
        """
        fd = fileobj.fileno()
        n = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, n|os.O_NONBLOCK)

    def _hook_streams(self, stdout, stderr):
        """  Avoid output of driver in current shell
        """
        self.old_stdout = os.dup(stdout)
        self.old_stderr = os.dup(stderr)

        self.pipeOut = os.pipe()
        self.pipeErr = os.pipe()

        os.close(stdout)
        os.dup2(self.pipeOut[1], stdout)
        os.close(stderr)
        os.dup2(self.pipeErr[1], stderr)

        self.driverOut = os.fdopen(self.pipeOut[0])
        self.driverErr = os.fdopen(self.pipeErr[0])
        self._set_nonblock(self.driverOut)
        self._set_nonblock(self.driverErr)

    def _close(self, *fds):
        for fd in fds:
            if type(fd) == file:
                fd.close()
            else:
                try:
                    os.close(fd)
                except:
                    pass
        
    def _restore_streams(self):
        """ Restore stdout and stderr for tests be able to display informations
        Fetch stdout and stderr from driver and return both in a tuple
        """

        try:
            readOut = self.driverOut.read(4096)
        except:
            readOut = None
        try:
            readErr = self.driverErr.read(4096)
        except:
            readErr = None

        self.driverOut.flush()
        self.driverErr.flush()
        
        os.dup2(self.old_stdout, sys.__stdout__.fileno())
        os.dup2(self.old_stderr, sys.__stderr__.fileno())
        self._close(self.old_stdout, self.old_stderr,
                    self.driverOut, self.driverErr,
                    self.pipeOut[1], self.pipeErr[1],
                    self.pipeOut[0], self.pipeErr[0])

        return (readOut, readErr)

