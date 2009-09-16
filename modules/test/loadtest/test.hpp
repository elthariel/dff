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

#ifndef __LOCAL_HH__
#define __LOCAL_HH__
#include <string>
#include <iostream>
#include <stdio.h>
#include <list>
#include "type.hpp"
#include "vfs.hpp"
#include "conf.hpp"
#include "loader.hpp"
#include "fdmanager.hpp"

using namespace std;

class test : public fso
{
private:
public:
  test(string dname) {  name = dname;  res = new results(dname); };
  ~test(){ /*close all system fd */};
  virtual int 		vopen(Handle* handle);
  virtual int 		vread(int fd, void *buff, unsigned int size);
  virtual int 		vclose(int fd);
  virtual dff_ui64 	vseek(int fd, dff_ui64 offset, int whence);
  virtual int 		vwrite(int fd, void *buff, unsigned int size) { return 0; };
  virtual unsigned int	status(void);
  virtual void		start(argument* arg);
};
#endif 
