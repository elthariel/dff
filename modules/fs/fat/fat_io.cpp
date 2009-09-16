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

int	Fat::Open()
{
  try 
  {
      File = ParentNode->open();
  }
  catch(vfsError e)
    {
      throw vfsError("Fat::Open() throw\n" +  e.error);
    }
  return (1);
}

int	Fat::Read(void *buff, unsigned int size)
{
  try 
    {
      return (File->read(buff, size));
    }
  catch(vfsError e)
    {
      throw vfsError("Fat::Read throw\n" + e.error);
    }
  return (1);
}

dff_ui64	Fat::Seek(dff_ui64 offset)
{
  try
    {
      offset = File->seek(offset);
      return (offset);
    }
  catch(vfsError e)
    {
      throw vfsError("Fat::Seek throw\n" + e.error);
    }
}

dff_ui64	Fat::Seek(dff_ui64 offset, int whence)
{
  try
    {
      offset = File->seek(offset, whence);
      return (offset);
    }
  catch(vfsError e)
    {
      return (0);
    }
}

int	Fat::Close()
{
  try
    {
      File->close();
    }
  catch(vfsError e)
    {
      throw vfsError("Fat::Close throw\n" + e.error);
    }
}

int	Fat::vopen(Handle *handle)
{
  FileInfo	*fi;
  FDInfo	*fd;
  int		i;

  if (handle == NULL)
     throw vfsError("Fat::vopen handle null\n"); 
  try
    {
      fi = filehandler->get(handle->id);
      if (fi != NULL)
	{
	  fd = new FDInfo;
	  fd->fdata = (void*)fi;
	  fd->current = 0;
	  i = fdm.AllocFD(fd);
	  return (i);
	}
      else
	throw vfsError("Fat::vopen can't find\n"); 
    }
  catch(...)
    {
      throw vfsError("Fat::vopen can't find\n"); 
      return -1;
    }
  return -1;
}

int	Fat::vread(int fd, void *buff, unsigned int size)
{
  unsigned int	BytesRead;
  unsigned int	Size;
  unsigned int	real_size;
  unsigned int	index;
  unsigned int	TotalBytesRead;
  unsigned int	Cluster;
  unsigned int	OffsetInCluster;
  dff_ui64	RealOffset;
  FDInfo	*vfd;
  FileInfo	*fi;

  TotalBytesRead = 0;
  vfd = fdm.GetFDInfo(fd);
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
	      vector<unsigned int> tmp;
	      tmp = *(fi->clusters);
	      while (TotalBytesRead < Size)
		{
		  if (fi->type == SLACK)
		    {
		      if (fi->clusters->size() - 1 < 0)
			throw vfsError("Fat::vread error index\n");
		      Cluster = tmp[0];
		      OffsetInCluster = ClusterSize - fi->size + vfd->current;
		      RealOffset = (GETCLUSTEROFFSET(Cluster, ClusterSize, DataOffset));
		      RealOffset += OffsetInCluster;
		      real_size = Size;
		    }
		  else if (fi->type == NORMAL)
		    {
		      Cluster = vfd->current / ClusterSize;
		      OffsetInCluster = vfd->current - (Cluster * ClusterSize);
		      RealOffset = (GETCLUSTEROFFSET(tmp[Cluster],  ClusterSize, DataOffset));
		      RealOffset += OffsetInCluster;
		      if ((Size - TotalBytesRead) > (ClusterSize - OffsetInCluster))
			real_size = ClusterSize - OffsetInCluster;
		      else
			real_size = Size - TotalBytesRead;
		    }
		  else if (fi->type == DELETED)
		    {
		      RealOffset = (GETCLUSTEROFFSET(tmp[0],  ClusterSize, DataOffset)) + vfd->current;
		      real_size = Size;
		    }
		  else
		    real_size = 0;
		  try
		    {
		      Seek(RealOffset);
		      void *buffer = malloc(sizeof(char) * real_size);
		      memset(buffer, '\0', real_size);
		      BytesRead = Read(buffer, real_size);
		      CopyBuffer((char*)buff, (char*)buffer, TotalBytesRead, BytesRead);
		      free(buffer);
		      if (BytesRead == 0)
			return (TotalBytesRead);
		      TotalBytesRead += BytesRead;
		      vfd->current += BytesRead;
		    }
		  catch(vfsError e)
		    {
		      throw vfsError("Fat::vread throw\n" + e.error);
		    }
		}
	      return TotalBytesRead;
	    }
          throw vfsError("Fat::vread error size problem\n");
	}
      else
	printf("FI NULL !!!!\n");
    }
  else
    printf("FD NULL\n");
  throw vfsError("Fat::vread end\n");
}

int	Fat::vclose(int fd)
{
  FileInfo *fi;

  fdm.ClearFD(fd);
  return 0;
}

dff_ui64	Fat::vseek(int fd, dff_ui64 offset, int whence)
{
  FDInfo *vfd;
  FileInfo	*fi;

  vfd = fdm.GetFDInfo(fd);
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
