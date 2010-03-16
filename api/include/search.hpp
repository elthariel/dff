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

#ifndef __SEARCH_HPP__
#define __SEARCH_HPP__

#include <string>
#include <list>
#include "export.hpp"
#include "type.hpp"

using namespace std;

class algorithm
{
public:
  //virtual algorithm(unsigned char *needle, unsigned int needlesize, unsigned char wildcard);
  //  virtual ~algorithm();
  virtual list<unsigned int>	*search(unsigned char *haystack, unsigned int hslen) = 0;
  virtual list<unsigned int>	*search(unsigned char *haystack, unsigned int hslen, unsigned int *count) = 0;
  virtual bool			preprocess() = 0;
  virtual bool			setNeedle(unsigned char *needle) = 0;
  virtual bool			setNeedleSize(unsigned int size) = 0;
  virtual bool			setWildcard(unsigned char wildcard) = 0;
  virtual unsigned char		*getNeedle() = 0;
  virtual unsigned char		getWildcard() = 0;
};

class Search
{
private:
  algorithm		*algo;
  unsigned char		*needle;
  unsigned int		needleSize;
  unsigned char		wildcard;
  bool			aligned;
  dff_ui64		blockSize;
  bool			preprocessed;

public:
  EXPORT Search();
  EXPORT Search(unsigned char *needle, unsigned int needlesize, unsigned char wildcard);
  EXPORT ~Search();
  EXPORT bool			setNeedle(unsigned char *n);
  EXPORT bool			setNeedleSize(unsigned int size);
  EXPORT bool			setWildcard(unsigned char w);
  EXPORT bool			setBlockSize(unsigned int bs);
  EXPORT bool			setAligned(bool aligned);
  EXPORT list<unsigned int>	*run(unsigned char *haystack, unsigned int hslen);
  EXPORT list<unsigned int>	*run(unsigned char *haystack, unsigned int hslen, unsigned int *count);
};

#endif
