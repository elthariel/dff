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
#  Christophe Malinge <cma@digital-forensic.org>
#  Frederic Baguelin <fba@digital-forensic.org>
#

import sys,string, os, traceback, types, completion, signal
import  line_to_arguments
from cmd import *
#from api.vfs import *
#from api.taskmanager.taskmanager import TaskManager 
from api.manager.manager import ApiManager

from ui.console.complete_raw_input import complete_raw_input
from ui.history import history

PROMPT = "dff / > "
INTRO = "\nWelcome to the Digital Forensic Framework\n"
IDENTCHARS = string.ascii_letters + string.digits + '\ _='

class console(Cmd):
    def __init__(self, completekey='tab', stdin=None, stdout=None):
        Cmd.__init__(self, completekey, stdin, stdout)
        self.history = history()
        self.api = ApiManager()
        self.vfs = self.api.vfs()
        self.taskmanager = self.api.TaskManager()
	self.line_to_arguments = line_to_arguments.Line_to_arguments()
        self.old_completer = ""
        self.prompt = "dff / > "
        self.intro = "\n##########################################\n\
# Welcome on Digital Forensics Framework #\n\
##########################################\n"
	self.stdin = self
	self.completekey = '\t'
	self.comp_raw = complete_raw_input(self)
        self.completion = completion.Completion(self.comp_raw)
	if os.name == 'posix':
  	  signal.signal(signal.SIGTSTP, self.bg)

    def bg(self, signum, trace):
	if self.taskmanager.current_proc:
	   proc = self.taskmanager.current_proc	
  	   proc.exec_flags += ["thread"]
	   print "\n\n[" + str(proc.pid) + "]" + " background " + proc.name
	   self.taskmanager.current_proc = None 
        self.cmdloop()                      	

    def precmd(self, line):
        return line

    def postcmd(self, stop, line):
        self.prompt = "dff " + self.vfs.getcwd().path + "/" + self.vfs.getcwd().name + " > "
        return stop

    def preloop(self):
	return 
 
    def postloop(self):
        print "Exiting..."

    def onecmd(self, line):
        try:
	    if line == 'exit' or line == 'quit':
	      return 'stop'
            exc_list = self.line_to_arguments.generate(line)
            if exc_list != None and len(exc_list) > 0:
                for exc in exc_list:
		    exec_type = ["console"]
                    if line[-1:] == "&":
		      exec_type += ["thread"]
                    for cmd, args in exc.iteritems():
                       if cmd != None:
		          self.history.add(line.strip())
    		          self.taskmanager.add(cmd, args,exec_type)
            else:
                return self.emptyline()
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback, None, sys.stdout)

    def emptyline(self):
        pass

    def default(self, line):
        try:
            exec(line) in self._locals, self._globals
        except Exception, e:
            print e.__class__, ":", e

    def cmdloop(self, intro=None):
        self.preloop()
        if self.intro:
          print self.intro
	  self.intro = None
	else:
	  print ''
        stop = None
        while not stop:
           if self.cmdqueue:
               line = self.cmdqueue.pop(0)
           else:
	       line = self.comp_raw.raw_input()
           line = self.precmd(line)
           stop = self.onecmd(line)
           stop = self.postcmd(stop, line)
        self.postloop()

    def complete(self, line, begidx):
	line = str(line).strip('\n')
        self.completion_matches = self.completion.complete(line, begidx)
        try:
            return self.completion_matches
        except IndexError:
            return None

