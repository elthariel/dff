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
#  Solal Jacob <sja@digital-forensic.org>
# 

from modules.fs.shm.touch import *
from api.vfs import *

class map_jpeg:
    def __init__(self, length):
        self.sof = length
        self.soi = -1
        self.eof = -1

class carv_jpeg:
    def __init__(self):
	self.vfs = vfs.vfs()
        self.__list_file = []

    def find(self, node):
        file = node.open()
        test = file.read(3)
        while test:
            test += file.read(1)
            if test == '\xff\xd8\xff\xe1' or test == '\xff\xd8\xff\xe0':
                self.__list_file.append(map_jpeg(file.tell() - 4))
            elif test[0:2] == '\xff\xda' and len(self.__list_file):
                self.__list_file[len(self.__list_file) - 1].soi = file.tell() - 2
            elif test[0:2] == '\xff\xd9' and len(self.__list_file):
                self.__list_file[len(self.__list_file) - 1].eof = file.tell() - 2
            test = test[1:]
        file.close()
        return self.__list_file

    def create(self, node, nfilename, list_file):
        nb = 0
        file = node.open()
        while len(list_file):
            x = list_file.pop()
            if (x.soi != -1) and (x.eof != -1):
                file.seek(x.sof)
                new = nfilename + "%s.jpg" % nb
                o = TOUCH()
                nfile = o.touch(new)
                nfile = self.vfs.open(new)
                nfile.write(file.read(x.eof - x.sof))
                nfile.close()
		nb += 1
        file.close()
