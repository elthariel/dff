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
#  Christophe Malinge <cma@digital-forensic.org>
#  Frederic Baguelin <fba@digital-forensic.org>
#

from api.vfs import *
from api.env import *
from api.loader import *
from api.type import *

import os.path, os, sys
import dircache

import utils

from types import *

import re

#predefined arguments types:
#node, path, driver, script

class Completion():
    def __init__(self, raw_input):
        #init framework core dependencies
        self.env = env.env()
        self.loader = loader.loader()
        self.vfs = vfs.vfs()
        self.lmodules = self.loader.modules
	self.console = raw_input 

    def get_completion_scope(self, arg, begidx):
        cur_arg = None
        prev_arg = None
        opt = []

        for a in arg:
            opt.append(a.arg)
            if begidx <= a.end:
                if begidx >= a.start:
                    cur_arg = a.arg
                elif cur_arg == None:
                    cur_arg = ""
            if self.is_cmd_arg(a.arg):
                if cur_arg == None:
                    opt = []
                    opt.append(a.arg)
                else:
                    break
        return opt, cur_arg
        #print "\ncurrent argument:", cur_arg, "of completion scope:", opt


    def complete_node(self):
        #print "complete node"
        rpath = ""
        supplied = ""
        out = {"type": "path",
               "matches": [],
               "length": 1,
               "supplied": "",
               "matched": 0}

        path = self.cur_str
	
        if path == "" or path[0] != "/":
            if self.vfs.getcwd().path == "" and self.vfs.getcwd().name == "":
                rpath = "/"
            else:
                rpath =  self.vfs.getcwd().path + "/" + self.vfs.getcwd().name + "/" 

	if path == "/":
	  path = "//"
        idx = path.rfind("/")
        if idx == -1:
            supplied = path
        else:
            supplied = path[idx+1:]
            rpath += path[:idx]
        try:
	    rpath = rpath.replace("\ ", " ")
            node = self.vfs.getnode(rpath)
        except OSError, e:
            out["matches"].append("")

        supplied = supplied.replace("\ ", " ")
        out["supplied"] = supplied
        if node:
            if node.next.empty():
                if self.cur_str == "/":
                    out["matches"].append("")
                else:
                    out["matches"].append("/")
                out["matched"] += 1
            else:
                list = node.next
                #for i in range(node.next.size()):
                #    print node.next[i].name
            #completion on a path
                if supplied == "":
                    for i in  list:
                        if not i.next.empty():
                            if len(i.name + "/") > out["length"]:
                                out["length"] = len(i.name + "/")
                            out["matches"].append(i.name + "/")
                        else:
                            if len(i.name) > out["length"]:
                                out["length"] = len(i.name)
                            out["matches"].append(i.name)
                        out["matched"] += 1
                else:
                    for i in list:
                        if i.name.startswith(supplied) == True:
                            if not i.next.empty():
                                if len(i.name + "/") > out["length"]:
                                    out["length"] = len(i.name + "/")
                                out["matches"].append(i.name + "/")
                            else:
                                if len(i.name) > out["length"]:
                                    out["length"] = len(i.name)
                                out["matches"].append(i.name)
                            out["matched"] += 1
        return out
        

    def complete_path(self):
        #print "complete path"
        rpath = ""
        supplied = ""
        out = {"type": "path",
               "matches": [],
               "length": 1,
               "supplied": "",
               "matched": 0}
        path = self.cur_str

        if path == "":
            rpath = os.getcwd() + "/"
        else:
            idx = path.rfind("/")
            if idx == -1:
                rpath = os.getcwd() + "/"
                supplied = path

            elif idx == 0:
              supplied = path[idx+1:]  
              rpath = path[:idx+1]

            else:
                supplied = path[idx+1:]
                if path[0] != "/":
                    rpath = os.getcwd() + "/" + path[:idx+1]
                else:
                    rpath = path[:idx+1]

        #directory listing
        rpath = rpath.replace("\ ", " ")
        supplied = supplied.replace("\ ", " ")
        out["supplied"] = supplied
        try:
            a = dircache.listdir(rpath)
        except OSError, e:
            return
        if a:
            #completion on a path
            if supplied == "":
                for it in a:
                    if os.path.isdir(rpath + '/' + it):
                        #it = it.replace(" ", "\ ")
                        if len(it + "/") > out["length"]:
                            out["length"] = len(it + "/")
                        out["matches"].append(it + '/')
                    else:
                        #it = it.replace(" ", "\ ")
                        if len(it) > out["length"]:
                            out["length"] = len(it)
                        out["matches"].append(it)
                    out["matched"] += 1
            else:
                for it in a:
                    if it.startswith(supplied) == True:
                        if os.path.isdir(rpath + '/' + it):
                            #it = it.replace(" ", "\ ")
                            #print it
                            if len(it + "/") > out["length"]:
                                out["length"] = len(it + "/")
                            out["matches"].append(it + '/')
                        else:
                            if len(it) > out["length"]:
                                out["length"] = len(it)
                            #it = it.replace(" ", "\ ")
                            out["matches"].append(it)
                        out["matched"] += 1
        return out


    def value_completion(self):
        out = []

        if self.prev_arg != None and hasattr(self, "complete_" + self.prev_arg.type):
            func = getattr(self, "complete_" + self.prev_arg.type)
            out = func()

        #other type, check if presetted values exist 
        else:
            out = {"type": "predefined",
                   "matches": [],
                   "matched": 0,
                   "length": 1}
            for i in self.cvl:
                to_add = False
                if i.name == self.prev_arg.name:
                    val = ""
                    if i.type == "string":
                        val = i.get_string()
                    elif i.type == "int":
                        val = str(i.get_int())
                    elif i.type == "node" and i.get_node() :
                        val = i.get_node().path + "/" + i.get_node().name
                    if self.cur_str == "":
                        to_add = True
                    elif val.startswith(self.cur_str):
                        to_add = True
                    if to_add:
                        out["matches"].append(val)
                        out["matched"] += 1
                        if len(val) > out["length"]:
                            out["length"] = len(val)
            if out["matched"] == 1:
                out = out["matches"][0]

        return out


    def complete_modules(self):
        out = {"type": "module",
               "matches": {},
               "length": {"tag": 1, "module": 1},
               "matched": 0}
        longest_tag = 1
        longest_module = 1

        for cmd in self.lmodules:
            to_add = False

            if self.cur_str != "":
                if cmd.startswith(self.cur_str):
                    to_add = True
                else:
                    to_add = False
            else:
                to_add = True

            if to_add:
                if longest_module < len(cmd):
                    longest_module = len(cmd)
                mod = self.lmodules[cmd]
                tag = mod.tags
                if longest_tag < len(tag):
                    longest_tag = len(tag)
                if tag not in out["matches"]:
                    out["matches"][tag] = []
                out["matches"][tag].append(cmd)
                out["matched"] += 1

        out["length"]["tag"] = longest_tag
        out["length"]["module"] = longest_module

        if out["matched"] == 1:
            out = [out["matches"][i][0] for i in out["matches"].iterkeys()]

        elif out["matched"] == 0:
            out = ""

        return out
        
    def get_conf(self, cmd):
        conf = None
        if cmd in self.lmodules:
            mod = self.lmodules[cmd]
            conf = mod.conf
        return conf

    def is_cmd_arg(self, arg):
	if arg in self.loader.modules:
          return True
        else:
          return False

    def get_arg(self):
        return None

    def complete_key(self):
        out = {"type": "key", 
               "required": [],
               "optional": [],
               "length": 1,
               "matched": 0}

        arg_with_no_key = utils.get_arg_with_no_key(self.args)
        needs_no_key = utils.needs_no_key(self.cdl)
        for i in range(len(self.cdl)):
            if (self.cdl[i].type == "path" or self.cdl[i].type == "node") and (arg_with_no_key != -1) and (needs_no_key != None):
                pass
            else:
                arg = "--" + self.cdl[i].name
                if arg not in self.args and arg.startswith(self.cur_str):
                    if len(arg) > out["length"]:
                        out["length"] = len(arg)
                    if self.cdl[i].optional:
                        out["optional"].append(arg)
                    else:
                        out["required"].append(arg)
                    out["matched"] += 1

        if out["matched"] == 0:
            out = ""
            
        elif out["matched"] == 1:
            if len(out["required"]) == 0:
                out = out["optional"][0]
            else:
                out = out["required"][0]

        return out


    def complete_empty(self):
        out = None

        if self.prev_str == "--":
            out = ""

        if self.prev_str == "--modules":
            out = self.complete_modules()

        elif self.prev_str.startswith("--"):
            if self.prev_arg == None:
                out = ""
            elif self.prev_arg.type != "bool":
                out = self.value_completion()
            else:
                arg_with_no_key = utils.get_arg_with_no_key(self.args)
                needs_no_key = utils.needs_no_key(self.cdl)
                if arg_with_no_key == -1 and needs_no_key != None:
                    if (needs_no_key.type in ["path", "node"]) or (len(self.cvl) > 0):
                        self.prev_arg = needs_no_key
                        out = self.value_completion()
                    else:
                        out = self.complete_key()
                else:
                    out = self.complete_key()
        else:
            arg_with_no_key = utils.get_arg_with_no_key(self.args)
            needs_no_key = utils.needs_no_key(self.cdl)
            if arg_with_no_key == -1 and needs_no_key != None:
                if (needs_no_key.type in ["path", "node"]) or (len(self.cvl) > 0):
                    self.prev_arg = needs_no_key
                    out = self.value_completion()
                else:
                    out = self.complete_key()
            else:
                out = self.complete_key()

        return out


    def complete_current(self):
        out = None

        if self.prev_str == "--modules":
            out = self.complete_modules()
        elif self.prev_str == "--":
            out = self.complete_key()
        elif self.prev_str.startswith("--"):
            if self.prev_arg == None:
                out = ""
            elif self.prev_arg.type != "bool":
                for i in range(len(self.cdl)):
                    arg = "--" + self.cdl[i].name
                    if arg == self.prev_str:
                        out = self.value_completion()
            else:
                out = self.complete_key()
        else:
            arg_with_no_key = utils.get_arg_with_no_key(self.args)
            needs_no_key = utils.needs_no_key(self.cdl)
            if self.args.index(self.cur_str) == arg_with_no_key:
                self.prev_arg = needs_no_key
                out = self.value_completion()
            else:
                out = self.complete_key()

        return out


    def complete(self, line, begidx):
        self.shell_key = [";", "<", ">", "&", "|", "&", ";"]
        self.cmd_key = ["--modules"]
        self.cmd_key.extend([i for i in self.lmodules])
        self.args, self.bopt = utils.split_line(line)
        self.cur_str = ""
        self.prev_str = ""
        self.prev_arg = None
        self.cdl = None
        self.cvl = None
        matches = []
        start_scope_idx = 0
        end_scope_idx = len(self.args)

        for item in self.bopt:
            if item["arg"][0] in self.shell_key or item["arg"] == "--modules":
                if begidx >= item["end"]:
                    start_scope_idx = self.bopt.index(item) + 1
                    self.prev_str = ""
                    self.cur_str = ""
                else:
                    end_scope_idx = self.bopt.index(item)
            else:
                if begidx >= item["start"] and begidx <= item["end"]:
                    self.cur_str = item["arg"]
                if item["end"] < begidx:
                    self.prev_str = item["arg"]

        self.args = self.args[start_scope_idx:end_scope_idx]

        if self.prev_str == "":
            if len(self.args) == 0:
                matches = self.complete_modules()
            elif len(self.args) == 1 and self.cur_str != "":
                matches = self.complete_modules()
            else:
                matches = ""

        else:
            conf = self.get_conf(self.args[0])
            if conf != None:
                self.cdl = conf.descr_l
                self.cvl = conf.val_l
                #print "prev:", self.prev_str, "cur:", self.cur_str
            
                for i in range(len(self.cdl)):
                    arg = "--" + self.cdl[i].name
                    if arg == self.prev_str:
                        self.prev_arg = self.cdl[i]
                    if self.cur_str == None or self.cur_str == "":
                        matches = self.complete_empty()
                    else:
                        matches = self.complete_current()
            else:
                matches = ""

        if isinstance(matches, list) and len(matches) == 1:
            return matches[0]
        else:
            return matches

    def strdiff(self, str1, str2):
     i = len(str1)
     j = 0
     while j < len(str1) and j < len(str2) and str1[j] == str2[j]:
       j += 1
       i -= 1
     return len(str1) - i


    def find_longest(self, list):
     max = 0
     for str in list:
       if len(str) > max:
         max = len(str)
     return max


    def get_max_col(self, start, max):
     displaywidth = self.console.get_term_size() - start
     col = (displaywidth - (displaywidth / 6)) / max
     return col

    def insert_predefined_comp(self, text, matches):
     max_predef = matches["length"]
     col = self.get_max_col(13, max_predef)
     x = 0

     sys.stdout.write("predefined: ")
     for item in matches["matches"]:
       if x == col:
         sys.stdout.write("\n" + " " * 13)
         x = 0
       predef_arg = item + " " * (max_predef + 2 - len(item))
       x += 1
       sys.stdout.write(predef_arg)


    def insert_module_comp(self, text, matches):     
     max_tag = matches["length"]["tag"]
     max_mod = matches["length"]["module"]
     col = self.get_max_col(max_tag + 4, max_mod)
     max_ident = 0
     prev_mod = ""
     cur_mod = text
     res = ""
     idx = 0

     if matches["matched"] == 1:
       if len(matches["matches"]["required"]) == 1:
         return self.get_str(text, matches["matches"]["required"][0])
       else:
         return self.get_str(text, matches["matches"]["optional"][0])

     for tag in matches["matches"].iterkeys():
       if len(matches["matches"][tag]) > 0:
         tag_arg = tag + " " * (max_tag + 2 - len(tag)) + ": "
         sys.stdout.write(tag_arg)
         x = 0
         #sys.stdout.write(str(len(matches["modules"][tag])))
         for item in matches["matches"][tag]:
           if cur_mod != "":
             if prev_mod != "":
               _len = self.strdiff(prev_mod, item)
               if max_ident > _len:
                 max_ident = _len
             else:
               max_ident = len(item)
             prev_mod = item[:max_ident]
           if x == col:
             sys.stdout.write("\n" + " " * (max_tag + 4))
             x = 0
           mod_arg = item + " " * (max_mod + 2 - len(item))
           x += 1
           sys.stdout.write(mod_arg)
         idx += 1
         if idx < len(matches["matches"]):
           sys.stdout.write("\n")

     if max_ident > 0:
       return prev_mod[len(text):max_ident]

    def insert_path_comp(self, text, matches):
     max_path = matches["length"]
     cur_path = matches["supplied"].replace("\ ", " ")
     print cur_path
     col = self.get_max_col(0, max_path)
     idx = 0
     filled = 0
     prev_path = ""
     max_ident = 0

     if matches["matched"] == 1:
       res = self.strdiff(cur_path, matches["matches"][0])
       comp = matches["matches"][0][res:]
       i = 0
       while i != len(comp):
         if comp[i] == " " and comp[i - 1] != "\\":
           comp = comp[:i] + "\\" + comp[i:] 
         i += 1
       return comp

     else:
       x = 0
       for path in matches["matches"]:
         if cur_path != "":
           if prev_path != "":
             res = self.strdiff(prev_path, path)
             if max_ident > res:
               max_ident = res
           else:
             max_ident = len(path)
           prev_path = path[:max_ident]
         if x == col:
           sys.stdout.write("\n")
           x = 0
         path_arg = path + " " * (max_path + 2 - len(path))
         sys.stdout.write(path_arg)
         x += 1
     if cur_path != "":
       comp = prev_path[len(cur_path):max_ident]
       i = 0
       while i != len(comp):
         if comp[i] == " " and comp[i - 1] != "\\":
           comp = comp[:i] + "\\" + comp[i:] 
         i += 1
       return comp
       #return prev_path[len(cur_path):max_ident]
     #  return self.get_str(cur_path, prev_path[:same])

    def get_str(self, text, matches):
     start = len(text)
     if start > 0:
       return matches[start:]
     else:
       return matches


    def insert_key_comp(self, text, matches):
     max_key = matches["length"]
     col = self.get_max_col(10, max_key)
     idx = 0
     filled = 0

     for type in ["required", "optional"]:
       if len(matches[type]) > 0:
         filled += 1
     
     prev_key = text
     same = 0
     for type in ["required", "optional"]:
       if len(matches[type]) > 0:
         sys.stdout.write(type + ": ")
         x = 0
         for key in matches[type]:
           same = self.strdiff(prev_key, key)
           prev_key = key
           if x == col:
             sys.stdout.write("\n" + " " * (10))
             x = 0
           key_arg = key + " " * (max_key + 2 - len(key))
           sys.stdout.write(key_arg)
           x += 1
         idx += 1
         if idx < filled:
           sys.stdout.write("\n")
     return self.get_str(text, prev_key[:same])

