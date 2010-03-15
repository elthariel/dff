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
 *  Frederic B. <fba@digital-forensic.org>
 */

#ifndef __FDMANAGER_HH__
#define __FDMANAGER_HH__
#include <vector>
#include "export.hpp"
#include "type.hpp"
#include "vfs.hpp"

using namespace std;

/*FD Structure*/
class fileInfo 
{
  public:
  fileInfo();
  void*		buff;
  dff_ui64 	size;
  Node*		node;
};

class filePos
{
 public:
  filePos(fileInfo* fi);
  dff_ui64 current;
  fileInfo* fi;
};


class fdmanager
{
  public: 
  fdmanager();
  ~fdmanager();
  vector<filePos*>	fdm; //files descriptors map /
  unsigned int		fdallocated; 
  EXPORT bool		InitFDM();
  EXPORT bool		DeleteFDM();
  EXPORT bool		ClearFD(int fd);
  EXPORT dff_ui64	UpdateFD(int fd, dff_ui64 offset); 
  EXPORT unsigned int	AllocFD(filePos * fdinfo);
  EXPORT filePos	*GetFDInfo(int fd);
};

#endif
