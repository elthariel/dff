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
#  Frederic Baguelin <fba@digital-forensic.org>


#!/usr/bin/python

from string import ascii_letters, printable
import sys

def hexlify(buff):
    for c in buff:
        hc = hex(ord(c))[2:]
        if len(hc) == 1:
            hc = "0" + hc
        sys.stdout.write(hc)
        sys.stdout.write(" ")
    if len(buff) < 16:
        pad = 3 * (16 - len(buff))
        sys.stdout.write(" " * pad)
    sys.stdout.write(" ")


def asciilify(buff):
    for c in buff:
        if c not in printable:
            sys.stdout.write(".")
        else:
            sys.stdout.write(c)


def is_ok(c):
    if c == "\n" or c == "Y" or c == "y":
        return True
    else:
        return False


def show_generated():
    file = open("dumb_fs.bin", "rb")
    buff = file.read(16)
    stop = False
    while len(buff) and stop != True:
        off = hex(file.tell() - 16)[2:-1]
        off = "0" * (4 - len(off)) + off + "  "
        sys.stdout.write(off)
        hexlify(buff)
        sys.stdout.write("|")
        asciilify(buff)
        sys.stdout.write("|\n")
        buff = file.read(16)
        if file.tell() % 512 == 0:
            sys.stdout.write("\ndo you want to see the following block of 512 bytes ? [Y/n]")
            c = sys.stdin.read(1)
            sys.stdout.write("\n")
            if not is_ok(c):
                stop == True


def generate():
    file = open("dumb_fs.bin", "wb")
    for i in ascii_letters:
        name = i + ".txt"
        name = name + " " * (8 - len(name)) + "\xDE\xAD\xBE\xEF" * 2
        data = i * 64
        try:
            sys.stdout.write(".")
            file.write(name)
            file.write(data)
        except:
            print sys.stdout.write(" [!!]\n")
            return False
    file.write(":)" * 41)
    sys.stdout.write(" [OK]\n")
    file.close()
    return True

if __name__ == "__main__":
    print "I am going to generate a dumb file system named dumb_fs.bin"
    if generate():
        print "file dumb_fs.bin generated"
    else:
        print "there was an error during the creation of the file"
        sys.exit(-1)
    print "Do you want to see the resulting file as hexdump ? [Y/n]"
    if is_ok(sys.stdin.read(1)) == True:
        show_generated()
    print "\nNow you can play with this dumb file system, press any key to exit"
    sys.stdin.read(1)
