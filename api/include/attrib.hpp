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

#ifndef __ATTRIB_HPP__
#define __ATTRIB_HPP__

#include <string>
#include <map>
#include "type.hpp"

using namespace std;


class Handle
{
 public:
  Handle();

  EXPORT	Handle(dff_ui64);
  EXPORT	Handle(string);
  EXPORT	Handle(dff_ui64, string);
  dff_ui64	id;
  string	name;	
};

class attrib
{
public:

  EXPORT						attrib();
  EXPORT virtual					~attrib();

  map<string, string >   				smap; 
  map<string, vtime* > 					time; 
  map<string, unsigned int >  				imap; 
  dff_ui64	 					size; 
  Handle*						handle;	
};

#endif

