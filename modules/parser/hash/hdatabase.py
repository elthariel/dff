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

#import hashlib 
import sys
import string

from api.vfs import *
from api.module.script import *
from api.module.module import *

from api.exceptions.libexceptions import *
from api.vfs.libvfs import *

from modules.search.find import *

#----------------------------------------#
#Supported algorithm: sha1: 0, md5: 1 (readBase argument)
#Input: 
#Files or parse all tree?
#Configuration (NSRL database compatibility):
#parse fileRecord and get database's path
#"SHA-1","MD5","CRC32","FileName","FileSize","ProductCode","OpSystemCode","SpecialCode"
#----------------------------------------#

class HDATABASE(Script):
    def __init__(self):
        Script.__init__(self, "hdatabase")
        self.vfs = vfs.vfs() 

    def initValues(self):
        #NSRL Records
        self.os = []
        self.product = []
        self.file = []
        self.man = []
        #Hash list
        self.hmd5 = {}
        self.hsha = {}
    
    def loadConfiguration(self):
        try:
            f = open(self.conf,  'r')
            for line in f:
                if line[0] != '#':
                    split = line.split('=')
                    key = split[0]
                    path = split[1]
                    path = path.rstrip('\n')
                    if key == "osRecord":
                        self.os.append(path)
                    elif key == "fileRecord":
                        self.file.append(path)
                    elif key == "productRecord":
                        self.product.append(path)
                    elif key == "manRecord":
                        self.man.append(path)
            f.close()
        except IOError, (errno, strerror):
            print "loadConfiguration I/O error(%s): %s" % (errno, strerror)
    
    def setNodeInformations(self, node, name):
        map = node.attr.smap
        map["trust"] = '1'

    def readFileRecord(self):
        #Hash dictionary
        #Get keys (Hashs)
        sha = self.hsha.keys()
        md5 = self.hmd5.keys()
        #Read fileRecord in order to find hash
        if len(self.file) > 0:
            for cfile in self.file:
                try:
                    #print cfile, "test"
                    f = open(cfile, 'r')
                    for line in f:
                        #Split 
                        split = line.split(',')
                        #Check if line information is a NSRL size
                        if len(split) == 8: 
                        #parse sha1
                            for sh in sha:
                                if split[0] == sh:
                                    self.fillInformations(self.hsha[sh], split[3]) #Get node!
                            for mhd in md5:
                                if split[1] == mhd:
                                    self.fillInformations(self.hmd5[mhd], split[3]) #Get node!
                        
                    f.close()
                except IOError, (errno, strerror):
                    print "readBase I/O error(%s): %s" % (errno, strerror)

    def start(self, args):
        #Get arguments
        confpath = args.get_string("conf")
        pattern = args.get_string("pattern")
        
        #Load configuration
        self.conf = confpath
        self.initValues()
        self.loadConfiguration()

        fi = FIND()
        nodelist = fi.find(args)
        for node in nodelist:
            #Attribute map of node to be check
            map = node.attr.smap
            #Check if hash is enable
            #Check if Sha1 algo is set
            if "hash-sha1" in map:
                sha = map["hash-sha1"]
                #Add key: sha hash 
                self.hsha[sha] = node
            #If not, try MD5
            elif "hash-md5" in map:
                    md5 = map["hash-md5"]
                    #Add key: md5 hash 
                    self.hmd5[md5] = node
#Parse databases located in Configuration file
        self.readFileRecord()

class hdatabase(Module):
    def __init__(self):
        """
        Compare files hash in NSRL databases and tag it
        """
        Module.__init__(self, "hdatabase", HDATABASE)
        self.conf.add("conf", "string")
        self.conf.add("pattern", "string")
        self.tags = "parser"

