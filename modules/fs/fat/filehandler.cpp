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

#include "filehandler.hpp"

FileHandler::FileHandler()
{
  inc = -1;
}

FileHandler::~FileHandler()
{
  unsigned long long	i;

  for (i = 0; i != inc; i++)
    delete handler[i];
}

unsigned long long	FileHandler::add(FileInfo* fi)
{
  try
    {
      handler.push_back(fi);
      return handler.size() - 1;
    }
  catch(...)
    {
      return ((unsigned long long)(-1));
    }
}

FileInfo*		FileHandler::get(unsigned long long handle)
{
  if (handle <= handler.size())
    {
      return handler[handle];
    }
  else
    {
      throw vfsError("Fat file handler: handle does not exist\n");
      return NULL;
    }
}
