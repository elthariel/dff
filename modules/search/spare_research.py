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

import os
import traceback
import struct

import sys

#import progress_bar

#from utils import *

import threading

import string

from api.vfs import *
from api.module.module import *
from api.module.script import *

from PyQt4.QtGui import QLabel, QVBoxLayout, QHBoxLayout, QTabWidget, QTreeWidget, QTreeWidgetItem, QWidget, QColor, QFont, QSplitter, QFrame, QApplication
from PyQt4.QtCore import Qt, QString


# K600
#-------------------------------------------------------------
#00040000   38 C7 F9 20  88 F7 F9 20  00 00 04 20  00 00 02 00
#00080010   00 00 D0 E5  EE 00 50 E3  00 00 08 20  00 00 02 00
#00120020   00 10 C2 05  04 C0 80 05  0D 00 00 0A  08 30 90 E5
#000C0020   00 00 50 E3  0C 00 9D E5  00 00 0C 20  00 00 02 00
#00100030   00 21 9B E7  04 10 94 E5  00 00 10 20  00 00 02 00
#00140040   01 01 80 E0  04 C0 82 E5  00 00 14 20  00 00 02 00
#011C0460   7C 03 0B 3E  7C 03 0F 6E  00 00 1C 21  00 00 02 00

#premier FFFF5412 --> 0x40000 + (0x40010 * 88)

#TODO recherche en fin de bloc !!!!!!!!

"dffmod"

class QTab(QTabWidget):
    def __init__(self):
        QTabWidget.__init__(self, None)
        self.splitters = {}
 
    def add_tab(self, name):
        self.splitters[name] = splitter = QSplitter(Qt.Vertical)
        self.addTab(splitter, name)

    def add_widget(self, tab, widget, title = None):
        widget = TitledWidget(widget, title)
        self.splitters[tab].addWidget(widget)
        pass

class TitledWidget(QFrame):
    def __init__(self, widget, title = None):
        QFrame.__init__(self, None)
        self.widget = widget
        self.title = title
        self.__create()
        
    def __create(self):
        self.setFrameShape(0x0016)
        self.setContentsMargins(0, 0, 0, 0)
        vbox = QVBoxLayout()
        vbox.setContentsMargins(0, 0, 0, 0)
        if self.title != None:
            vbox.addWidget(QLabel(self.title), 0, Qt.AlignHCenter)
        vbox.addWidget(self.widget)
        self.setLayout(vbox)


class SpareMapping():
    
    def __init__(self, node, type, where, skip = 0, sparesize = 0x10):
        self.node = node
        self.file = self.node.open()
        self.type = type
        self.where = where
        self.skip = skip
        self.sparesize = sparesize
        self.allocated = 0
        self.filesize = node.attr.size
        self.spares = {}
        self.spares["interval"] = {}

        for interval in [0x200, 0x1000, 0x2000, 0x4000, 0x10000, 0x20000, 0x40000]:
            self.map_spare(interval)


    """
    Description:
    count occurence of byte found at a given position inside the spare

    Prototype:
    interval: gives the interval between one spare and another
    type: the type of spare. aligned means inside the block. not aligned means outside the block
    where: the position of the spare area of the current block ?
    """
    def map_spare(self, interval):

        if self.where == "end":
            if self.type == "naligned":
                file.seek(interval)
            else:
                file.seek(interval - self.sparesize)
        else:
            file.seek(0)        
        end = file.tell()
        while end < self.filesize:
            spare = file.read(self.sparesize)
            if (spare != ("\xff" * self.sparesize)) and (spare != ("\x00" * self.sparesize)):
                i = 0
                allocated += 1
                while i != self.sparesize:
#                    if i not in self.:
 #                       spare_bytes_occurence[i] = {}
                    byte, = struct.unpack("B", spare[i:i+1])
                    if byte not in spare_bytes_occurence[i]:
                        spare_bytes_occurence[i][byte] = 0
                    spare_bytes_occurence[i][byte] += 1
                    i += 1
            if type == "naligned":
                file.seek(interval, 1)
                end = file.tell() + interval + self.sparesize
            else:
                file.seek(interval - self.sparesize, 1)
                end = file.tell() + interval
        file.close()
        return spare_bytes_occurence, allocated    
    

