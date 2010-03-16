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
#  Solal J. <sja@digital-forensic.org>
#

from api.vfs import *
from api.env import *
from api.exceptions.libexceptions import *

class Script(object):
    def __init__(self, name):
	self.name = name
        self.env = env.env()
        self.vfs = vfs.vfs()
	self.res = self.env.libenv.results(self.name)
	self.stateinfo = "" 
