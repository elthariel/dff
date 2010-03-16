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

#include "boyer_moore.hpp"

BoyerMoore::BoyerMoore()
{
  this->bcs = NULL;
}

BoyerMoore::BoyerMoore(unsigned char *needle, unsigned int needlesize, unsigned char wildcard)
{
  this->bcs = NULL;
  if (needle != NULL)
    this->needle = needle;
  this->needleSize = needlesize;
  if (wildcard != 0x00)
    this->wildcard = wildcard;
  else
    this->wildcard = 0x00;
  if (this->computeBcs() == -1)
    ;
}

BoyerMoore::~BoyerMoore()
{
  if (this->bcs != NULL)
    delete this->bcs;
}

bool	BoyerMoore::preprocess()
{
  bool ret;

  ret = this->computeBcs();
  return ret;
}

bool	BoyerMoore::computeBcs()
{
  unsigned int	i;
  unsigned int	j;
  unsigned int	ridx = 0;
 
  if (this->needle != NULL)
  {
	this->bcs = (unsigned char*)malloc(sizeof(unsigned char) * UCHAR_MAX + 1);
	if (this->bcs == NULL || this->needleSize <= 0)
		return false;
	for (i = 0; i != UCHAR_MAX + 1; i++)
		this->bcs[i] = this->needleSize;
	for (i = 0; i < this->needleSize - 1; i++)
		{
			ridx = this->needleSize - i - 1;
			if (this->needle[i] == wildcard)
				for (j = 0; j <= UCHAR_MAX; j++)
					this->bcs[j] = ridx;
			this->bcs[this->needle[i]] = ridx;
		}
	return true;
  }
  return false;
}

unsigned int	BoyerMoore::charMatch(unsigned char c1, unsigned char c2)
{
  if (((wildcard != '\0') && (c1 == wildcard)) || (c1 == c2))
    return 1;
  else
    return 0;
}

unsigned int	BoyerMoore::charMatch(unsigned char c1, unsigned char c2, unsigned char w)
{
  if (((w != '\0') && (c1 == w)) || (c1 == c2))
    return 1;
  else
    return 0;
}

unsigned char			*BoyerMoore::generateBcs(pattern *p)
{
  unsigned int	i;
  unsigned int	j;
  unsigned int	ridx = 0;
  unsigned char	*bcs;
 
  bcs = (unsigned char*)malloc(sizeof(unsigned char) * UCHAR_MAX + 1);
  if ((bcs != NULL) && (p->size > 0))
    {
      for (i = 0; i != UCHAR_MAX + 1; i++)
	bcs[i] = p->size;
      for (i = 0; i < p->size - 1; i++)
	{
	  ridx = p->size - i - 1;
	  if (p->needle[i] == p->wildcard)
	    for (j = 0; j <= UCHAR_MAX; j++)
	      bcs[j] = ridx;
	  bcs[p->needle[i]] = ridx;
	}
    }
  return bcs;
}

int	BoyerMoore::search(unsigned char *haystack, unsigned int hslen, pattern *p, unsigned char *bcs)
{
  unsigned int	hspos;
  int		ndpos;
  //list<unsigned int> *l = new list<unsigned int>;
  int shift;

  hspos = 0;
  while (hspos <= (hslen - p->size))
    {
      for (ndpos = p->size - 1; ndpos >= 0, this->charMatch(p->needle[ndpos], haystack[hspos+ndpos], p->wildcard); ndpos--)
	;
      if (ndpos < 0)
	return hspos;
      else
	{
	  shift = bcs[(unsigned char)haystack[hspos + ndpos]] - p->size + 1 + ndpos;
	  if (shift <= 0)
	    shift = 1;
	  hspos += shift;
	}
    }
  return -1;
}

list<unsigned int>	*BoyerMoore::search(unsigned char *haystack, unsigned int hslen, unsigned int *count)
{
  unsigned int	hspos;
  int	ndpos;
  list<unsigned int> *l = new list<unsigned int>;
  int shift;

  hspos = 0;
  while ((hspos <= (hslen - this->needleSize)) && (*count != 0))
    {
      for (ndpos = this->needleSize - 1; ndpos >= 0, this->charMatch(this->needle[ndpos], haystack[hspos+ndpos]); ndpos--)
	;
      if (ndpos < 0)
	{
	  l->push_back(hspos);
	  if (this->needleSize == 1)
	    hspos++;
	  else
	    hspos += this->needleSize - 1;
	  (*count)--;
	}
      else
	{
	  shift = this->bcs[(unsigned char)haystack[hspos + ndpos]] - this->needleSize + 1 + ndpos;
	  if (shift <= 0)
	    shift = 1;
	  hspos += shift;
	}
    }
  return l;
}

list<unsigned int>	*BoyerMoore::search(unsigned char *haystack, unsigned int hslen)
{
  unsigned int	hspos;
  int	ndpos;
  list<unsigned int> *l = new list<unsigned int>;
  int shift;

  hspos = 0;
  while (hspos <= hslen - this->needleSize)
    {
      for (ndpos = this->needleSize - 1; ndpos >= 0 && this->charMatch(this->needle[ndpos], haystack[hspos+ndpos]); ndpos--)
	;
      if (ndpos < 0)
	{
	  l->push_back(hspos);
	  if (this->needleSize == 1)
	    hspos++;
	  else
	    hspos += this->needleSize - 1;
	}
      else
	{
	  shift = this->bcs[(unsigned char)haystack[hspos + ndpos]] - this->needleSize + 1 + ndpos;
	  if (shift <= 0)
	    shift = 1;
	  hspos += shift;
	}
    }
  return l;
}

bool	BoyerMoore::setNeedleSize(unsigned int ns)
{
  bool	ret;

  ret = true;
  if (ns != 0)
    this->needleSize = ns;
  else
    ret = false;
  return ret;
}

bool	BoyerMoore::setNeedle(unsigned char *n)
{
  bool ret;

  ret = true;
  if (n != NULL)
    this->needle = n;
  else
    ret = false;
  return ret;
}

bool	BoyerMoore::setWildcard(unsigned char w)
{
  bool	ret;

  ret = true;
  if (wildcard != '\0')
    this->wildcard = w;
  else
    ret = false;
  return ret;
}

unsigned char	*BoyerMoore::getNeedle()
{
  return this->needle;
}

unsigned char	BoyerMoore::getWildcard()
{
  return this->wildcard;
}
