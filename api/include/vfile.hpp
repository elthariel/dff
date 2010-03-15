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

#ifndef __VPATH_HH__
#define __VPATH_HH__

#include <stdlib.h> 
#include <string>
#include <string.h>
#include "node.hpp"
#include "type.hpp"
#include "export.hpp"
#include "search.hpp"

using namespace std;

class Node;


#define BUFFSIZE 1024*1024*10

typedef struct _pdata
{
  void *buff;
  dff_ui64 len;
} pdata;


class VFile
{
private:
  Search	*s;

public:
  int		fd;	
  class 	Node*  		node;

  VFile() {s = new Search(); };
  EXPORT	int 		close(void);

  pdata*		read(void);
  pdata*		read(unsigned int size);
  EXPORT	int 		read(void *buff, unsigned int size);
  EXPORT	dff_ui64 	seek(dff_ui64 offset, char *whence);
  EXPORT	dff_ui64 	seek(dff_ui64 offset, int whence);
  EXPORT    	dff_ui64 	seek(dff_ui64 offset);
  EXPORT	long long	seek(int offset, int whence);
  EXPORT	int		write(string buff);
  EXPORT    	int		write(char *buff, unsigned int size);

  EXPORT	list<dff_ui64>	*search(char *needle, unsigned int len, char wildcard, dff_ui64 start = 0, dff_ui64 window = (dff_ui64)-1, unsigned int count = (unsigned int)-1);

  EXPORT	dff_ui64	find(char *needle, unsigned int len, char wildcard, dff_ui64 start=0, dff_ui64 window=(dff_ui64)-1);

  EXPORT	dff_ui64	rfind(char *needle, unsigned int len, char wildcard, dff_ui64 start=0, dff_ui64 window=(dff_ui64)-1);

  EXPORT	unsigned int	count(char *needle, unsigned int len, char wildcard, dff_ui64 start=0, dff_ui64 window=(dff_ui64)-1);

  EXPORT int		fileno();
  EXPORT dff_ui64 	tell();
};

#endif
