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
 *  Frederic Baguelin <fba@digital-forensic.org>
 */


#include "carver.hpp"

int Carver::vopen(Handle *handle)
{
  FileInfo	*fi;
  FDInfo	*fd;
  int		i;

  if (handle == NULL)
     throw vfsError("Carver::vopen handle null\n"); 
  try
    {
      fi = filehandler->get(handle->id);
      if (fi != NULL)
	{
	  fd = new FDInfo;
	  fd->fdata = fi;
	  fd->current = 0;
	  i = fdm->AllocFD(fd);
	  return (i);
	}
      else
	throw vfsError("Carver::vopen can't find\n"); 
    }
  catch(...)
    {
      throw vfsError("Carver::vopen can't find\n"); 
      return -1;
    }
  return -1;
}

int Carver::vread(int fd, void *buff, unsigned int size)
{
  unsigned int	BytesRead;
  unsigned int	Size;
  unsigned int	real_size;
  unsigned int	index;
  unsigned int	TotalBytesRead;
  dff_ui64	RealOffset;
  FDInfo	*vfd;
  FileInfo	*fi;


  TotalBytesRead = 0;
  vfd = fdm->GetFDInfo(fd);
  if (vfd != NULL)
    {
      fi = (FileInfo*)vfd->fdata;
      if (fi != NULL)
	{
	  Size = -1;
	  if (vfd->current >= fi->size)
	    return (0);
	  if (size > (fi->size - vfd->current))
	    Size = fi->size - vfd->current;
	  else
	    Size = size;
	  if (Size >= 0)
	    {
	      try
		{
		  this->ifile->seek(fi->offset + vfd->current);
		  BytesRead = this->ifile->read(((char *)buff) + TotalBytesRead, Size);
		  if (BytesRead == 0)
		    return (TotalBytesRead);
		  TotalBytesRead += BytesRead;
		  vfd->current += BytesRead;
		}
	      catch(vfsError e)
		{
		  throw vfsError("Carver::vread throw\n" + e.error);
		}
	    }
	  return TotalBytesRead;
	}
      throw vfsError("Carver::vread error size problem\n");
    }
  else
    printf("FI NULL !!!!\n");
}

int Carver::vclose(int fd)
{
  FileInfo *fi;

  fdm->ClearFD(fd);
  return 0;
}

dff_ui64 Carver::vseek(int fd, dff_ui64 offset, int whence)
{
  FDInfo	*vfd;
  FileInfo	*fi;

  vfd = fdm->GetFDInfo(fd);
  fi = (FileInfo*)vfd->fdata;
  if (whence == 0)
    if (offset < fi->size)
    vfd->current = offset;
  if (whence == 1)
    if ((vfd->current + offset) < fi->size)
      vfd->current += offset;
    else
      return 0;
  if (whence == 2)
    vfd->current = fi->size;
  return vfd->current;
}
