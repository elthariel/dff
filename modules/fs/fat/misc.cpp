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
 *  Frederic Baguelin <fba@digital-forensic.org>
 *
 */

#include "fat.hpp"

void	patch_escape(char *str)
{
  char *tmp;

  for (tmp = str; *tmp; tmp++)
    if(*tmp == ' ')
      *tmp = '\0';
}

int	is_valid_eight_plus_three(char c)
{
 return 0;
}

int	is_valid_char(char c)
{
  char t[] = "\x22\x2A\x2B\x2C\x2E\x2F\x3A\x3B\x3C\x3D\x3E\x3F\x5B\x5C\x5D\x7C";
  int	i;

  i = 0;
  if (c >= 0x20)
    {
      while (t[i] != '\0')
	if (c == t[i])
	  return -1;
	else
	  i++;
      return 0;
    }
  return -1;
}

void	*CopyBuffer(char *dst, char *src, unsigned int start, unsigned int size)
{
  char	*dstptr;
  char	*srcptr;
  int	i;

  for (i = 0, dstptr = dst + start, srcptr = src; i != size; i++, dstptr++, srcptr++)
    *dstptr = *srcptr;
  return ((void*)dstptr);
}
