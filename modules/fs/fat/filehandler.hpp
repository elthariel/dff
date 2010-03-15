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
 *  Frederic Baguelin <fba@digital-forensic.org>
 */

#ifndef __FILEHANDLER_HPP__
#define __FILEHANDLER_HPP__

#include "common.hpp"
#include "fat_struct.h"
#include "fdmanager.hpp"
#include "log.hpp"

class FileHandler
{
public:
  vector<FileInfo*>	handler;
  unsigned long long    inc;
  FileHandler();
  ~FileHandler();
  unsigned long long	add(FileInfo* fi);
  FileInfo*		get(unsigned long long handle);
};

#endif
