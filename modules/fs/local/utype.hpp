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
 *  Solal Jacob <sja@digital-forensic.org>
 */

#ifndef __UTYPE_HPP__
#define __UTYPE_HPP__

#include "type.hpp"
#include <time.h>
#include <sys/stat.h>
#include <sys/ioctl.h>
#include <fcntl.h>
#include <sys/types.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <linux/fs.h>

class u_attrib : public attrib
{
public:
  u_attrib() {};
  u_attrib(struct stat *);
  u_attrib(struct stat *, char *path);
  void get_stat(struct stat*);
};

class u_vtime : public vtime
{
public:
  u_vtime() {};
  u_vtime(struct tm *t);
  struct tm*   get_tm(void);
};

#endif
