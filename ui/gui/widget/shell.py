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
 
import os, sys, inspect, threading
import signal; signal.signal(signal.SIGINT, signal.SIG_DFL)
from PyQt4.QtGui import QAction, QApplication, QTextEdit, QTextCursor , QPalette, QColor, QBrush, QHBoxLayout, QIcon, QDockWidget, QFont, QFontMetrics
from PyQt4.QtCore import Qt, QString, QThread, QSemaphore, SIGNAL, QObject
from ui.console.console import *
from ui.redirect import RedirectIO
from api.vfs import *
from api.taskmanager.taskmanager import *

class ShellView(QTextEdit, console):
    def __init__(self, parent=None, log=''):
        QTextEdit.__init__(self, parent)
        console.__init__(self)
	self.completion = completion.Completion(self)
	taskmanager = TaskManager()
        self.vfs = vfs.vfs()
        self.log = log or ''
        if parent is None:
            self.eofKey = Qt.Key_D
        else:
            self.eofKey = None
        self.line    = QString()
        self.lines   = []
        self.point   = 0
        self.more    = 0
        self.reading = 0
        self.pointer = 0
        self.cursor_pos   = 0
	font = QFont("Courier")
	font.setFixedPitch(1)
	fm = QFontMetrics(font)	
       	self.fontwidth = fm.averageCharWidth()
	self.setFont(font)
        self.bgcolor = QColor("black")
        self.fgcolor = QColor("white")
        self.selcolor = QColor("green")
        pal = QPalette()
        pal.setColor(pal.Base, self.bgcolor)
        pal.setColor(pal.Text, self.fgcolor)
        self.setPalette(pal)
        self.preloop()
        self.cwd = self.vfs.getcwd()
        self.ps1 = self.cwd.path + "/" + self.cwd.name + " > "
	self.redirect = RedirectIO()
	self.sig = "Sputtext"
	self.connect(self, SIGNAL(self.sig), self.puttext)
	self.redirect.addparent(self, ["ui.gui.widget.shell", "ui.console.console", "ui.console.completion", "ui.console.line_to_arguments", "api.taskmanager.taskmanager", "api.taskmanager.scheduler", "api.taskmanager.processus"], True)
        self.write('Welcome to dff shell\n')
        self.write(self.ps1)

    def write(self, str):
	self.redirect.write(str)
	#self.redirect.write(str, inspect.currentframe().f_back.f_globals['__name__'])
#	self.redirect.write(str,  [sys._getframe(0).f_globals['__name__'], sys._getframe(1).f_globals['__name__'], sys._getframe(2).f_globals['__name__'] ])

    def puttext(self, text):
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.End)
        pos1 = cursor.position()
        cursor.insertText(text)
        self.cursor_pos = cursor.position()
        self.setTextCursor(cursor)
        self.ensureCursorVisible()
        cursor.setPosition(pos1, QTextCursor.KeepAnchor)
        format = cursor.charFormat()
        format.setForeground(QBrush(self.fgcolor))
        cursor.setCharFormat(format)


    def get_interpreter(self):
        return self.interpreter

    def moveCursor(self, operation, mode=QTextCursor.MoveAnchor):
        cursor = self.textCursor()
        cursor.movePosition(operation, mode)
        self.setTextCursor(cursor)

    def flush(self):
        pass

    def isatty(self):
        return 1

    def clear(self):
	pass

    def readline(self):
        self.reading = 1
        self.__clearLine()
        self.moveCursor(QTextCursor.End)
        while self.reading:
            QtGui.qApp.processEvents()
        if self.line.length() == 0:
            return '\n'
        else:
            return str(self.line) 
    
    def writelines(self, text):
        map(self.write, text)

    def fakeUser(self, lines):
        for line in lines:
            self.line = QString(line.rstrip())
            self.write(self.line)
            self.write('\n')
            self.run()

    def run(self):
        self.pointer = 0
        try:
            self.lines.append(str(self.line))
        except Exception,e:
            print e
        line = '\n'.join(self.lines)
	line = self.precmd(line)
	stop = self.onecmd(line)
        stop = self.postcmd(stop, line)
	self.cwd = self.vfs.getcwd()
	self.ps1 = self.cwd.path + "/" + self.cwd.name + " > "
        if self.more:
            self.write(self.ps2)
        else:
            self.write(self.ps1)
            self.lines = []
        self.__clearLine()
        
    def __clearLine(self):
        """
        Clear input line buffer
        """
        self.line.truncate(0)
        self.point = 0
        
    def __insertText(self, text):
        """
        Insert text at the current cursor position.
        """
        self.line.insert(self.point, text)
        self.point += text.length()
        cursor = self.textCursor()
        cursor.insertText(text)
        self.color_line()

    def get_term_size(self):
	 n =  int(self.document().textWidth()/ 7.4)
