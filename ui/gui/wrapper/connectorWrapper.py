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
#  Francois Percot <percot@gmail.com>
# 

import sys
import os

from api.vfs import *
from api.loader import *
from api.env import *
from api.script import *
from api.scheduler import *

from connectorCallback import ConnectorCallback

class ConnectorWrapper():
    def __init__(self,  mainWindow):
        self.__mainWindow = mainWindow
        self.vfs = vfs.vfs()
        self.env = env.env()
        self.loader = loader.loader()
        self.scheduler = scheduler.sched
        
    def initCallback(self):
        self.callback = ConnectorCallback(self.__mainWindow, self)
        
    def VFS_listingDirectoryWithVFSNODE(self, nodeDir):
        if nodeDir == False:
            return False
        listing = []
        list = nodeDir.next
        for i in list.size:
            if not i.next.empty():
                listing.append(i)
        return listing
    
    def VFS_listingDirectoryAndFiles(self, nodeDir):
        if nodeDir == False:
            return False
        if nodeDir.next.empty() and nodeDir.is_file:
            return False
        listing = []
        list = nodeDir.next
        for i in list:
            listing.append(i)
        return listing
    
    def VFS_getInfoDirectory(self,  node):
        list = node.next
        info = {}
        info['size'] = 0
        info['item'] = 0

        for i in list:
            if not i.next.empty() :
                info_child = self.VFS_getInfoDirectory(i)
                info['size'] = info['size'] + info_child['size']
                info['item'] = info['item'] + info_child['item'] + 1
            else :
                info['item'] = info['item'] + 1
                info['size'] = info['size'] + i.attr.size
        return info
 
    def getValuesInDb(self, vardb_name, type):
        value = []
        for i in self.env.vars_db:
            if str(i) == vardb_name:
                val = self.env.vars_db[i].val_l
                for v in val:
                    if v.type == type :
                        if v.type == "int":
                            value.append(v.get_int())
                        elif v.type == "string":
                            value.append(v.get_string())
                        elif v.type == "node": 
                            value.append(v.get_node())
        return value
