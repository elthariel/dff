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

import unittest, sys, os
from dffunittest import DffUnittest
from api.exceptions.libexceptions import *

class SeekTests(DffUnittest):
    """ Validate valid and invalid seek.

    """

    def __init__(self, name='runTest'):
        unittest.TestCase.__init__(self, name)

#FIXME What about windows ?
    testFile = "/etc/passwd"
    nonExistentFilePath = "/chifoumi/pouf/pif/paf"
    
    def test01_BadLocalOpen(self):
        """ #01 Output error when loading non existent filepath
        """

        # avoid output from driver loading in current stdout/stderr
        self._hook_streams(sys.__stdout__.fileno(), sys.__stderr__.fileno())

        # load an invalid path
        self.ui.onecmd('local --path ' + self.nonExistentFilePath + ' --parent /')

        # get output
        driverStdout, driverStderr = self._restore_streams()

        # validate output from framework
        self.assertEqual(sys.stdout.getvalue(), self.nonExistentFilePath + '\nValue error: local path < ' + self.nonExistentFilePath + " > doesn't exist\n")
        self.assertFalse(sys.stderr.getvalue())
        
        # validate output from driver loading (none)
        self.assertFalse(driverStdout)
        self.assertFalse(driverStderr)

    def test02_BadReadDirectory(self):
        """ #02 Raise error reading a directory for data
        """

        # avoid output from driver loading in current stdout/stderr
        self._hook_streams(sys.__stdout__.fileno(), sys.__stderr__.fileno())

        # load an valid filepath
        self.ui.onecmd('local --path ' + self.testFile + ' --parent /')

        # get output
        driverStdout, driverStderr = self._restore_streams()

        node = self.vfs.getnode('/')
        # Error must be raised if directory is not plugged to a data module
        self.assertRaises(vfsError, lambda: node.open())
        try:
            node.open()
        except vfsError, e:
            # Validate message raised by the exception
            self.assertEqual("Node::open(void) throw\nCan't Open file", e.error)

        # Last output, must be empty
        self.assertFalse(driverStderr)
        self.assertFalse(sys.stderr.getvalue())

    def test03_BadSeek0File(self):
        """ #03 Validate error raising : negative seek from 0
        """
        
        node = self.vfs.getnode(os.path.basename(self.testFile))
        f = node.open()
        # Seeking to a negative value must raise an exception
        self.assertRaises(vfsError, lambda: f.seek(-1, 0))
        try:
            f.seek(-1, 0)
        except vfsError, e:
            # Validate no message raised by the exception (FIXME)
            self.assertFalse(e.message)
               
    def test04_BadSeekNFile(self):
        """ #04 Validate NO error raising : negative seek -1 from +N
        """
        node = self.vfs.getnode(os.path.basename(self.testFile))
        f = node.open()
        
        # Get in the middle of the file
        f.seek(os.stat(self.testFile).st_size / 2)

        # Try to seek -1, have to work
        self.assertTrue(lambda: f.seek(-1, 1))

    def test05_BadSeekMaxFile(self):
        """ #05 Validate empty read starting at filesize
        """
        node = self.vfs.getnode(os.path.basename(self.testFile))
        f = node.open()
        f.seek(os.stat(self.testFile).st_size)
        self.assertFalse('', f.read(512))

        
suite = unittest.TestSuite()
suite.addTest(SeekTests('test01_BadLocalOpen'))
suite.addTest(SeekTests('test02_BadReadDirectory'))
suite.addTest(SeekTests('test03_BadSeek0File'))
suite.addTest(SeekTests('test04_BadSeekNFile'))
suite.addTest(SeekTests('test05_BadSeekMaxFile'))
res = unittest.TextTestRunner(verbosity=2).run(suite)

if (len(res.errors) or len(res.failures)):
    sys.exit(1)
