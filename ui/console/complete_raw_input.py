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

import sys,os, string, struct

if os.name == "posix":
  import tty, termios, fcntl
elif os.name == "nt":
  import msvcrt
  from ctypes import windll, create_string_buffer

from ui.history import history

class complete_raw_input():
   class __posix():
     eol = "\n"
     MOVE_LEFT = '\x1b\x5b\x44'
     MOVE_RIGHT = '\x1b\x5b\x43'
     MOVE_UP = '\x1b\x5b\x41'
     MOVE_DOWN = '\x1b\x5b\x42'

     def __init__(self, parent, console):
       self.console = console	
       self.completekey = self.console.completekey
       self.complete_func = self.console.complete
       self.line = ""
       self.history = history()
       self.parent = parent

     def get_term_size(self):
       width = 80
       s = struct.pack('HHHH', 0, 0, 0, 0)
       s = fcntl.ioctl(1, termios.TIOCGWINSZ, s)
       twidth = struct.unpack('HHHH', s)[1]
       if twidth > 0:
         width = twidth
       return width

     def get_char(self):
       fd = sys.stdin.fileno()
       if os.isatty(fd):
         oldterm = termios.tcgetattr(fd)
         term = termios.tcgetattr(fd)
         term[3] = term[3] & ~termios.ICANON & ~termios.ECHO
         term[6] [termios.VMIN] = 1
         term[6] [termios.VTIME] = 0
         try :
           termios.tcsetattr(fd, termios.TCSANOW, term)
           termios.tcsendbreak(fd, 0)
	   ch = os.read(fd, 7) 
         finally :	
	   termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
       else: 	
           ch = os.read(fd, 7)
       if len(ch) == 1:
         if ch in string.printable:
           return ch
         elif ch == '\b' or ch == '\x7f':
           self.delchar()
       elif ch == self.MOVE_LEFT: #left arrow
         if self.cursor > 0:	
	   self.print_text(ch)
	   self.cursor -= 1	
       elif ch == self.MOVE_RIGHT:
         if self.cursor < len(self.line):
	   self.print_text(ch)
	   self.cursor += 1
       elif ch == self.MOVE_UP:
	   self.clear_line()
	   cmd = self.history.getnext()
	   if cmd:
             self.insert_text(cmd)	
       elif ch == self.MOVE_DOWN:
	   self.clear_line()
           cmd = self.history.getprev()
	   if cmd:
	    self.insert_text(cmd)
       return None	

     def __getattr__(self, attr):
	return getattr(self.parent, attr)

   class __nt():
     eol = "\r"
     CODE_LEFT = '\x4b'
     MOVE_LEFT = '\x08'
     MOVE_RIGHT = '\x4d'
     MOVE_UP = '\x48'
     MOVE_DOWN = '\x50'
      
     def __init__(self, parent, console):
       self.console = console
       self.completekey = self.console.completekey
       self.complete_func = self.console.complete
       self.line = ""
       self.history = history()
       self.parent = parent

     def get_term_size(self):
       h = windll.kernel32.GetStdHandle(-12)
       csbi = create_string_buffer(22)
       res = windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)
       if res:
         (bufx, bufy, curx, cury, wattr, left, top, right, bottom, maxx, maxy) = struct.unpack("hhhhHhhhhhh", csbi.raw)
         sizex = right - left + 1
       else:
         sizex = 80
       return sizex    	

     def get_char(self):
       ch = msvcrt.getch()      
       if len(ch) == 1:
         if ch in string.printable:
           return ch
         elif ch == '\x08':
           self.delchar() 		 
   	 elif ch == '\xe0':
          ch = msvcrt.getch()
          if ch == self.CODE_LEFT: 
            if self.cursor > 0:
	      self.print_text(self.MOVE_LEFT)	
	      self.cursor -= 1	
          elif ch == self.MOVE_RIGHT:
            if self.cursor < len(self.line):
	      pad = len(self.line) - self.cursor
	      self.print_text(self.line[self.cursor:] + (pad - 1) * self.MOVE_LEFT)
	      self.cursor += 1
          elif ch == self.MOVE_UP:
	      self.clear_line()
	      cmd = self.history.getnext()
	      if cmd:
                self.insert_text(cmd)	
          elif ch == self.MOVE_DOWN:
	      self.clear_line()
              cmd = self.history.getprev()
	      if cmd:
	        self.insert_text(cmd)
          return None

     def __getattr__(self, attr):
	return getattr(self.parent, attr)

   def __init__(self, console):
	if os.name == "posix":
	  complete_raw_input.__instance = complete_raw_input.__posix(self, console)
  	elif os.name == "nt":
	  complete_raw_input.__instance = complete_raw_input.__nt(self, console)
 
   def __setattr__(self, attr, value):
	setattr(self.__instance, attr, value)
  
   def __getattr__(self, attr):
	return getattr(self.__instance, attr)

   def raw_input(self):
    c = None 
    self.line = ""
    self.cursor = 0
    sys.__stdout__.write(self.console.prompt)
    sys.__stdout__.flush()
    while c != self.eol:
       if c:
         if c == self.completekey:
	   lstrip = self.line[:self.cursor]
           text = lstrip.split(' ')[-1]
           matches = self.complete_func(self.line, self.cursor)
           self.insert_comp(text, matches)
         else:
	   self.insert_text(c)
       c = self.get_char()			   
    self.print_text('\n')
    return self.line

   def insert_text(self, text):
       lsplit = self.line[:self.cursor]
       rsplit = self.line[self.cursor:]	
       self.line = lsplit + text + rsplit 
       self.cursor += len(text) 
       sys.__stdout__.write(text + rsplit)	
       sys.__stdout__.write(len(rsplit) * self.MOVE_LEFT)
       sys.__stdout__.flush()	

   def print_text(self, text): 
       sys.__stdout__.write(text)
       sys.__stdout__.flush()	


   def clear_line(self):
      self.print_text(self.cursor * self.MOVE_LEFT + len(self.line) * ' '  + len(self.line) * self.MOVE_LEFT)
      self.line = ''
      self.cursor = 0		

   def delchar(self):
       if self.cursor > 0:
         lsplit = self.line[:self.cursor - 1]
         rsplit = self.line[self.cursor:]	
         self.line = lsplit + rsplit
         self.cursor -= 1
      	 self.print_text(self.MOVE_LEFT + rsplit + ' '  + (len(rsplit) + 1)*self.MOVE_LEFT)


   def insert_comp(self, text, matches):
     #results of completion with lots of information
     res = ""
     if isinstance(matches, dict) and matches["matched"] != 0:
       if matches["matched"] > 1:
         sys.stdout.write("\n")
       if "type" in matches:
         if hasattr(self.console.completion, "insert_" + matches["type"] + "_comp"):
           func = getattr(self.console.completion, "insert_" + matches["type"] + "_comp")
           res = func(text, matches)
         else:
           pass
       else:
         pass

     if isinstance(matches, str):
       start = len(text)
       if start > 0:
          ins = matches[start:]
       else:
         ins = matches
       self.line = self.line[:self.cursor] + ins + self.line[self.cursor:]
       self.cursor += len(ins)

     if res != "" and res != None:
       self.line = self.line[:self.cursor] + res + self.line[self.cursor:]
       self.cursor += len(res)

     n = len(self.line) - self.cursor
     sys.stdout.write("\n" + self.console.prompt)
     self.print_text(self.line + n * self.MOVE_LEFT)
