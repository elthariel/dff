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

class map_gif:
    def __init__(self, length):
        self.sof = length
        self.eof = -1

class carv_gif:
    def __init__(self):
        self.__list_file = []
	self.vfs = vfs.vfs()

    def find(self, node):
        file = node.open()
        size = file.node.attr.size
        test = file.read(5)
        i = 1
        while test:
            if size * i == file.tell():
                i += 1
            test += file.read(1)
            if test == 'GIF87a' or test == 'GIF89a':
                self.__list_file.append(map_gif(file.tell() - 6))
            elif test[0:2] == '\x00\x3b' and len(self.__list_file):
                self.__list_file[len(self.__list_file) - 1].eof = file.tell() - 4
            test = test[1:]
        file.close()
        return self.__list_file

    def create(self, node, nfilename, list_file):
        nb = 0
        file = node.open()
        while len(list_file):
            x = list_file.pop()
            if x.eof != -1:
                file.seek(x.sof)
		new = nfilename + "%s.gif" % nb
                o = TOUCH()
                nfile = o.touch(new)
		nfile = self.vfs.open(new)
                nfile.write(file.read(x.eof - x.sof))
                nfile.close()
                nb += 1
	file.close()
