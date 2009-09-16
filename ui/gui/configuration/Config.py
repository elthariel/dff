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

class DFF_Conf(object):
    __instance = None
    
    def __new__(self): 
        if self.__instance is None:
            self.__instance = object.__new__(self)
        return self.__instance
        
    def __init__(self):
        self.initLanguage()
        self.extractFolder = ""
        
    def initLanguage(self):
        try :
            fd = open('dff.conf',  'r')
        except IOError, (errno, strerror):
            self.language = "EN"
            return
        string = fd.readline()
        tab = string.split("=")
        self.language = str(tab[1])
        fd.close()
    
    def backupConfig(self, lConf):
        if lConf[0] == 0 :
            code_return = 0
        else :
            fd = open('dff.conf',  'w')
            code_return = 1
            if self.language == "FR" :
                self.language = "EN"
                fd.write("LANGUAGE=EN")
            else :
                self.language = "FR"
                fd.write("LANGUAGE=FR")
            fd.close()
        self.extractFolder = lConf[1]
        return code_return
