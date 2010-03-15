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

#ifndef __PARTITION_HPP__
#define __PARTITION_HPP__

#include "common.hpp"
#include "fdmanager.hpp"
#include "filehandler.hpp"
#include "partition_struct.h"

#include <iostream>
#include <iomanip>
#include <sstream>

class Partition : public fso
{
private:
  class fdmanager		*fdm;
  FileHandler			*filehandler;
  std::ostringstream		Result;
  Node				*ParentNode;
  VFile				*File;
  unsigned int			part_count;

  int				SetResult();
  int				getParts();
  Node				*createPart(Node *parent, unsigned int sector_start, unsigned int size);
  void				readMbr();
  void				readExtended(Node *parent, unsigned int start, unsigned int next_lba);
  bool				isExtended(char type);
  string			hexilify(char type);

public:
  int		Close();
  int		Open();
  int		Read(void *buff, unsigned int size);
  dff_ui64	Seek(dff_ui64 offset);

  Partition();
  ~Partition();

  virtual void		start(argument* arg);
  virtual unsigned int	status(void);
  virtual int vopen(Handle* handle);
  virtual int vread(int fd, void *buff, unsigned int size);
  virtual int vclose(int fd);
  virtual dff_ui64 vseek(int fd, dff_ui64 offset, int whence);
  virtual int vwrite(int fd, void *buff, unsigned int size){return 0;};
};

#endif
