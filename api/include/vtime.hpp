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

#ifndef __VTIME_HPP__
#define __VTIME_HPP__

#include "export.hpp"


class vtime
{
public:
  EXPORT		vtime();
  EXPORT virtual	~vtime();
  EXPORT 		vtime(int, int, int, int, int, int, int);
  int 			year;	
  int 			month;	
  int 			day;	
  int 			hour;	
  int 			minute;	
  int 			second;	
  int 			usecond; 
  int			wday;
  int			yday;	
  int			dst;
};

#endif

