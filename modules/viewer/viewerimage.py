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

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from api.vfs import *
from api.module.module import *
from api.module.script import *

import sys

import time

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


class ImageView(QWidget, Script):
  def __init__(self):
    Script.__init__(self, "viewerimage")
    self.type = "imageview"
    self.icon = None
  
  def start(self, args):
    self.node = args.get_node("file")
    file = self.node.open()
    self.buff = file.read()
    file.close()


  def createMenuItems(self):
    self.l90button = QRotateButton(-90, ":rotate-left.png")
    self.r90button = QRotateButton(90, ":rotate-right.png")
    self.rotate180button = QRotateButton(180, ":rotate-180.png")
    self.zoomin = QZoomButton(float(1.25), ":zoom-in.png")
    self.zoomout = QZoomButton(float(0.8), ":zoom-out.png")
    #self.fitbest = QPushButton("fitbest")

    self.connect(self.l90button, SIGNAL("clicked"), self.rotate)
    self.connect(self.r90button, SIGNAL("clicked"), self.rotate)
    self.connect(self.rotate180button, SIGNAL("clicked"), self.rotate)
    self.connect(self.zoomin, SIGNAL("zoomed"), self.zoom)
    self.connect(self.zoomout, SIGNAL("zoomed"), self.zoom)
    #self.connect(self.fitbest, SIGNAL("clicked()"), self.fitBest)


  def drawMenu(self):
    self.hbox = QHBoxLayout()

    self.setLayout(self.vbox)
    self.hbox.addWidget(self.l90button)
    self.hbox.addWidget(self.r90button)
    self.hbox.addWidget(self.rotate180button)
    self.hbox.addWidget(self.zoomin)
    self.hbox.addWidget(self.zoomout)
    #self.hbox.addWidget(self.fitbest)
    self.vbox.addLayout(self.hbox)


  def g_display(self):
    QWidget.__init__(self, None)
    self.factor = 1
    self.vbox = QVBoxLayout()
    self.setLayout(self.vbox)
    self.imageLabel = QLabel()
    #self.imageLabel.setBackgroundRole(QPalette.Dark)
    self.imageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
    self.scrollArea = QScrollArea()
    #self.scrollArea.setBackgroundRole(QPalette.Dark)
    self.scrollArea.setWidget(self.imageLabel)
    self.scrollArea.setAlignment(Qt.AlignCenter)
    self.orig_pixmap = QPixmap()
    self.orig_pixmap.loadFromData(self.buff)
    self.matrix = QMatrix()
    self.imageLabel.setPixmap(self.orig_pixmap)
    self.imageLabel.adjustSize()
    #self.fitBest()
    self.vbox.addWidget(self.scrollArea)
    self.createMenuItems()
    self.drawMenu()


  def fitBest(self):
    #self.factor = 1
    pixmap = None

    #self.imageLabel.setMaximumSize(self.width(),  self.height())
    #if self.height() < self.img.height() :
    #  self.img = self.img.scaledToHeight(self.height())
    #if self.width() < self.img.width() :
    #  self.img = self.img.scaledToWidth(self.width())
    #self.imageLabel.setPixmap(self.img)

    if self.scrollArea.height() < self.imageLabel.pixmap().height():
      self.orig_pixmap.scaledToHeigth(self.scrollArea.heigth())
      #fact = (self.imageLabel.pixmap().height() - self.scrollArea.height()) / 100
      #self.stateinfo = str(fact)
      #self.matrix.scale(fact, fact)
      #pixmap = self.orig_pixmap.transformed(self.matrix)

    if self.scrollArea.width() < self.imageLabel.pixmap().width():
      self.orig_pixmap.scaledToWidth(self.scrollArea.width())
      #fact = (self.imageLabel.pixmap().width() - self.scrollArea.width()) / 100
      #self.stateinfo = str(fact)
      #self.matrix.scale(fact, fact)
      #pixmap = self.orig_pixmap.transformed(self.matrix)

    if pixmap != None:
      self.imageLabel.setPixmap(self.orig_pixmap)


  def zoom(self, zoomer):
    self.factor *= zoomer
    self.matrix.scale(zoomer, zoomer)
    pixmap = self.orig_pixmap.transformed(self.matrix)
    self.imageLabel.setPixmap(pixmap)
    self.imageLabel.adjustSize()
    if self.factor > 3.33:
      self.zoomin.setEnabled(False)
    elif self.factor < 0.33:
      self.zoomout.setEnabled(False)
    else:
      self.zoomin.setEnabled(True)
      self.zoomout.setEnabled(True)
    #self.scrollArea.setWidget(self.imageLabel)


  def rotate(self, angle):
    pass
    self.matrix.rotate(angle)
    pixmap = self.orig_pixmap.transformed(self.matrix)
    self.imageLabel.setPixmap(pixmap)
    self.imageLabel.adjustSize()


  def updateWidget(self):
    pass
    #self.imageLabel.setMaximumSize(self.width(),  self.height())
    #if self.height() < self.img.height() :
    #  self.img = self.img.scaledToHeight(self.height())
    #if self.width() < self.img.width() :
    #  self.img = self.img.scaledToWidth(self.width())
    #self.imageLabel.setPixmap(self.img)

  def resizeEvent(self, e):
    pass
    #self.img = QPixmap()
    #self.img.loadFromData("")
    #self.imageLabel.setPixmap(self.img)
    #self.imageLabel.setMaximumSize(self.width(),  self.height())
    #if self.height() < self.img.height() :
    #  self.img = self.img.scaledToHeight(self.height())
    #if self.width() < self.img.width() :
    #  self.img = self.img.scaledToWidth(self.width())
    #self.imageLabel.update()
    #self.imageLabel.setPixmap(self.img)
    

class viewerimage(Module):
  def __init__(self):
    Module.__init__(self, "viewerimage", ImageView)
    self.conf.add("file", "node")
    self.conf.add_const("mime-type", "JPEG")
    self.conf.add_const("mime-type", "GIF")
    self.conf.add_const("mime-type", "PNG")
    self.tags = "viewer"
