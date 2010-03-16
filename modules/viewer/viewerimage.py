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
from PyQt4.QtCore import Qt, QSize, QString, SIGNAL, QThread
from PyQt4.QtGui import QPixmap, QImage, QPushButton, QLabel, QWidget, QHBoxLayout, QVBoxLayout, QScrollArea, QIcon, QMatrix

from api.vfs import *
from api.module.module import *
from api.module.script import *
from api.magic.filetype import FILETYPE

import sys
import time
import re


class QRotateButton(QPushButton):
  def __init__(self, angle, icon):
    QPushButton.__init__(self, QIcon(QString(icon)), "")
    self.angle = angle

  def mousePressEvent(self, event):
    self.animateClick()
    self.emit(SIGNAL("clicked"), self.angle)


class QZoomButton(QPushButton):
  def __init__(self, zoom, icon):
    QPushButton.__init__(self, QIcon(QString(icon)), "")
    self.zoom = zoom


  def mousePressEvent(self, event):
    self.animateClick()
    self.emit(SIGNAL("zoomed"), self.zoom)


class LoadedImage(QLabel):
  def __init__(self):
    QLabel.__init__(self)
    #self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
    self.node = None
    self.angle = 0
    self.factor = 1
    self.imgWidth = 0
    self.baseImage = QImage()
    self.cpixmap = QPixmap()
    self.matrix = QMatrix()


  def load(self, node, type):
    self.node = node
    file = self.node.open()
    buff = file.read()
    file.close()
    self.baseImage.loadFromData(buff, type)


  def adjust(self, imgwidth):
    self.imgWidth = imgwidth
    self.currentImage = self.baseImage.scaled(QSize(self.imgWidth, self.imgWidth), Qt.KeepAspectRatio, Qt.FastTransformation)
    self.setPixmap(QPixmap.fromImage(self.currentImage))
    self.adjustSize()


  def resize(self, zoomer):
    w = self.currentImage.width() * zoomer
    self.currentImage = self.baseImage.scaled(QSize(w, w), Qt.KeepAspectRatio, Qt.FastTransformation)
    self.setPixmap(QPixmap.fromImage(self.currentImage))
    self.adjustSize()


  def rotate(self, angle):
    matrix = QMatrix()
    matrix.rotate(angle)
    self.currentImage = self.currentImage.transformed(matrix)
    self.baseImage = self.baseImage.transformed(matrix)
    self.setPixmap(QPixmap.fromImage(self.currentImage))
    self.adjustSize()


  def fitbest(self):
    self.currentImage = self.baseImage.scaled(QSize(self.imgWidth, self.imgWidth), Qt.KeepAspectRatio, Qt.FastTransformation)
    self.setPixmap(QPixmap.fromImage(self.currentImage))
    self.adjustSize()


  def notSupported(self):
    #self.setPixmap(None)
    self.setText("Format Not Supported")
    self.adjustSize()

class Metadata(QWidget):
  def __init__(self):
    QWidget.__init__(self)


import time


#class SortImages(QThread):
#  def __init__(self):
#    QThread.__init__(self)
#    self.images = {}
#    self.ft = FILETYPE()
#    self.reg_viewer = re.compile(".*(JPEG|JPG|jpg|jpeg|GIF|gif|bmp|BMP|png|PNG|pbm|PBM|pgm|PGM|ppm|PPM|xpm|XPM|xbm|XBM).*", re.IGNORECASE)


#  def getImageType(self, node):
#    type = None

#    if node.attr.size != 0:
#      map = node.attr.smap
#      try:
        #XXX temporary patch for windows magic
#        f = node.attr.smap["type"]
#      except IndexError:
#        #XXX temporary patch for windows magic
#        self.ft.filetype(node)
#        f = node.attr.smap["type"]
#        res = self.reg_viewer.match(f)
#        if res != None:
#          type = f[:f.find(" ")]
#    return type


#  def setFolder(self, folder):
#    self.folder = folder
#    self.images = {}


#  def run(self):
#    self.images = {}
#    for node in self.folder:
#      type = self.getImageType(node)
#      if type != None:
#        self.images[node] = type


