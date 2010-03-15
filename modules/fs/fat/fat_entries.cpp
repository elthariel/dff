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

#include "fat.hpp"

int	Fat::EntryReader(unsigned char *Entry)
{
  dff_ui64	offset;
  unsigned int	next_cluster;
  unsigned int	bytesread;
  Info		*info;

  bytesread = 0;
  info = info_stack.top();
  if ((info->offset >= DataOffset) && (info->total_read >= (ClusterSize)))
    {
      info->total_read = 0;
      next_cluster = GetNextClusterEntry(info->cluster);
      if (next_cluster <= TotalCluster)
	{
	  offset = GETCLUSTEROFFSET(next_cluster, ClusterSize, DataOffset);
	  info->offset = offset;
	  info->cluster = next_cluster;
	  try 
	    {
	      Seek(info->offset);
	    }
	  catch (vfsError e)
	    {
	      return 0;
	    }
	}
      else
	{
	  return 0;
	}
    }
  try
  {
    bytesread = Read((void*)Entry, 32);
    info->total_read += bytesread;
    info->offset += bytesread;
    return (bytesread);
  }
  catch (vfsError e)
  {
    throw vfsError("Fat::EntryReader throw\n" + e.error);
    return 0;
  }

}

int	Fat::LongDirectoryEntry(unsigned char *Entry)
{
  LongFileName		*lfn;
  unsigned char		size;
  Info			*info;
  
  info = info_stack.top();
  lfn = (LongFileName*)malloc(sizeof(LongFileName));
  memset(lfn, 0, sizeof(LongFileName));
  memcpy(lfn, Entry, 32);
  info->LongDirEntries.push_front(lfn);
  return (0);
}

int	Fat::ShortDirectoryEntry(unsigned char *Entry)
{
  attrib*	attr = new attrib;
  RootDir	DirSpec;
  string	filename;
  string	name;
  Info		*info;
  int		i;
  char		tmp[26];
  list<LongFileName*>::iterator it;
  unsigned short ent;
  string	ext;

  info = info_stack.top();
  wchar_t unicode[1000];
  filename = "";
  if (!info->LongDirEntries.empty())
    {
      it = info->LongDirEntries.begin();
      while (it != info->LongDirEntries.end())
	{
	  memset(tmp, 0, 26);
	  memcpy(tmp, (*it)->fivechar, 10);
	  memcpy(tmp+10, (*it)->sixchar, 12);
	  memcpy(tmp+22, (*it)->twochar, 4);
	  for (i = 0; i != 26; i+=2)
	    {
	      memcpy(&ent, tmp+i, 2);
	      if ((ent == 0xFFFF) || (ent == 0x0000))
		break;
	      else if (ent < 0x0080)
		filename += tmp[i];
	      else
		filename += ".";
	    }
	  free(*it);
	  it++;
	  info->LongDirEntries.pop_front();
	}
    }
  else
    {
      memset(&DirSpec, 0, sizeof(RootDir));
      memcpy(&DirSpec, Entry, 32);
      if (DirSpec.Name[0] == 0xE5)
	i = 1;
      else
	i = 0;
      for (; i != 8; i++)
	{
	  if ((is_valid_char(DirSpec.Name[i]) == 0) && (DirSpec.Name[i] != ' ') && (DirSpec.Name[i] < 0x80))
	    name += DirSpec.Name[i];
	  else
	    break;
	}
      ext = "";
      for (i = 0; i != 3; i++)
	{
	  if ((is_valid_char(DirSpec.Ext[i]) == 0) && (DirSpec.Ext[i] != ' ') && (DirSpec.Ext[i] < 0x80) && (DirSpec.Ext[i] != 0x00))
	    ext += DirSpec.Ext[i];
	  else
	    break;
	}
      if (!name.empty())
	{
	  filename += name;
	  if (!ext.empty())
	    filename += "." + ext;
	}
    }
  info->filename = filename;
  if (filename.size() != 0)
    {
      //File
      if ((Entry[11] & (ATTR_DIRECTORY | ATTR_VOLUME_ID)) == 0x00)
	{
	  GetFile(Entry);
	  return 0;
	}
      //Directory
      else if ((Entry[11] & (ATTR_DIRECTORY | ATTR_VOLUME_ID)) == ATTR_DIRECTORY)
	{
	  GetDirectory(Entry);
	  return 0;
	}
      //Volume label
      else if ((Entry[11] & (ATTR_DIRECTORY | ATTR_VOLUME_ID)) == ATTR_VOLUME_ID)
	{
	  GetVolumeLabel(Entry);
	  return 0;
	}
      //Unknown Entry
      else
	{
	  return -1;
	}
      return -1;
    }
  return 0;
}