#	 n =  int(self.document().textWidth()/self.fontwidth)
#	 self.write(str(self.document().textWidth()) + "\n")
	 #self.write(str(n) + "\n")
	 return n 

    def insert_comp(self, text, matches):
      res = ""
      if isinstance(matches, dict) and matches["matched"] != 0:
        if matches["matched"] > 1:
          self.write("\n")
        if "type" in matches:
          if hasattr(self.completion, "insert_" + matches["type"] + "_comp"):
            func = getattr(self.completion, "insert_" + matches["type"] + "_comp")
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
	ins = QString(ins)  
        self.line.insert(self.point, ins)
        self.point += ins.length()

      if res != "" and res != None:
	res = QString(res)  
        self.line.insert(self.point, res)
        self.point += res.length()

      self.cwd = self.vfs.getcwd()
      self.ps1 = "\n" + self.cwd.path + "/" + self.cwd.name + " > "
      self.write(self.ps1)
      self.write(QString(self.line))

      n = len(self.line) - self.point
      for i in range(0, n):
        self.moveCursor(QTextCursor.Left)

    def keyPressEvent(self, e):
        text  = e.text()
        key   = e.key()

	try:	
	  if self.taskmanager.current_proc:
	    if key == Qt.Key_Z and ord(str(text[0])) == 26:
	   	proc = self.taskmanager.current_proc	
  	   	proc.exec_flags += ["thread"]
	   	self.write("\n[" + str(proc.pid) + "]" + " background " + proc.name + "\n")
	   	self.taskmanager.current_proc = None 
		e.ignore()
		self.lines = []
        	self.__clearLine()
		return
	    else:	
	      e.ignore()
	      return 	 
	except AttributeError:
	    pass

        if key == Qt.Key_Backspace:
            if self.point:
                cursor = self.textCursor()
                cursor.movePosition(QTextCursor.PreviousCharacter, QTextCursor.KeepAnchor)
                cursor.removeSelectedText()
                self.color_line()
                self.point -= 1 
                self.line.remove(self.point, 1)

        elif key == Qt.Key_Delete:
            cursor = self.textCursor()
            cursor.movePosition(QTextCursor.NextCharacter, QTextCursor.KeepAnchor)
            cursor.removeSelectedText()
            self.color_line()
            self.line.remove(self.point, 1)
            
        elif key == Qt.Key_Return or key == Qt.Key_Enter:
            self.write('\n')
            if self.reading:
                self.reading = 0
            else:
	        self.lthread = threading.Thread(target = self.run)
		self.lthread.start()
                
        elif key == Qt.Key_Tab:
	    pline = str(self.line)
	    lstrip =  pline[:self.point]
            text = lstrip.split(' ')[-1]
	    matches = self.complete(pline, self.point)
	    self.insert_comp(text, matches)

        elif key == Qt.Key_Left:
            if self.point : 
                self.moveCursor(QTextCursor.Left)
                self.point -= 1 
        elif key == Qt.Key_Right:
            if self.point < self.line.length():
                self.moveCursor(QTextCursor.Right)
                self.point += 1 

        elif key == Qt.Key_Home:
            cursor = self.textCursor ()
            cursor.setPosition(self.cursor_pos)
            self.setTextCursor (cursor)
            self.point = 0 

        elif key == Qt.Key_End:
            self.moveCursor(QTextCursor.EndOfLine)
            self.point = self.line.length() 

        elif key == Qt.Key_Up:
	  cmd = self.history.getnext()
 	  self.histclear()         
	  if cmd:
            self.__insertText(QString(cmd))

        elif key == Qt.Key_Down:
	 cmd = self.history.getprev()
	 self.histclear()
	 if cmd:
           self.__insertText(QString(cmd))
                
        elif text.length():
            self.__insertText(text)
            return

        else:
            e.ignore()
	    return 	
	e.accept()

    def histclear(self):
        cursor = self.textCursor ()
        cursor.select(QTextCursor.LineUnderCursor)
        cursor.removeSelectedText()
        if self.more:
            self.write(self.ps2)
        else:
            self.write(self.ps1)
        self.__clearLine()

    def mousePressEvent(self, e):
        """
        Keep the cursor after the last prompt.
        """
        if e.button() == Qt.LeftButton:
            self.moveCursor(QTextCursor.End)
            

    def contentsContextMenuEvent(self,ev):
        """
        Suppress the right button context menu.
        """
        pass
    
    def dragEnterEvent(self, event):
        event.setAccepted(event.mimeData().hasFormat("text/plain"))

    def dragMoveEvent(self, event):
        if (event.mimeData().hasFormat("text/plain")):
            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()
        else:
            event.ignore()
            
    def dropEvent(self, event):
        if(event.mimeData().hasFormat("text/plain")):
            line = event.mimeData().text()
            self.__insertTextAtEnd(line)
            self.setFocus()
            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()
        else:
            event.ignore()

    def color_line(self):
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.StartOfLine)
        newpos = cursor.position()
        pos = -1
        while(newpos != pos):
            cursor.movePosition(QTextCursor.NextWord)
            pos = newpos
            newpos = cursor.position()
            cursor.select(QTextCursor.WordUnderCursor)
            word = str(cursor.selectedText ().toAscii())
            if(not word) : continue
            color= self.get_color(word)
            format = cursor.charFormat()
            format.setForeground(QBrush(color))
            cursor.setCharFormat(format)

    def get_color(self, word):
        stripped = word.strip()
        if(stripped in self.completenames("")):
            return (self.selcolor) 
        else:
            return (self.fgcolor)

class Shell(QDockWidget):
    def __init__(self, mainWindow):
        QDockWidget.__init__(self)
        self.__mainWindow = mainWindow
        self.icon = QIcon(":shell.png")
        self.addAction(mainWindow)
        self.g_display()
        
    def g_display(self):
        self.setWidget(ShellView(self))
        self.setWindowTitle(QApplication.translate("Shell", "Shell", None, QApplication.UnicodeUTF8))

    def addAction(self, mainWindow):
        self.__action = QAction(self)
        self.__action.setCheckable(True)
        self.__action.setChecked(True)
        self.__action.setObjectName("actionCoreInformations")
        self.__action.setText(QApplication.translate("MainWindow", "Shell", None, QApplication.UnicodeUTF8))
        mainWindow.menuWindow.addAction(self.__action)
        self.connect(self.__action,  SIGNAL("triggered()"),  self.changeVisibleInformations)
    
    def changeVisibleInformations(self):
        if not self.isVisible() :
            self.setVisible(True)
            self.__action.setChecked(True)
        else :
            self.setVisible(False)
            self.__action.setChecked(False)
