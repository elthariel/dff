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
#  Jeremy Mounier <jmo@digital-forensic.org>
# 

import hashlib 
from api.vfs import *
from api.module.script import *
from api.module.module import *

class HASH(Script):
    """@brief Hash class using Python hashlib.

    This class provide computation of six hash algorithm, result of this
    computation will be stored internally in Node (node.attr.smap) and
    will be appended to the result queue for direct printing in DFF.
    """
    def __init__(self):
        Script.__init__(self, "hash")
        self.vfs = vfs.vfs()
        ##@var vfs
        # Framework object.

    def getHash(self, algorithm):
        """ Obtain a ready for computation hash object.

        @param algorithm Wished algorithm.
        @return An hashlib Python object ready for computation, -1 if hashlib
        doesn't support supplied algorithm.
        """
        if algorithm == "md5":
            return hashlib.md5()
        elif algorithm == "sha1":
            return hashlib.sha1()
        elif algorithm == "sha224":
            return hashlib.sha224()
        elif algorithm == "sha256":
            return hashlib.sha256()
        elif algorithm == "sha384":
            return hashlib.sha384()
        elif algorithm == "sha512":
            return hashlib.sha512()
        else:
            return -1
     
    def start(self, args):
        """ This is the entry point of the Hash script.

        @param args holds \e Node file object and optionnal \e algorithm.
        @return Result object with selected algorithm computed as string, or
        md5 if algorithm not set.
        """
        
        node = args.get_node("file")
	try :
          algorithm = args.get_string("algorithm")
	except envError:
          # No algorithm provided by user, using md5
	  algorithm = "md5" 
        f = node.open()
        map = node.attr.smap 
        try:
            algmap = "hash-" + algorithm
            # Search if hash already computed
            map[algmap]
        except:
            # Hash not in node attributes map, compute it

            # Obtain hashing object
            h = self.getHash(algorithm)
            # Read data in file
            buff = f.read(8192)
            while len(buff) > 0:
                # Continuously update hash object
                h.update(buff)
                try :  
                    buff = f.read(8192)
                except vfsError:
                    pass
            algmap = "hash-" + algorithm
            # Set algorithm in node
            map[algmap] = h.hexdigest()
            f.close()
            res = map[algmap] + "  " + node.path + "/" + node.name
            # Add result to result object
            self.res.add_const("result", res)
    
class hash(Module):
  """@brief Base class to connect Hash script to DFF.

  Hash a file and add the results in the file attribute.
  @param file Node object to hash.
  @param algorithm Hash algorithm to use, default: md5.
  """
  def __init__(self):
    """Hash a file and add the results in the file attribute
ex: hash /myfile"""
    Module.__init__(self, "hash", HASH)
    self.conf.add("file", "node")
    self.conf.add("algorithm", "string", True)
    self.conf.add_const("algorithm",  "md5")
    self.conf.add_const("algorithm",  "sha1")
    self.conf.add_const("algorithm",  "sha224")
    self.conf.add_const("algorithm",  "sha256")
    self.conf.add_const("algorithm",  "sha384")
    self.conf.add_const("algorithm",  "sha512")
    self.tags = "parser"

    ##@var tags
    # This variable set this script as a DFF parser
