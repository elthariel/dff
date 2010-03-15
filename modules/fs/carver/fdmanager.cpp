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


#include "fdmanager.hpp"

dff_ui64 fdmanager::UpdateFD(int fd, dff_ui64 offset)
{
  if (fd >= fdm.size())
    return -1;
  else
    {
      fdm[fd]->current = offset;
      return (fdm[fd]->current);
    }
}

FDInfo	*fdmanager::GetFDInfo(int fd)
{
  if (fd >= fdm.size())
    return NULL;
  else
    return fdm[fd];
}

bool 	fdmanager::ClearFD(int fd)
{
  if (fd < fdm.size())
    {
      if (fdm[fd] != NULL)
	{
	  delete fdm[fd];
	  fdm[fd] = NULL;
	  fdallocated--;
	}
    }
  else
    return 0;
  return 1;
}

unsigned int 	fdmanager::AllocFD(FDInfo* fdinfo)
{
  int	fd;
  int	unalloc;
  FDInfo	*fdin = new FDInfo;

  if (fdallocated == fdm.size())
    {
      fdin->current = fdinfo->current;
      fdm.push_back(fdin);
      fd = fdm.size();
    }
  else
    {
      for (unalloc = 1; unalloc < fdm.size(); unalloc++)
	if (fdm[unalloc] == NULL)
	  break;
      fd = unalloc;
      fdm[fd] = fdinfo;
    }
  fdallocated++;

  return fd;
}

fdmanager::fdmanager()
{
}

fdmanager::~fdmanager()
{

}

bool 	fdmanager::InitFDM()
{
  int	i;

  fdallocated = 0;
  fdm.resize(65535);
  for (i = 0; i < fdm.size(); i++)
    fdm[i] = NULL;
  return 1;
}

bool 	fdmanager::DeleteFDM()
{
  int	i;

  for (i = 0; i < fdm.size(); i++)
    if (fdm[i] != NULL)
      delete fdm[i];
  fdm.clear();
  return 1;
}
