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

#include "search.hpp"
#include "boyer_moore.hpp"

Search::Search()
{
  this->algo = new BoyerMoore();
  this->preprocessed = false;
}

Search::~Search()
{
  delete this->algo;
}

Search::Search(unsigned char *needle, unsigned int needlesize, unsigned char wildcard)
{
  this->algo = new BoyerMoore(needle, needlesize, wildcard);
  this->preprocessed = true;
}

list<unsigned int>	*Search::run(unsigned char *haystack, unsigned int hslen)
{
  if (!this->preprocessed)
    this->algo->preprocess();
  return this->algo->search(haystack, hslen);
}

list<unsigned int>	*Search::run(unsigned char *haystack, unsigned int hslen, unsigned int *count)
{
  if (!this->preprocessed)
    this->algo->preprocess();
  return this->algo->search(haystack, hslen, count);
}

bool			Search::setNeedle(unsigned char *n)
{
  this->preprocessed = false;
  return this->algo->setNeedle(n);
}

bool			Search::setNeedleSize(unsigned int size)
{
  this->preprocessed = false;
  return this->algo->setNeedleSize(size);
}

bool			Search::setWildcard(unsigned char w)
{
  this->preprocessed = false;
  return this->algo->setWildcard(w);
}

bool			Search::setBlockSize(unsigned int bs)
{
  // this->preprocessed = false;
  return true;
}

bool			Search::setAligned(bool aligned)
{
  //  this->preprocessed = false;
  this->aligned = aligned;
  return true;
}
