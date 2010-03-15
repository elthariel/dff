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
#  Jeremy Mounier <jmo@digital-forensic.org>
#

#import sys
#Is digit
#import re
import os


from PyQt4.QtCore import Qt, SIGNAL
from PyQt4.QtGui import QScrollBar, QAbstractSlider

class hexScrollBar(QScrollBar):
    def __init__(self, whex):
        QScrollBar.__init__(self)
        self.init(whex)
        self.initCallBacks()
#        self.setValues()

    def init(self, whex):
        self.whex = whex
        self.heditor = self.whex.heditor
        self.filesize = self.heditor.filesize
        self.min = 0
        self.single = 1
        #Initialized in Whex with LFMOD
        self.page = self.heditor.pageSize
        self.max = 0

        #Long File Mode
#        self.lfmod = False

        ###### LFMOD ######
        ###################
#        self.maxint = 2147483647
#        self.lines = self.filesize / self.heditor.bytesPerLine
#        self.restlines = self.filesize % 16
#        if self.isInt(self.lines):
#            self.max = self.lines - 1
#            self.page = self.heditor.pageSize / 16
#        else:
#            self.lfmod = True
#            self.max = self.maxint - 1
#            self.page = self.heditor.pageSize
        ####################
        ####################

    def initCallBacks(self):
        self.connect(self, SIGNAL("sliderMoved(int)"), self.moved) 
        self.connect(self, SIGNAL("actionTriggered(int)"), self.triggered) 

    def setValues(self):
        self.setMinimum(self.min)
        self.setMaximum(self.max)
        self.setSingleStep(self.single)
        self.setPageStep(self.page)
        self.setRange(self.min, self.max)

#    def isLFMOD(self):
#        return self.lfmod

#    def isInt(self, val):
#        try:
#            res = int(val)
#            if res <  2147483647:
#                return True
#            else:
#                return False
#        except ValueError, TypeError:
#            return False
#        else:
#            return False

    # LFMOD #
#    def valueToOffset(self, value):
#        return ((self.filesize * value) / self.maxint)

#    def offsetToValue(self, offset):
#        if self.isLFMOD():
#            return ((self.maxint * offset) / self.filesize)
#        else:
#            return (offset / self.heditor.bytesPerLine)

########################################
#          Navigation Operations       #
########################################

    def triggered(self, action):
        if action == QAbstractSlider.SliderSingleStepAdd:
            self.whex.view.move(self.singleStep(), 1)
        elif action == QAbstractSlider.SliderSingleStepSub:
            self.whex.view.move(self.singleStep(), 0)
        elif action == QAbstractSlider.SliderPageStepSub:
            self.whex.view.move(self.pageStep(), 0)
        elif action == QAbstractSlider.SliderPageStepAdd:
            self.whex.view.move(self.pageStep(), 1)


#    def oldtriggered(self, action):
#        offset = self.heditor.currentOffset
        #######################
        #        LINES        #
        #######################
        #LINE DOWN
#        if action == QAbstractSlider.SliderSingleStepAdd:
#            if offset + 16 <= (self.filesize - 5 * 16):
#                self.heditor.readOffset(offset + 16)
                #Update value
#                if self.isLFMOD():
#                    self.setValue(self.offsetToValue(offset + 16))
#                else:
#                    self.setValue(self.value() + 1)
        #LINE UP
#        elif action == QAbstractSlider.SliderSingleStepSub:
#            if offset - 16 >= 0:
#                self.heditor.readOffset(offset - 16)
#                #Update value
#                if self.isLFMOD():
#                    self.setValue(self.offsetToValue(offset - 16))
#                else:
#                    self.setValue(self.value() - 1)
        #######################
        #        PAGES        #
        #######################
        #PAGE UP
#        elif action == QAbstractSlider.SliderPageStepSub:
#            if offset - (self.page * 16) >= 0:
#                self.heditor.readOffset(offset - (self.page * 16))
#                #Update value
#                if self.isLFMOD():
#                    self.setValue(self.offsetToValue(offset - (self.page * 16)))
#                else:
#                    self.setValue(self.value() - self.page)
        #PAGE DOWN
#        elif action == QAbstractSlider.SliderPageStepAdd:
#            if offset + (self.page * 16) <= self.filesize - (5* 16):
#                self.heditor.readOffset(offset + (self.page * 16))
#                #Update value
#                if self.isLFMOD():
#                    self.setValue(self.offsetToValue(offset + (self.page * 16)))
#                else:
#                    self.setValue(self.value() + self.page)

    def moved(self, value):
        if self.whex.isLFMOD():
            if value <= self.max:
                offset = (self.filesize * value) / self.whex.maxint
                self.heditor.readOffset(offset)
        else:
            if value <= self.max:
                if value == self.max:
                    offset = self.filesize - (5 * self.heditor.bytesPerLine)
                else:
                    offset = value * self.heditor.bytesPerLine
                self.heditor.readOffset(offset)

