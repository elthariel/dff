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
#  Frederic B. <fba@digital-forensic.org>

from api.env import *
from api.env.libenv import *
from api.type.libtype import *
from api.module import *
from api.vfs.libvfs import *
from api.exceptions.libexceptions import *

from CARVER import *

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from typeSelection import *

import string

import time

from predef import predefPattern
from userdef import userPattern

from utils import QFFSpinBox

class worker(QThread):
    def __init__(self, **kwargs):
        QThread.__init__(self)
        self.args = kwargs["toCarve"]
        self.mapper = kwargs["mapper"]
        self.callback = kwargs["callback"]
        self.startOffset = kwargs["start"]
        self.aligned = kwargs["aligned"]

    def run(self):
        res = self.mapper(self.args, self.startOffset, self.aligned)
        self.callback()
        self.emit(SIGNAL("end(QString)"), QString(res))


class carvingProcess(QWidget, DEventHandler):
    def __init__(self):
        QWidget.__init__(self)
        DEventHandler.__init__(self)
        self.layout = QVBoxLayout()
        self.grid = QGridLayout()
        self.info = QVBoxLayout()
        self.layout.addLayout(self.grid)
        self.layout.addLayout(self.info)
        self.setLayout(self.layout)
        self.currentLabel = QLabel("Overall progress :")
        self.elapsedLabel = QLabel("elapsed time:    00d00h00m00s")
        self.estimatedLabel = QLabel("estimated time: 00d00h00m00s")
        self.totalLabel = QLabel("total headers found: 0")
        self.currentProgress = QProgressBar()
        self.grid.addWidget(self.currentLabel, 0, 0)
        self.grid.addWidget(self.currentProgress, 0, 1)
        self.info.addWidget(self.elapsedLabel)
        self.info.addWidget(self.estimatedLabel)
        self.info.addWidget(self.totalLabel)
        self.factor = 1
        self.parsetime = 0
        self.time = time.time()
        self.starttime = time.time()

    def strtime(self, day, hour, min, sec):
        day = str(day)
        hour = str(hour)
        min = str(min)
        sec = str(sec)
        res = "0" * (2-len(day)) + day + "d" + "0" * (2-len(hour)) + hour + "h" + "0" * (2-len(min)) + min + "m" + "0" * (2-len(sec)) + sec + "s"
        return res

    def timesec2str(self, timesec):
        day = hour = min = sec = 0
        if timesec > 3600 * 24:
            day = timesec / (3600 * 24)
            timesec = timesec % (3600 * 24)
        if timesec > 3600:
            hour = timesec / 3600
            timesec = timesec % 3600
        if timesec > 60:
            min = timesec / 60
            timesec = timesec % 60
        sec = timesec
        res = self.strtime(int(day), int(hour), int(min), int(sec))
        return res


    def Event(self, e):
        self.emit(SIGNAL("update"), e)


    def update(self, e):
        if e.type == SEEK:
            ref = time.time() - self.time
            self.time = time.time()
            if not str(ref).startswith("0.0"):
                ref *= self.parsetime
                res = self.timesec2str(ref)
                self.estimatedLabel.setText("estimated time: " + res)
            res = self.timesec2str(time.time() - self.starttime)
            self.elapsedLabel.setText("elapsed time:    " + res)
            i = int(e.seek / self.factor)
            if i > 2147483647:
                i = 2147483647
            self.emit(SIGNAL("valueChanged(int)"), i)
            info = self.currentProgress.text() + " - " + self.totalLabel.text()
            self.emit(SIGNAL("stateInfo(QString)"), info)
        else:
            self.totalLabel.setText("total headers found: " + str(e.seek))
            


    def doJob(self, **kwargs):
        self.kwargs = kwargs
        self.factor = kwargs["factor"]
        self.parsetime = kwargs["max"] / (10*1204*1024)
        self.elapsedLabel.setText("elapsed time:    00d00h00m00s")
        self.estimatedLabel.setText("estimated time: 00d00h00m00s")
        self.totalLabel.setText("total headers found: 0")
        maxrange = int(kwargs["max"] / self.factor)
        if maxrange > 2147483647:
            maxrange = 2147483647
        self.currentProgress.setRange(kwargs["min"], maxrange)
        self.currentProgress.setValue(0)
        self.workerThread = worker(**self.kwargs)
        self.connect(self.workerThread, SIGNAL("end(QString)"), self.end)
        self.connect(self, SIGNAL("valueChanged(int)"), self.currentProgress.setValue)
        self.time = time.time()
        self.starttime = time.time()
        self.workerThread.start()
        self.connect(self, SIGNAL("update"), self.update)

        
    def end(self, res):
        self.hide()
        self.emit(SIGNAL("end(QString)"), res)


    def killJob(self):
        e = DEvent()
        e.seek = 1
        e.type = SEEK
        self.notify(e)


