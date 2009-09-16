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
 *  Frederic Baguelin <fba@digital-forensic.org>
 *
 */

#ifndef __COMMON_HPP__
#define __COMMON_HPP__

#include <iostream>
#include <iomanip>
#include <stdio.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdlib.h>
#include <wchar.h>
#include <map>
#include <vector>
#include <queue>
#include <stack>

#include "type.hpp"
#include "vfs.hpp"
#include "conf.hpp"
#include "loader.hpp"

using namespace std;

typedef unsigned long long dff_ui64;

typedef struct s_FileInfo
{
  unsigned int	size;
  char		type;
  vector<unsigned int>	*clusters;
}		FileInfo;

#endif
