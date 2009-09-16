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

from PyQt4.QtGui import *
from PyQt4.QtCore import *

#from GScroll import *


class GView(QGraphicsView):
    def __init__(self, parent):
        QGraphicsView.__init__(self)
        self.heditor = parent
        self.touchdown = 0
        self.touchup = 0
        self.scroll = self.verticalScrollBar()
        self.initCallbacks()
                

    def initCallbacks(self):
        pass

    def scrollContentsBy(self, x, y):
        scroll = self.scroll

        if (scroll.value() == scroll.maximum()):
            self.touchdown += 1
            if ((self.heditor.CurrentSector < self.heditor.sectors) and (self.touchdown > 1)):
                self.heditor.CurrentOffset += self.heditor.sectorSize
                self.heditor.CurrentSector += 1
                self.heditor.readSector()
                self.touchdown = 0
                self.heditor.navigation.updateInformations()
                scroll.setSliderPosition(scroll.minimum() + 1)
        elif (scroll.value() == scroll.minimum()):
            self.touchup += 1
            if ((self.heditor.CurrentSector > 0) and (self.touchup > 1)):
                self.heditor.CurrentOffset -= self.heditor.sectorSize
                self.heditor.CurrentSector -= 1
                self.heditor.readSector()
                self.touchup = 0         
                self.heditor.navigation.updateInformations()
                scroll.setSliderPosition(scroll.maximum() - 1)
        self.viewport().update()