class PyCarver(QWidget, fso):
    def __init__(self):
        fso.__init__(self)
        QWidget.__init__(self)
        self.name = "carver"
        self.res = results(self.name)
        self.carver = Carver()
        setattr(self, "vread", self.carver.vread)
        setattr(self, "vseek", self.carver.vseek)
        setattr(self, "vopen", self.carver.vopen)
        setattr(self, "vclose", self.carver.vclose)
        self.mapperFunc = getattr(self.carver, "process")
        self.addNodesFunc = getattr(self.carver, "AddNodes")
        self.tellFunc = getattr(self.carver, "tell")

    def start(self, args):
        self.carver.start(args)
        self.name += " <" + args.get_node("ifile").name + ">"
        self.filesize = args.get_node("ifile").attr.size


    def status(self):
        return 0


    def g_display(self):
        self.draw()
        

    def updateWidget(self):
        pass


    def startOffset(self):
        self.offsetLayout = QHBoxLayout()
        self.offsetSpinBox = QFFSpinBox(self)
        self.offsetSpinBox.setMinimum(0)
        self.offsetSpinBox.setMaximum(self.filesize)
        self.offsetLabel = QLabel("start offset:")
        self.offsetLayout.addWidget(self.offsetLabel)
        self.offsetLayout.addWidget(self.offsetSpinBox)

    def setStateInfo(self, sinfo):
        self.stateinfo = str(sinfo)

    def draw(self):
        #define layout
        self.vbox = QVBoxLayout()
        self.setLayout(self.vbox)

        #define all area
        #self.user = userPattern()
        self.pp = predefPattern()
        self.startButton = QPushButton("Start")
        self.stopButton = QPushButton("Stop")
        self.alignedCheck = QCheckBox("match only at the beginning of sector")
        self.startOffset()
        self.carvingProcess = carvingProcess()
        self.carver.connection(self.carvingProcess)
        self.carvingProcess.connection(self.carver)
        self.connect(self.carvingProcess, SIGNAL("stateInfo(QString)"), self.setStateInfo)
        
        #add widget and hide progress bars
        self.vbox.addWidget(self.pp)
        #self.vbox.addWidget(self.user)
        self.vbox.addLayout(self.offsetLayout)
        self.vbox.addWidget(self.alignedCheck)
        self.vbox.addWidget(self.startButton)
        self.vbox.addWidget(self.stopButton)
        self.vbox.addWidget(self.carvingProcess)
        self.carvingProcess.hide()
        self.stopButton.setEnabled(False)

        #define connectors
        self.connect(self.stopButton, SIGNAL("clicked()"), self.stopCarving)
        self.connect(self.startButton, SIGNAL("clicked()"), self.startCarving)
        self.connect(self.carvingProcess, SIGNAL("end(QString)"), self.carvingEnded)


    def carvingEnded(self, res):
        results = str(res).split("\n")
        print results
        for item in results:
            begidx = item.find(":")
            self.res.add_const(str(item[:begidx]), str(item[begidx+1:] + "\n"))
        self.startButton.setEnabled(True)
        self.stopButton.setEnabled(False)


    def stopCarving(self):
        self.carvingProcess.killJob()
        self.stopButton.setDown(True)


    def createContext(self, selected):
        toCarve = listDescr()
        toCarve.thisown = False
        for key, items in selected.iteritems():
            for item in items:
                descr = filetypes[key][item]
                for p in descr:
                    header = pattern()
                    footer = pattern()
                    header.thisown = False
                    footer.thisown = False
                    header.needle = p[0]
                    header.size = len(p[0])
                    footer.needle = p[1]
                    footer.size = len(p[1])
                    if p[0].find(wildcard) != -1 or p[1].find(wildcard) != -1:
                        header.wildcard = wildcard
                        footer.wildcard = wildcard
                    else:
                        header.wildcard = ""
                        footer.wildcard = ""
                    d = description()
                    d.thisown = False
                    d.header = header
                    d.footer = footer
                    d.type = item
                    d.window = p[2]
                    d.aligned = False
                    toCarve.append(d)
        return toCarve
        

    def startCarving(self):
        self.startButton.setEnabled(False)
        self.stopButton.setEnabled(True)
        self.stopButton.setDown(False)
        selected = self.pp.getChecked()
        toCarve = self.createContext(selected)
        factor = round(float(self.filesize) / 2147483647)
        if factor == 0:
            factor = 1
        carvingArgs = {"min": 0, "max": self.filesize, "toCarve": toCarve, 
                       "callback": self.addNodesFunc, "mapper": self.mapperFunc,
                       "factor": factor, "start": self.offsetSpinBox.value(),
                       "aligned": self.alignedCheck.isChecked()}
        self.carvingProcess.show()
        self.carvingProcess.doJob(**carvingArgs)


class interface(Module):
  def __init__(self):
    Module.__init__(self, 'carver', PyCarver)
    self.conf.add("ifile", "node")
    self.tags = "search"
