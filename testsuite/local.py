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

import unittest, sys, os, random
from dffunittest import DffUnittest

class LocalTests(DffUnittest):
    """@brief Tests on 'local' DFF driver.

    Local driver simply maps a file, or a directory, from the host computer to
    DFF.
    We load several things, and validate basic functionality of the framework.
    Keep in mind that VFS loads are persistant from one single test of this
    class to another.
    @todo
    - Open & close many files and check fd reallocation
    - Load same file two times, open both, seek one, check both position are OK
    - What about a file present on every windows systems ?
    """
    
    ##@var _testFile
    # A file present on every Unix systems
    _testFile = '/etc/passwd'

    def __init__(self, name='runTest'):
        """ Init parent package """
        unittest.TestCase.__init__(self, name)

    def test01_LoadOneFile(self):
        """ #01 Load a file present on every Unix.
        """
        
        # avoid output from driver loading in current stdout/stderr
        self.hook_streams(sys.__stdout__.fileno(), sys.__stderr__.fileno())
        
        # launch command
        self.ui.onecmd('local --path ' + self._testFile + ' --parent /')
        
        # get output
        driverStdout, driverStderr = self.restore_streams()

        # validate output from driver loading
        self.assertFalse(driverStdout)
        self.assertFalse(driverStderr)
        
        # validate output from framework
        self.assertEqual(sys.stdout.getvalue(), self._testFile + '\nresult:\n\
no problem\n')
        self.assertEqual(sys.stderr.getvalue(), '')

    def test02_LsOneFile(self):
        """ #02 ls previously loaded file and validate size.
        
        Check if --long (switch for size output) outputs right size of the
        file.
        """
        
        self.ui.onecmd('ls --long /')
        
        fileSize = str(os.stat(self._testFile).st_size)
        expectedStdout = '/' + os.path.basename(self._testFile) + '\t' + \
                         fileSize + '\n'

        self.assertEqual(sys.stdout.getvalue(), expectedStdout)
        self.assertEqual(sys.stderr.getvalue(), '')
        
    def test03_LoadOneDirectory(self):
        """ #03 Load current working directory and validate number of files
        loaded.
        
        Make sure number of nodes loaded is the same number as number of file
        stored in current working directory.
        """

        testDirectory = os.getcwd()
        self.hook_streams(sys.__stdout__.fileno(), sys.__stderr__.fileno())
        self.ui.onecmd('local --path ' + testDirectory + ' --parent /')
        driverStdout, driverStderr = self.restore_streams()

        expectedItems = str(self._itemsCount(os.getcwd()))
        # Expected output after local execution
        expectedStdout = testDirectory + '\nnodes created:\n' + expectedItems \
                         + '\nresult:\nno problem\n'

        # Get number of nodes created, for message if first assert below failed
        countPosStart = sys.stdout.getvalue().rfind('created:\n') + \
                        len('created:\n')
        countPosEnd = sys.stdout.getvalue().find('\n', countPosStart)
        loadedItems = sys.stdout.getvalue()[countPosStart:countPosEnd]

        # validate output from driver loading
        self.assertFalse(driverStdout)
        self.assertFalse(driverStderr)
        
        # validate output from framework
        self.assertEqual(sys.stdout.getvalue(), expectedStdout, "maybe hidden \
        files exist in " + os.getcwd() + " (directory loaded by this test, \
        expected: " + expectedItems + " items, loaded: " + loadedItems + ")")
        self.assertFalse(sys.stderr.getvalue())
        
    def test04_ReadFile(self):
        """ #04 Read 128 byte in previously loaded file.
        
        Make sure content on disk and in vfs are the same.
        """
        readAmount = 128
        
        with open(self._testFile, 'r') as f:
            expectedContent = f.read(128)

        checknode = self.vfs.getnode('/passwd')

        nodeFile = checknode.open()
        buff = nodeFile.read(128)
        self.assertEqual(expectedContent, buff)

    def test05_RandomReadFile(self):
        """ #05 Randomly check 100 file content.
        
        Read 'randomReadSize' from beginning of file and make sure
        same content is obtained from disk and from VFS.
        """

        checkAmount = 100
        while checkAmount:
            # Obtain a random filepath from given directory
            randomFilepath = self._randomItem(os.getcwd())
            # Compute a random size to read
            randomReadSize = int(random.random() * \
                                 os.stat(randomFilepath).st_size)
            # Open reference file
            with open(randomFilepath, 'r') as f:
                # Save reference data
                expectedContent = f.read(randomReadSize)
                # Set node path according to VFS format
                vfsNodePath = '/' + randomFilepath[len(os.getcwd()) - \
                                                   len(os.path.basename(\
                                                       os.getcwd())):]
                # Open node file
                nodeFile = self.vfs.getnode(vfsNodePath).open()
                # Save rode date from VFS
                buff = nodeFile.read(randomReadSize)
                # Close node file
                nodeFile.close()
                # Compare both data
                self.assertEqual(expectedContent, buff)
                # Reference file is automatically close ; 'with' statement
            checkAmount -= 1

    def _itemsCount(self, path, onlyFiles = False):
        """ Count amount of file in a given directory.

        We can count only files or directories plus files, this is useful
        for _randomItem below.
        @param path Path to a directory on the filesystem, where to count.
        @param onlyFiles If set, return only files count, no directory.
        @return Amount of items.
        """
        itemsCount = 0
        for root, dirs, files in os.walk(path):
            if onlyFiles:
                itemsCount += len(files)
            else:
                itemsCount += len(dirs) + len(files)
        return itemsCount

    def _randomItem(self, path):
        """ Select a random file in a given directory.

        @param path Path to a directory on the filesystem.
        @return A string holding the path to a random file
        """
        # Count number of files
        itemsCount = self._itemsCount(path, True)
        randomItemPosition = 0
        while randomItemPosition == 0 or randomItemPosition > itemsCount:
            # Set a random index
            randomItemPosition = int(random.random() * itemsCount)
        i = 0
        for root, dirs, files in os.walk(path):
            j = 0
            # Walk to this random index
            for j in range(len(files)):
                i += 1
                if i == randomItemPosition:
                    # Random index found, returning file path string
                    return root + '/' + files[j]


##@var suite
# Object collecting tests to be run.
suite = unittest.TestSuite()
suite.addTest(LocalTests('test01_LoadOneFile'))
suite.addTest(LocalTests('test02_LsOneFile'))
suite.addTest(LocalTests('test03_LoadOneDirectory'))
suite.addTest(LocalTests('test04_ReadFile'))
suite.addTest(LocalTests('test05_RandomReadFile'))

##@var res
# Holds the test results to exit with an error if needed
res = unittest.TextTestRunner(verbosity=2).run(suite)

if (res.errors or res.failures):
    # Something goes wrong, exiting with an error
    sys.exit(1)
