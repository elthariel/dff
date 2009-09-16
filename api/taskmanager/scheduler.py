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
#  Solal J. <sja@digital-forensic.org>
#

import threading 
import sys
import traceback

from Queue import *
from types import *
from api.loader import *
from api.exceptions.libexceptions import *
from api.env import *


event_type = ["refresh_tree", "add_str", "add_qwidget"]

class WorkQueue():
	class __WorkQueue():
		def launch(self):
			while True:
				work = self.waitQueue.get()
				self.workerQueue.put(work)
		def enqueue(self, proc):
			self.waitQueue.put(proc)

		def set_callback(self, type, func):
			if type in self.event_func:
				self.event_func[type].append(func)
	
		def worker(self):
			while True:
			  	proc  = self.workerQueue.get()
				proc.launch()
				self.workerQueue.task_done()

		def __init__(self, max = 5):
			self.waitQueue = Queue()
			self.workerQueue = Queue(max)
			self.max = max
			self.env = env.env()
			self.event_func = {}
			for type in event_type:
				self.event_func[type] = []
			for i in range(max):
				thread = threading.Thread(target = self.worker)
				thread.setDaemon(True)
				thread.start()

	__instance = None
	
	def __init__(self):
		if WorkQueue.__instance is None:
			WorkQueue.__instance = WorkQueue.__WorkQueue()
	
	def __setattr__(self, attr, value):
		setattr(self.__instance, attr, value)

	def __getattr__(self, attr):
		return getattr(self.__instance, attr)

sched = WorkQueue()

def voidcall(node):
	pass

sched.set_callback("refresh_tree", voidcall)
sched.set_callback("add_widget", voidcall)
sched.set_callback("add_str", voidcall)

thread = threading.Thread(target = sched.launch)
thread.setDaemon(True)
thread.start()
