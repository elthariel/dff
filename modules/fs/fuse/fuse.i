/*
 * DFF -- An Open Source Digital Forensics Framework
 * Copyright (C) 2009-2010 ArxSys
 * This program is free software, distributed under the terms of
 * the GNU General Public License Version 2. See the LICENSE file
 * at the top of the source tree.
 *  
 * See http: *www.digital-forensic.org for more information about this
 * project. Please do not directly contact any of the maintainers of
 * DFF for assistance; the project provides a web site, mailing lists
 * and IRC channels for your use.
 * 
 * Author(s):
 *  Solal J. <sja@digital-forensic.org>
 */

%module  FUSE 
%include "std_string.i"
%include "std_list.i"
%include "std_set.i"
%include "std_map.i"
%include "windows.i"
%import "../../../api/vfs/libvfs.i"
%{
#include "../include/export.hpp"
#include "fuse.hpp"
%}

%include "../include/export.hpp"
%include "fuse.hpp"


namespace std
{
  %template(ListString)         list<string>;
};

%pythoncode
%{
from api.module.module import *
class FUSE(Module):
  def __init__(self):
    Module.__init__(self, 'fuse', fuse)
    self.conf.add("parent", "node", True)
    self.conf.add("path", "path")
    self.tags = "file system"
%}