class ImageView(QWidget, Script):
  def __init__(self):
    Script.__init__(self, "viewerimage")
    self.type = "imageview"
    self.icon = None
    self.vfs = vfs.vfs()
    self.ft = FILETYPE()
    self.reg_viewer = re.compile(".*(JPEG|JPG|jpg|jpeg|GIF|gif|bmp|BMP|png|PNG|pbm|PBM|pgm|PGM|ppm|PPM|xpm|XPM|xbm|XBM).*", re.IGNORECASE)
    self.loadedImage = LoadedImage()
    self.sceneWidth = 0
    #self.sorter = SortImages()


  def start(self, args):
    self.node = args.get_node("file")
    self.curnode = self.node
    #self.parent = self.node.parent
    #self.sorter.setFolder(self.parent)
    #self.sorter.start()
    #self.getImage()


  def createMenuItems(self):
    self.l90button = QRotateButton(-90, ":rotate-left.png")
    self.r90button = QRotateButton(90, ":rotate-right.png")
    self.rotate180button = QRotateButton(180, ":rotate-180.png")
    self.zoomin = QZoomButton(float(1.25), ":zoom-in.png")
    self.zoomout = QZoomButton(float(0.8), ":zoom-out.png")
    self.fitbest = QPushButton("fitbest")
    #self.previous = QPushButton("previous")
    #self.next = QPushButton("next")

    self.connect(self.l90button, SIGNAL("clicked"), self.rotate)
    self.connect(self.r90button, SIGNAL("clicked"), self.rotate)
    self.connect(self.rotate180button, SIGNAL("clicked"), self.rotate)
    self.connect(self.zoomin, SIGNAL("zoomed"), self.zoom)
    self.connect(self.zoomout, SIGNAL("zoomed"), self.zoom)
    self.connect(self.fitbest, SIGNAL("clicked()"), self.fitbestgeom)
    #self.connect(self.previous, SIGNAL("clicked()"), self.setPreviousImage)
    #self.connect(self.next, SIGNAL("clicked()"), self.setNextImage)


  def drawMenu(self):
    self.hbox = QHBoxLayout()
    self.setLayout(self.vbox)
    self.hbox.addWidget(self.l90button)
    self.hbox.addWidget(self.r90button)
    self.hbox.addWidget(self.rotate180button)
    self.hbox.addWidget(self.zoomin)
    self.hbox.addWidget(self.zoomout)
    #self.hbox.addWidget(self.previous)
    #self.hbox.addWidget(self.next)
    self.hbox.addWidget(self.fitbest)
    self.vbox.addLayout(self.hbox)

  
  #def getIdx(self):
  #  idx = 0
  #  res = -1
  #  for node in self.parent.next:
  #    if node.name == self.node.name:
  #      res = idx
  #    idx += 1
  #  return res



  #type: 0 = forward, 1 = backward
  #def getImage(self, type=1):
  #  pass
    #idx = self.parent.next.(self.curnode)
    #print nodes
    #for node in self.parent.next[self.idx:]:
    #  type = getImageType(node)
    #  if type != None:
    #self.setImage()
    

  #def setPreviousImage(self):
  #  if self.idx == 0:
  #    self.idx = len(self.parent.next)
  #    self.node = self.parent.next[self.idx]
  #  else:
  #    self.idx -= 1
  #    self.node = self.parent.next[self.idx]
  #  self.setImage()


  #def setNextImage(self):
  #  pass


  def setImage(self):
    if self.node.attr.size != 0:
      map = self.node.attr.smap
      try:
        #XXX temporary patch for windows magic
        f = self.node.attr.smap["type"]
      except IndexError:
        #XXX temporary patch for windows magic
        self.ft.filetype(node)
        f = self.node.attr.smap["type"]
    res = self.reg_viewer.match(f)
    if res != None:
      type = f[:f.find(" ")]
      self.loadedImage.load(self.node, type)
    else:
      self.loadedImage.notSupported()
      #not supported format
      #self.loadedImage.notSupported()


  def g_display(self):
    QWidget.__init__(self, None)
    self.factor = 1
    self.vbox = QVBoxLayout()
    self.setLayout(self.vbox)
    self.scrollArea = QScrollArea()
    self.scrollArea.setWidget(self.loadedImage)
    self.scrollArea.setAlignment(Qt.AlignCenter)
    self.vbox.addWidget(self.scrollArea)
    self.createMenuItems()
    self.drawMenu()
    self.setImage()


  def zoom(self, zoomer):
    self.factor *= zoomer
    self.loadedImage.resize(zoomer)
    if self.factor > 3.33:
      self.zoomin.setEnabled(False)
    elif self.factor < 0.33:
      self.zoomout.setEnabled(False)
    else:
      self.zoomin.setEnabled(True)
      self.zoomout.setEnabled(True)

  
  def fitbestgeom(self):
    self.factor = 1
    self.loadedImage.adjust(self.sceneWidth)
    self.zoomin.setEnabled(True)
    self.zoomout.setEnabled(True)


  def rotate(self, angle):
    self.loadedImage.rotate(angle)


  def updateWidget(self):
    self.sceneWidth = self.scrollArea.geometry().width()
    self.loadedImage.adjust(self.sceneWidth)


  def resizeEvent(self, e):
    self.sceneWidth = self.scrollArea.geometry().width()
    self.loadedImage.adjust(self.sceneWidth)


class viewerimage(Module):
  def __init__(self):
    Module.__init__(self, "viewerimage", ImageView)
    self.conf.add("file", "node")
    self.conf.add_const("mime-type", "JPEG")
    self.conf.add_const("mime-type", "GIF")
    self.conf.add_const("mime-type", "PNG")
    self.tags = "viewer"
