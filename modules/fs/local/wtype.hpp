/* 
 * DFF -- An Open Source Digital Forensics Framework
 * Copyright (C) 2009 ArxSys
 * 
 * This program is free software, distributed under the terms of
 * the GNU General Public License Version 2. See the LICENSE file
 * at the top of the source tree.
 * 
 * See http://www.digital-forensic.org for more information about this
 * project. Please do not directly contact any of the maintainers of
 * DFF for assistance; the project provides a web site, mailing lists
 * and IRC channels for your use.
 * 
 * Author(s):
 *  Solal Jacob <sja@digital-forensic.org>
 *
 */

#ifndef __WTYPE_HPP__
#define __WTYPE_HPP__

#include "type.hpp"
#include <time.h>
#include <sys/stat.h>
#include <String>
#include <windows.h>
#include <shlwapi.h>
#include <string>
#include <iostream>

class w_attrib : public attrib
{
public:
  w_attrib::w_attrib(WIN32_FILE_ATTRIBUTE_DATA info);
  w_attrib(WIN32_FIND_DATAA info);
};

class w_vtime : public vtime
{
public:
  w_vtime(FILETIME* t);
};

#endif
