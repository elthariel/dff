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


#ifndef __TYPE_HPP__
#define __TYPE_HPP__

#include "export.hpp"
#include <stdlib.h>
#include <string>
#include <iostream>
#include <map>

typedef  unsigned long long dff_ui64;

#include "vtime.hpp"
#include "attrib.hpp"

union s_ull
{
  struct 
  {
    unsigned long Low;
    unsigned long High;
  };
  struct 
  {
    unsigned long Low;
    unsigned long High;
  }    u;
  unsigned long long ull;
};

using namespace std;

class Path
{
public:
  string	path;
  EXPORT 	Path(string p);
};

#endif

