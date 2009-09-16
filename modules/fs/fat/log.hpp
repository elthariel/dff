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

#ifndef __LOG_HPP__
#define __LOG_HPP__

#include "common.hpp"

#include <stdio.h>
#include <stdarg.h>

// define type of logged information
#define DEBUG "[DEBUG] "
#define WARNING "[WARNING] "
#define MY_ERROR "[ERROR] "
#define INFO "[INFO] "
#define NONE ""

//define type of the output file
#define LOCAL (char)0
#define VIRTUAL (char)1

class Log
{
 private:
  VFile	*vfile;
  string lfile;
  int	fd;
  char	active;
 public:
  Log();
  Log(char a);
  Log(string output_file, char filetype);
  ~Log();
  int	log(char *fmt, ...);
};

#endif
