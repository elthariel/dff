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

%module  FAT 
%include "std_string.i"
%include "std_list.i"
%include "std_set.i"
%include "std_map.i"
%include "std_vector.i"
%include "windows.i"
%import "../../../api/vfs/libvfs.i"
//%import "../../../api/exceptions/libexceptions.i"

%{
//#include "../../../api/include/exceptions.hpp"

#include "fdmanager.hpp"
#include "common.hpp"
#include "fat_struct.h"
#include "log.hpp"
#include "filehandler.hpp"
#include "fat.hpp"
%}
%include "fdmanager.hpp"
%include "common.hpp"
%include "log.hpp"
%include "filehandler.hpp"
%include "fat.hpp"

namespace std
{
  %template(VecFI) vector<FileInfo*>;
  %template(VecUI) vector<unsigned int>;
  %template(VecFDI) vector<FDInfo* >;  
};

%pythoncode
%{
from api.module.module import *
class FAT(Module):
  def __init__(self):
    Module.__init__(self, 'fat', Fat)
    self.conf.add("parent", "node")
    self.conf.add_const("mime-type", "x86 boot sector")
    self.tags = "file system"
%}