int	Fat::GetDirectory(unsigned char *Entry)
{
  Info		*newinfo = new Info;
  Info		*info;
  Node		*current;
  attrib	*attr = new attrib;
  unsigned int	cluster;
  RootDir	DirSpec;
  unsigned long long offset;

  if (Entry[0] != 0x2E)
    {
      info = info_stack.top();
      memset(&DirSpec, 0, sizeof(RootDir));
      memcpy(&DirSpec, Entry, 32);
      cluster = DirSpec.FirstClusterLo;
      if (FatType == FAT32)
	cluster |= (DirSpec.FirstClusterHi << 16);
      offset = GETCLUSTEROFFSET(cluster, ClusterSize, DataOffset);
      if (parsed_clusters.count(info->offset) == 0)
	{
	  parsed_clusters.insert(pair<unsigned int, bool>(info->offset, true));
	  SetAttr(DirSpec, attr);
	  if (Entry[0] == 0xE5)
	    {
	      deleted_dir++;
	      current = CreateNodeDir(DeletedItems, info->filename, attr);
	    }
	  else
	    {
	      total_dir++;
	      current = CreateNodeDir(info->parent, info->filename, attr);
	    }
	  newinfo->offset = offset;
	  newinfo->total_read = 0;
	  newinfo->parent = current;
	  newinfo->cluster = cluster;
	  newinfo->nname = info->nname + "/" + info->filename;
	  newinfo->filename = "";
	  info_stack.push(newinfo);
	  ListRec(info->nname, newinfo->offset, current, info->cluster, info->deleted);
	  delete info_stack.top();
	  info_stack.pop();
	  info = info_stack.top();
	  try
	    { 
	      Seek(info->offset);
	    } 
	  catch (vfsError e)
	    {
	      throw vfsError("Fat::GetDirectory\n" + e.error);
	    }
	}
      else
	{
	  return 0;
	}
      return (0);
    }
}
  
int	Fat::GetFile(unsigned char *Entry)
{
    Info	*info = info_stack.top();
    unsigned long long handle;
    attrib	*attr = new attrib;
    RootDir	DirSpec;
    string	path;

    memset(&DirSpec, 0, sizeof(RootDir));
    memcpy(&DirSpec, Entry, 32);
    path = info->nname + "/" + info->filename;
    if ((Entry[0] == 0xE5))
      {
	handle = RegisterFile(DirSpec, path, 1);
	if (handle != (unsigned long long)-1)
	  {
	    attr->handle = new Handle(handle);
	    attr->size = DirSpec.FileSize;
	    SetAttr(DirSpec, attr);
	    CreateNodeFile(DeletedItems, path.substr(path.rfind('/') + 1), attr);
	    deleted_file++;
	  }
	else
	  throw vfsError("Fat: cannot register file\n");
      }
    else
      {
	handle = RegisterFile(DirSpec, path, 0);
	if (handle != (unsigned long long)-1)
	  {
	    attr->handle = new Handle(handle);
	    attr->size = DirSpec.FileSize;
	    SetAttr(DirSpec, attr);
	    CreateNodeFile(info->parent, info->filename, attr);
	    total_file++;
	  }
	else
	  throw vfsError("Fat: cannot register file\n");
      }
    return (0);
  }

int	Fat::GetVolumeLabel(unsigned char *Entry)
{
  return (0);
}
