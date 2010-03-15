# DFF -- An Open Source Digital Forensics Framework
# Copyright (C) 2009-2010 ArxSys
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

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *


from api.vfs import *
from api.module.module import *
from api.module.script import *
from api.loader import *
from api.env import *

class MAN(QWidget, Script):
    def __init__(self):
        Script.__init__(self, "man")
        self.type = "man"
        self.loader = loader.loader()
        self.lmodules = self.loader.modules


    def get_val(self, arg):
        val = ""

        if arg.type == "string":
            val = arg.get_string()
        elif arg.type == "int":
            val = str(arg.get_int())
        elif i.type == "node" and i.get_node() :
            val = arg.get_node().path + "/" + arg.get_node().name
        return val

    def start(self, args):        
        self.module = args.get_string("module")
        if self.module in self.lmodules:
            mod = self.lmodules[self.module]
            conf = mod.conf
            cdl = mod.conf.descr_l
            cvl = mod.conf.val_l
            self.fres = "NAME\n\t"
            self.fres += self.module + " - " + conf.description + "\n\n"
            self.fres += "SYNOPSIS\n"
            self.fres += "\t" + self.module + "[OPTION]...\n\n"
            self.fres += "DESCRIPTION\n"
            for arg in cdl:
                self.fres += "\n\t"
                self.fres += "--" + arg.name + "  ( type: " + arg.type
                if arg.optional:
                    self.fres += ", optional )"
                else:
                    self.fres += ", required )"
                self.fres += "\n\t\t" + arg.description
                if cvl.size() > 0:
                    first = True
                    init = False
                    for val in cvl:
                        if val.name == arg.name:
                            fval = self.get_val(val)
                            if fval != "":
                                if init == False:
                                    init = True
                                    self.fres += "\n\t\tpredefined value(s): " + fval
                                else:
                                    self.fres += ", " + fval
                self.fres += "\n"

        else:
            self.fres = "no entry for module: " + self.module


    def g_display(self):
        QWidget.__init__(self, None)
        hbox = QHboxLayout()
        self.setLayout(hbox)
        

    def updateWidget(self):
        pass


    def c_display(self):
        print self.fres
        pass


class man(Module):
    def __init__(self):
        Module.__init__(self, "man", MAN)
        self.conf.description = "man display help on other module"
        self.conf.add("module", "string", True, "corresponds to the module you want help")
        self.tags = "help"
