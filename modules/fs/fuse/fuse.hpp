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

#ifndef __LOCAL_HH__
#define __LOCAL_HH__
#include <string>
#include <iostream>
#include <stdio.h>
#include <list>
#include "type.hpp"
#include "vfs.hpp"
#include "conf.hpp"
//#include "fdmanager.hpp"
#include "../local/utype.hpp"

#define FUSE_USE_VERSION 26

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <fuse.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <dirent.h>
#include <errno.h>
#include <sys/time.h>
#ifdef HAVE_SETXATTR
#include <sys/xattr.h>
#endif

using namespace std;

//VFS&	vfs = VFS::Get();
 
class fuse : public fso
{
public:
  fuse();
//  virtual ~fuse(){ /*close all system fd */};
  virtual void		start(argument* arg);
  virtual int 		vopen(Handle*) { return -1; };
  virtual int 		vread(int, void*, unsigned int) { return -1; };
  virtual int 		vwrite(int, void*, unsigned int) { return -1; };
  virtual int 		vclose(int) { return 0;  };
  virtual dff_ui64 	vseek(int, dff_ui64, int) { return -1 ;};
  virtual unsigned int  status() { return 1; };
};

#endif 
