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

#ifndef __EXTRACT_HH__
#define __EXTRACT_HH__
#include <iostream>
#include <stdio.h>
#include <list>
#include "type.hpp"
#include "vfs.hpp"
#include "conf.hpp"
#include "loader.hpp"

using namespace std;

class extract : public fso
{
private:
public:
  extract(string dname) { name = dname; res = new results(name); };
  ~extract() {};
  virtual void		start(argument* arg);
  virtual int 		vopen(Handle* handle) { return 0; };
  virtual int 		vread(int fd, void *buff, unsigned int size) { return 0; };
  virtual int 		vclose(int fd) { return 0; };
  virtual dff_ui64 	vseek(int fd, dff_ui64 offset, int whence) { return 0; };
  virtual int 		vwrite(int fd, void *buff, unsigned int size) { return 0; };
  virtual unsigned int 	status(void);
};
#endif 
