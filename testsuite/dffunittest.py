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

# Appending previous directory, to package search path. Because tests are
# mostly run alone from top level source tree of DFF, we have to know this
# path to load modules (see below DffUnittest.setUp).
sys.path.insert(0, sys.path[0] + '/../')

if os.name == "posix":
   # Set propper library openning flags in case we are on a posix system.
   try :	
      import dl
      sys.setdlopenflags(sys.getdlopenflags() | dl.RTLD_GLOBAL)
   except ImportError:
      import ctypes
      sys.setdlopenflags(sys.getdlopenflags() | ctypes.RTLD_GLOBAL)
##@var graphical
# Tests shouldn't be run graphically.
graphical = 0


from ui.console.console import *
from api.loader import *
from api.vfs import vfs


class DffUnittest(unittest.TestCase):
    """@brief This is the main class driving DFF test environnement.

    DFF is loaded in a way it can be used with Python unittest package.
    Two objects are provided ;
     \e ui  to launch direct commands to DFF.
     \e vfs to access to low level interfaces of DFF.
    This class also provide propper output handling for validation.
    """
    def setUp(self):
        """ Initialize DFF framework in DffUnittest.

        Called by unittest runner just before running tests.
        Load DFF modules.
        Load console and avoid infinite loop like in shell mode.
        Redirect stdout and stderr to readable fileobjects, avoiding direct
        output.
        """
        sys.stdout = StringIO()
        sys.stderr = StringIO()

        # Obtain DFF loader
        l = loader.loader()
        # Hook outputs to avoid direct printing
        self.hook_streams(sys.__stdout__.fileno(), sys.__stderr__.fileno())
        # Load every DFF modules
        l.do_load('../modules/')
        # Restore outputs, handy for unittest status printing
        self.restore_streams()

        # Set console object for future use
        self.ui = console()

        # Set VFS object for future use
        self.vfs = vfs.vfs()
        
        # Close and = StringIO() again to drop ugly output from below
        sys.stdout.close()
        sys.stderr.close()
        sys.stdout = StringIO()
        sys.stderr = StringIO()

        
    def tearDown(self):
        """ Restore stdout and stderr before end of testsuite.

        Called by unittest at the end of the test suite.
        Set standard output and error output to original value,
        nativelly backuped in sys package.
        """
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

    def hook_streams(self, stdout, stderr):
        """ Avoid output of driver in current shell.

        These outputs are already hooked in DFF, see ui/redirect.py and
        ui/gui/widget/stdio.py.
        @bug In case of a C/C++ driver failure output will be lost.
        @param stdout Original standard output file descriptor.
        @param stderr Original error output file descriptor.
        """
        self._old_stdout = os.dup(stdout)
        self._old_stderr = os.dup(stderr)

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

    def restore_streams(self):
        """ Restore previously streamed outputs.

        Restore stdout and stderr for tests be able to display informations.
        Fetch stdout and stderr from driver.
        @return 4096 bytes from stdout and stderr in a tuple
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
        
        os.dup2(self._old_stdout, sys.__stdout__.fileno())
        os.dup2(self._old_stderr, sys.__stderr__.fileno())
        self._close(self._old_stdout, self._old_stderr,
                    self.driverOut, self.driverErr,
                    self.pipeOut[1], self.pipeErr[1],
                    self.pipeOut[0], self.pipeErr[0])

        return (readOut, readErr)

    def _set_nonblock(self, fileobj):
        """ Set a fileobject as nonblocking.

        @param fileobj An openened file object.
        """
        fd = fileobj.fileno()
        n = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, n|os.O_NONBLOCK)



    def _close(self, *fds):
        """ Close list of files.

        For each file listed we first try to close it like a file descriptor,
        if it fails we try to close it like a file object, if it fails again we
        skip, assuming it is already closed.
        @param *fds list of opened file descriptors or file objects.
        """
        for fd in fds:
            if type(fd) == file:
                fd.close()
            else:
                try:
                    os.close(fd)
                except:
                    pass

    # XXX ## Member data documentation need ##@var no Python docstring ...
    #  doxypy is unable to generate it and doxygen will ignore @var in """
    
    ##@var ui
    # Holds the console object, to launch command to DFF.

    ##@var vfs
    # Holds the VFS object, low level access to DFF framework.

    ##@var _old_stdout
    # Backups original standard output.

    ##@var _old_stderr
    # Backups original error output.

    ##@var pipeOut
    # File descriptor in a pipe holding standard output of framework.

    ##@var pipeErr
    # File descriptor in a pipe holding error output of framework.

    ##@var driverOut
    # Readable standard output of framework.

    ##@var driverErr
    # Readable error output of framework.
