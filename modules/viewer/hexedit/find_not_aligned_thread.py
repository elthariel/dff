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

import struct

from PyQt4.QtGui import *
from PyQt4.QtCore import *

predef_args =  {"pattern": "",
                "count": 0,
                "from_offset": 0,
                "to_offset": 0,
                "type": "string",
                "endianess": "big",
                "node": None}

class PatternSearch(QThread):
    def __init__(self, node, parent, args = None):

        QThread.__init__(self)

        self.__node = node
        self.__pattern = predef_args["pattern"]
        self.__count = predef_args["count"]
        self.__from_offset = predef_args["from_offset"]
        self.__to_offset = predef_args["to_offset"]
        self.__type = predef_args["type"]
        self.__endianess = predef_args["endianess"]
        self.__buffersize = 8192

        self.stopit = False

        self.navigation = parent
        self.connect(self.navigation, SIGNAL("stopsearch () "), self.stops)
                
        if args != None:
            for item in predef_args.iterkeys():
                if item in args:
                    setattr(self, "_PatternSearch__" + item, args[item])
            for item in predef_args.iterkeys():
                print item, getattr(self, "_PatternSearch__" + item)
        self.__pattern_size = len(self.__pattern)
        #if self.__type == "hex":
        #    self.__pattern, = struct.unpack(str(self.__pattern_size) + "s", self.__pattern)


    def set(self, key, value):
        if key in predef_args:
            setattr(self, "_PatternSearch__" + key, value)
        if key == "pattern":
            self.__pattern_size = len(self.__pattern)

    def run(self):
        self.__search()
        #self.exec_()
        #return res


    def getResults(self):
        return self.res

    def stops(self):
        print "Thread stop"
        self.stopit = True


    def __search(self):
        results = []
        file = self.__node.open()
        file.seek(self.__from_offset)
        filebuff = file.read(self.__buffersize)

        #Progress dialog stuff
        progress_cur = 0
        progress_end = file.node.attr.size / self.__buffersize
        
        if progress_end == 0:
            progress_end = 1

        self.navigation.progressBar.setMinimum(progress_cur)
        self.navigation.progressBar.setMaximum(progress_end)


        self.stopit = False
        stop = False
        counted = 0
        current_pos = 0
        #print file.tell()
        while len(filebuff) != 0 and not stop:
            i = 0
            found = False

            while i != len(filebuff) and not stop:
                #print file.tell() + i
                #if self.__pattern[current_pos] != "?":
                if self.stopit == True:
                    self.res = results
                    self.emit(SIGNAL("setValue( int )"), progress_end)
                    self.emit(SIGNAL("progressTerminated()"))                            
                    self.exit()
                    return

                if filebuff[i] == self.__pattern[current_pos]:
                    current_pos += 1
                    if current_pos == self.__pattern_size:
                        pos = file.tell() - self.__buffersize + i - self.__pattern_size + 1
                        results.append(pos)
                        counted += 1
                        #print pos
                        current_pos = 0
                elif current_pos > 0:
                    i -= current_pos
                    current_pos = 0
                #else:
                #    current_pos += 1
                i += 1

                if self.__count > 0 and self.__count == counted:
                    stop = True

            self.emit(SIGNAL("setValue( int )"), progress_cur)

#            if progress.wasCanceled():
#                break;
            progress_cur += 1
#            progress.setValue(progress_cur)

            filebuff = file.read(self.__buffersize)

#        progress.setValue(progress_end)
        file.close()
        self.res = results
        self.emit(SIGNAL("setValue( int )"), progress_end)
        self.emit(SIGNAL("progressTerminated()"))               
        #return results