"""
This class is only used for the graphical rendering
No processing is done inside
"""
class GuiSpareResearch(QWidget, Script):

    def __init__(self):
        Script.__init__(self, "spare_research")
        self.type = "search"
        self.icon = None

    def start(self, args):
        self.infile = args.get_node("infile")
        self.sparesize = args.get_int("sparesize")
        print self.sparesize
        #self.eraseblocksize = args.get_int("blocksize")
        #self.magics = {}
        #self.spare = {}
        self.filesize = self.infile.attr.size
        self.occurences = {}
        self.occurences["aligned"] = {}
        self.occurences["aligned"]["start"] = {}
        self.occurences["aligned"]["end"] = {}
        self.occurences["naligned"] = {}
        self.occurences["naligned"]["start"] = {}
        self.occurences["naligned"]["end"] = {}
        
        for type in self.occurences.iterkeys():
            print type
            for where in self.occurences[type].iterkeys():
                print " ", where
                for interval in [0x200, 0x1000, 0x10000, 0x20000, 0x40000]:
                    print " " * 3, interval
                    self.occurences[type][where][interval], self.occurences[type][where][interval]["allocated"] = self.map_spare(interval, type, where)
        
        self.guess_spare()

    def g_display(self):
        QWidget.__init__(self, None)
        hbox = QHBoxLayout(self)
        self.setLayout(hbox)

        self.trees = {}

        tab = QTab()
        tab.add_tab("aligned spare")
        tab.add_widget("aligned spare", self.fill_spare_tree(self.occurences["aligned"]["start"]), "spare at the beginning of blocks")
        tab.add_widget("aligned spare", self.fill_spare_tree(self.occurences["aligned"]["end"]), "spare at the end of blocks")

        tab.add_tab("not aligned spare")
        tab.add_widget("not aligned spare", self.fill_spare_tree(self.occurences["naligned"]["start"]), "spare before the beginning of blocks")
        tab.add_widget("not aligned spare", self.fill_spare_tree(self.occurences["naligned"]["end"]), "spare after the end of blocks")
        
        hbox.addWidget(tab)

    def fill_spare_tree(self, occurences):
        spare_tree = QTreeWidget()
        spare_tree.setColumnCount(2)
        headerLabel = [QApplication.translate("GuiMagicFinder", "spare", None, QApplication.UnicodeUTF8),
        QApplication.translate("GuiMagicFinder", "found", None, QApplication.UnicodeUTF8)] 
        spare_tree.setHeaderLabels(headerLabel)
        spare_tree.setAlternatingRowColors(True)
 
        #iteration on interval
        for key in occurences.iterkeys():
            current_interval = occurences[key]
            cint_item = QTreeWidgetItem(spare_tree) 
            cint_item.setText(0, str(hex(key)))
            cint_item.setText(1, str(occurences[key]["allocated"]))

            #iteration on position in spare content
            for position_key in current_interval.iterkeys():
                try:
                    position_bytes = current_interval[position_key]
                    pos_item = QTreeWidgetItem(cint_item)
                    pos_item.setText(0, str(hex(position_key)) + " - " + str(hex(position_key + 1)))
                    pos_item.setText(1, str(len(current_interval[position_key])))
                #iteration on bytes found
                    for byte in position_bytes.iterkeys():
                        byte_item = QTreeWidgetItem(pos_item)
                        byte_item.setText(0, str(hex(byte)))
                        byte_item.setText(1, str(position_bytes[byte]))
                except:
                    pass

        return spare_tree


    def updateWidget(self):
        pass
        

    def guess_spare(self):
        #possible_valid_spare
        #aligned / not aligned	
        for type in self.occurences.iterkeys():
            # start / end
            for where in self.occurences[type].iterkeys():
                # interval
                for interval in [0x200, 0x1000, 0x10000, 0x20000, 0x40000]:
                    #position
                    for position in self.occurences[type][where][interval].iterkeys():
		      try :	
                        if len(self.occurences[type][where][interval][position]) < 5:
                            print type, where, hex(interval)
                        for bytes in self.occurences[type][where][interval][position].iterkeys():
                            percent = (self.occurences[type][where][interval][position][bytes] * 100) / (self.filesize / interval)
                            if len(self.occurences[type][where][interval][position]) < 5:
                                print type, where, hex(interval), self.occurences[type][where][interval][position][bytes], "/", self.filesize / interval, "=", percent
                            if percent > 60:
                                print type, where, hex(interval), self.occurences[type][where][interval][position][bytes], "/", self.filesize / interval, "=", percent
		      except :
			 pass



    """
    Description:
    count occurence of byte found at a given position inside the spare

    Prototype:
    interval: gives the interval between one spare and another
    type: the type of spare. aligned means inside the block. not aligned means outside the block
    where: the position of the spare area of the current block ?
    """
    def map_spare(self, interval, type, where):
        file = self.infile.open()
        spare_bytes_occurence = {}

        if where == "end":
            if type == "naligned":
                file.seek(interval)
            else:
                file.seek(interval - self.sparesize)
        else:
            file.seek(0)

        end = file.tell()
        allocated = 0
        while end < self.filesize:
            spare = file.read(self.sparesize)
            if (spare != ("\xff" * self.sparesize)) and (spare != ("\x00" * self.sparesize)):
                i = 0
                allocated += 1
                while i != self.sparesize:
                    if i not in spare_bytes_occurence:
                        spare_bytes_occurence[i] = {}
                    byte, = struct.unpack("B", spare[i:i+1])
                    if byte not in spare_bytes_occurence[i]:
                        spare_bytes_occurence[i][byte] = 0
                    spare_bytes_occurence[i][byte] += 1
                    i += 1
            if type == "naligned":
                file.seek(interval, 1)
                end = file.tell() + interval + self.sparesize
            else:
                file.seek(interval - self.sparesize, 1)
                end = file.tell() + interval
        file.close()
        return spare_bytes_occurence, allocated


class spare_research(Module):
    def __init__(self):
        Module.__init__(self, "spare_research", GuiSpareResearch)
        self.conf.add("infile", "node")
        #self.conf.add("magicsize", "int")
        self.conf.add("sparesize", "int", True)
        self.conf.add_const("sparesize", 0x10)
        self.conf.add_const("sparesize", 0x20)
        self.conf.add_const("sparesize", 0x40)
        self.tags = "search"
