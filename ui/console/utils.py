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
#  Frederic Baguelin <fba@digital-forensic.org>
#

import re
import os


def get_arg_with_no_key(args):
    found = False
    res = -1

    for arg in args:
        if not arg.startswith("--") and not arg.startswith("-"):
            idx = args.index(arg)
            if found == False and idx != 0:
                res = idx
                found = True
    return res


def needs_no_key(cdl):
    res = None
    
    for i in range(len(cdl)):
        if cdl[i].type == "node" or cdl[i].type == "path":
            if res == None:
                res = cdl[i]
            else:
                return None
        elif cdl[i].optional == False:
            if res != None:
                return None
            else:
                res = cdl[i]
    return res


def split_line(line):
    startidx = 0
    arg = ""
    opt = []
    i = 0
    
    bopt = []

    shell_key = [";", "<", ">", "&", "|", "&", ";"]

    while i < len(line):
        if line[i] == " " and (line[i-1] != "\\") and (len(arg.split()) != 0):
            opt.append(arg)
            bopt.append({"start": startidx, "end": i, "arg": arg})
            arg = ""
            startidx = i
        elif line[i] in shell_key and (line[i-1] != "\\"):
            if len(arg.split()) != 0:
                opt.append(arg)
                bopt.append({"start": startidx, "end": i, "arg": arg})
            arg = ""
            startidx = i
            while i < len(line) and line[i] in shell_key:
                arg += line[i]
                i += 1
            opt.append(arg)
            bopt.append({"start": startidx, "end": i, "arg": arg})
            if i < len(line):
                arg = line[i]
            else:
                arg = ""
            startidx = i
        elif len(arg.split()) == 0:
            startidx = i
            arg = line[i]
        else:
            arg = arg + line[i]
        i += 1

    if len(arg.split()) != 0:
        bopt.append({"start": startidx, "end": i, "arg": arg})
        opt.append(arg)

    return opt, bopt


def get_absolute_path(value):
    if value.startswith("/"):
        return value
    else:
        return os.getcwd() + "/" + value


def get_absolute_node(value):
    #XXX check '..' in string and not only at the begining
    if value.startswith("/"):
        return value
    elif value.startswith(".."):
        pass
    elif value.startswith("."):
        pass
    else:
        pass


def is_hex(val):
    val = val.lower()
    str = val
    if val.startswith("0x"):
        str = val[2:]
    if len(str) == len(val):
        return False
    try:
        res = int(val, 16)
        if res < 2147483647:
            return True
        else:
            return False
    except ValueError, TypeError:
        return False

def is_int(val):
    if val.isdigit():
        try:
            res = int(val)
            if res < 2147483647:
                return True
            else:
                return False
        except ValueError, TypeError:
            return False
    else:
        return False
