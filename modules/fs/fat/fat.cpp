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

unsigned int	Fat::GetNextClusterEntry(unsigned int cluster)
{
  unsigned int	index;
  unsigned int	FatSecNum;
  unsigned int	FatEntryOffset;
  unsigned short NextClusterEntry;
  unsigned int	NextClusterEntry32;
  Info			*info;
  
  info = info_stack.top();
  if (FatType == FAT12)
    {
      index = cluster + cluster / 2;
      FatSecNum = index / Bpb.BytesPerSector;
      FatEntryOffset = index % Bpb.BytesPerSector;
      index = FatSecNum * Bpb.BytesPerSector + FatEntryOffset;
      try 
	{
	  Seek(FatOffset+index);
	  NextClusterEntry = 0xFFF;
	  Read(&NextClusterEntry, 2); 
	  Seek(info->offset);
	}
      catch (vfsError e) 
	{ 
	  throw vfsError("Fat::GetNexClusterEntry FAT12 throw\n" + e.error); 
	}
      if(cluster & 0x0001)
	NextClusterEntry = NextClusterEntry >> 4;
      else
	NextClusterEntry = NextClusterEntry & 0x0FFF;
      if (NextClusterEntry > TotalCluster)
	return (0x0FF8);
      else	  
	return (NextClusterEntry);
    }
  else if (FatType == FAT16)
    {
      index = cluster * 2;
      FatSecNum = index / Bpb.BytesPerSector;
      FatEntryOffset = index % Bpb.BytesPerSector;
      index = FatSecNum * Bpb.BytesPerSector + FatEntryOffset;
      try 
	{
	  Seek(FatOffset+index);
	  NextClusterEntry = 0xFFF8;
	  Read(&NextClusterEntry, 2);
	  Seek(info->offset);
	}
      catch (vfsError e) 
      { 
	throw vfsError("Fat::GetNexClusterEntry FAT16 throw\n" + e.error); 
      }
      if (NextClusterEntry > TotalCluster)
	return (0xFFF8);
      else
	return (NextClusterEntry);
    }
  else if (FatType == FAT32)
    {
      index = cluster * 4;
      FatSecNum = index / Bpb.BytesPerSector;
      FatEntryOffset = index % Bpb.BytesPerSector;
      index = FatSecNum * Bpb.BytesPerSector + FatEntryOffset;
      try 
	{
	  Seek(FatOffset+index);
	  NextClusterEntry32 = 0x0FFFFFF8;
	  Read(&NextClusterEntry32, 4);
	  Seek(info->offset);
	} 
      catch (vfsError e) 
      { 
	throw vfsError("Fat::GetNexClusterEntry FAT32 throw\n" + e.error); 
      }
      return (NextClusterEntry32);
    }
}

unsigned long long	Fat::RegisterFile(RootDir rd, string nname, char deleted)
{
  FileInfo *fi;
  vector<unsigned int>	*clusterchain;
  unsigned int	i;
  unsigned int	cluster;
  Info	*info = info_stack.top();
  unsigned long long inode;

  if ((rd.FileSize != 0xffffffff))
    {
      fi = new FileInfo;
      clusterchain = new vector<unsigned int>;
      fi->clusters = clusterchain;
      if (FatType == FAT12)
	{
	  cluster = rd.FirstClusterLo;
	  fi->size = rd.FileSize;
	  if (deleted == 1)
	    {
	      fi->clusters->push_back(cluster);
	      fi->type = DELETED;
	    }
	  else
	    {
	      fi->type = NORMAL;
	      while (cluster < 0x0FF8)
		{
		  fi->clusters->push_back(cluster);
		  cluster = GetNextClusterEntry(cluster);
		}
	    }
	  GetSlack(fi);
	  inode = filehandler->add(fi);
	  return inode;
	}
      
      if (FatType == FAT16)
	{
	  cluster = rd.FirstClusterLo;
	  fi->size = rd.FileSize;
	  if (deleted == 1)
	    {
	      fi->clusters->push_back(cluster);
	      fi->type = DELETED;
	    }
	  else
	    {
	      fi->type = NORMAL;
	      while (cluster < 0xFFF8)
		{
		  fi->clusters->push_back(cluster);
		  cluster = GetNextClusterEntry(cluster);
		}
	    }
	  GetSlack(fi);
	  inode = filehandler->add(fi);
	  return inode;
	}
      
      if (FatType == FAT32)
	{
	  cluster = rd.FirstClusterLo;
	  cluster |= (rd.FirstClusterHi << 16);
	  fi->size = rd.FileSize;
	  if (deleted == 1)
	    {
	      fi->clusters->push_back(cluster);
	      fi->type = DELETED;
	    }
	  else
	    {
	      fi->type = NORMAL;
	      while (cluster < 0x0FFFFFF8)
		{
		  fi->clusters->push_back(cluster);
		  cluster = GetNextClusterEntry(cluster) & 0x0FFFFFFF;
		}
	    }
	  GetSlack(fi);
	  inode = filehandler->add(fi);
	  return inode;
	}
    }
  else
    return 0;
}

int	Fat::ListRec(string name, dff_ui64 offset, Node *parent, unsigned int current_cluster, char deleted)
{
  unsigned int		nbread;
  Node			*current;
  Info			*info;
  unsigned char		*Entry;
  
  info = info_stack.top();
  try 
  {
  Seek(info->offset);
  }
  catch (vfsError e)
  {
    return (0);
  }
  Entry = (unsigned char*) malloc(sizeof(unsigned char) * 32);
  do
    {
      memset(Entry, 0, 32);
      nbread = EntryReader(Entry);
      if (nbread != 0)
 	{
	  if ((Entry[11] & (char)ATTR_LONG_NAME_MASK) == ATTR_LONG_NAME)
	    LongDirectoryEntry(Entry);
	  else if ((Entry[11] & (char)ATTR_LONG_NAME_MASK) != ATTR_LONG_NAME)
	    {
	      if (ShortDirectoryEntry(Entry) == -1)
		return 0;
	    }
	  else
	    return 0;
	}
      else
	;
    }  while ((Entry[0] != 0x00));
  return 0;
}

void Fat::start(argument* arg)
{
  attrib	*attr;
  Node	*root;
  string path;
  Info	*info;


  fdm = new fdmanager;
  fdm->InitFDM();
  filehandler = new FileHandler();
  attr = new attrib;
  arg->get("parent", &ParentNode);
  root = CreateNodeDir(ParentNode, "Fat", attr);
  SlackNode = CreateNodeDir(root, "Slack", attr);
  BaseTree = CreateNodeDir(root, "Base-Tree", attr);
  DeletedItems = CreateNodeDir(root, "Deleted-Items", attr);
  Open();
  DumpSize = ParentNode->attr->size;
  log->log(DEBUG "Dumpsize: %lld", DumpSize);

  if (DefineFatType() != -1)
    {
      info = new Info;
      info->offset = RootDirOffset;
      info->total_read = 0;
      info->cluster = 0;
      info->parent = BaseTree;
      info->filename = "";
      info->nname = "";
      info_stack.push(info);
      
      ListRec((char*)path.c_str(), RootDirOffset, BaseTree, 0, 0);
      SetResult();
      cout << endl;
    }
  return ;
}

int	Fat::SetResult()
{
  char* cres = new char[1024];
  string Result;

  sprintf(cres, "Type of Fat: %d\n", FatType);
  Result = cres;
  sprintf(cres, "Number of Fat %d\n", Bpb.NumberOfFat);
  Result += cres;
  sprintf(cres, "Number of Cluster: %d\n", TotalCluster);
  Result += cres;
  sprintf(cres, "Sectors per Cluster: %d\n", Bpb.SectorsPerCluster);
  Result += cres;
  Result += "-------------------\n";
  Result += "Size (bytes -- hex)\n";
  Result += "-------------------\n";
  sprintf(cres, "Fat: %d -- 0x%08x\n", FatSize, FatSize);
  Result += cres;
  sprintf(cres, "Root Directory: %d -- 0x%08x\n", RootDirSize, RootDirSize);
  Result += cres;
  sprintf(cres, "Bytes Per Sector: %d -- 0x%08x\n", Bpb.BytesPerSector, Bpb.BytesPerSector);
  Result += cres;
  Result += "----------------------\n";
  Result += "Offsets (bytes -- hex)\n";
  Result += "----------------------\n";
  sprintf(cres, "Fat: %d -- 0x%08x\n", FatOffset, FatOffset);
  Result += cres;
  sprintf(cres, "Root Directory: %d -- 0x%08x\n", RootDirOffset, RootDirOffset);
  Result += cres;
  sprintf(cres, "Data Region: %d -- 0x%08x\n", DataOffset, DataOffset);
  Result += cres;
  Result += "----------------------\n";
  sprintf(cres, "Total File: %d\n", total_file);
  Result += cres;
  sprintf(cres, "Total Dir: %d\n", total_dir);
  Result += cres;
  sprintf(cres, "Deleted File: %d\n", deleted_file);
  Result += cres;
  sprintf(cres, "Deleted Directory: %d\n", deleted_dir);
  Result += cres;
  Result += "----------------------\n";
  res->add_const("result", Result);

  return (0);
}

int	Fat::DefineFatType()
{
  int	RootDirSector;
  int	FatSz;
  int	DataSector;
  int	res;
  BiosParameterBlock32 Bpb32;

  log->log(INFO "FAT: DefineFatType() : Reading bios parameter block");
  if (Read(&Bpb, sizeof(BiosParameterBlock)) < 0)
    {
      log->log(MY_ERROR "FAT: DefineFatType() : Reading bios parameter block");
      return (-1);
    }
  log->log(INFO "FAT: DefineFatType() : Checking sanity of bytes per sector field");
  if ((Bpb.BytesPerSector <= 0) || ((Bpb.BytesPerSector % 512) != 0))
    {
      log->log(MY_ERROR "FAT: DefineFatType() : Checking sanity of bytes per sector field %d", Bpb.BytesPerSector);
      return -1;
    }
  log->log(INFO "FAT: DefineFatType() : Checking sanity of root directory entry size field");
  log->log(INFO "FAT: DefineFatType() : Calculating size of root directory in sectors");
  RootDirSector = ((Bpb.RootEntrySize * 32) + (Bpb.BytesPerSector - 1)) / Bpb.BytesPerSector;
  log->log(INFO "FAT: DefineFatType() : Checking sanity of bios parameter block");
  if (Bpb.FatSize != 0)
    FatSz = Bpb.FatSize;
  else if (Bpb.TotalSector16 == 0)
    {
      Read(&Bpb32, 54);
      FatSz = Bpb32.FAT_sector_size;
    }
  else
    return (-1);

  if (Bpb.TotalSector16 != 0)
    TotalSector = Bpb.TotalSector16;
  else
    TotalSector= Bpb.TotalSector32;

  log->log(INFO "Expected Number of sectors : %d\n", TotalSector);
  log->log(INFO "Effective Number of sectors : %lld\n", DumpSize / Bpb.BytesPerSector);
  if ((TotalSector > (DumpSize / Bpb.BytesPerSector)) || (TotalSector <= 0))
    log->log(WARNING "Total Sector exceeded the file size\n");
  DataSector = TotalSector - (Bpb.ReservedSector + (Bpb.NumberOfFat * FatSz) + RootDirSector);
  TotalCluster = DataSector / Bpb.SectorsPerCluster;

  log->log(INFO "Data sector: %d -- 0x%x\n", DataSector, DataSector);
  log->log(INFO "Total Cluster: %d -- 0x%x\n", TotalCluster, TotalCluster);

  ClusterSize = Bpb.BytesPerSector * Bpb.SectorsPerCluster;
  log->log(INFO "Cluster size: %d -- 0x%x\n", ClusterSize, ClusterSize);

  RootDirSize = RootDirSector * Bpb.BytesPerSector;

  FatSize = FatSz * Bpb.BytesPerSector;
  log->log(INFO "Fat size: %d -- 0x%x\n", FatSize, FatSize);

  FatOffset = Bpb.ReservedSector * Bpb.BytesPerSector;
  log->log(INFO "Fat offset: %d -- 0x%x\n", FatOffset, FatOffset);

  if(TotalCluster < 4085)
    {
      FatType = FAT12;
      RootDirOffset = FatOffset + (FatSize * Bpb.NumberOfFat);
      DataOffset = (Bpb.ReservedSector * Bpb.BytesPerSector) + (Bpb.NumberOfFat * FatSize) + RootDirSize;
      log->log(INFO "Data offset: %d -- 0x%x\n", DataOffset, DataOffset);
      log->log(INFO "Root directory offset: %d -- 0x%x\n", RootDirOffset, RootDirOffset);
    }
  else if(TotalCluster < 65525)
    {
      FatType = FAT16;
      RootDirOffset = FatOffset + (FatSize * Bpb.NumberOfFat);
      DataOffset = (Bpb.ReservedSector * Bpb.BytesPerSector) + (Bpb.NumberOfFat * FatSize) + RootDirSize;
      log->log(INFO "Data offset: %d -- 0x%x\n", DataOffset, DataOffset);
      log->log(INFO "Root directory offset: %d -- 0x%x\n", RootDirOffset, RootDirOffset);
    }
  else
    {
      FatType = FAT32;
      DataOffset = (Bpb.ReservedSector * Bpb.BytesPerSector) + (Bpb.NumberOfFat * FatSize);
      RootDirOffset = GETCLUSTEROFFSET(Bpb32.root_dir_cluster, ClusterSize, DataOffset);
      log->log(INFO "Data offset: %d -- 0x%x\n", DataOffset, DataOffset);
      log->log(INFO "Root directory offset: %d -- 0x%x\n", RootDirOffset, RootDirOffset);
    }
  log->log(INFO "Fat type: %d\n", FatType);
  return (0);
}

unsigned int Fat::status(void)
{
  return (fdm->fdallocated);
}

Fat::~Fat()
{
  delete filehandler;
  cout << " Fat instance destructor called" << endl;
  Close();
}

Fat::Fat()
{
  name = "fat";
  //fdm = new fdmanager;
  //fdm->InitFDM();
  File = 0;
  total_file = 0;
  total_dir = 0;
  deleted_file = 0;
  deleted_dir = 0;
  res = new results(name);
  log = new Log(0);
//  filehandler = new FileHandler();
}
/*
extern "C"
{
  fso* create(void)
  {
      return (new Fat("fat"));
  }

  void destroy(fso *p)
  {
    delete p;
  }

  class proxy
  {
    public :
    proxy()
    {
      CModule* cmod = new CModule("fat", create);
      cmod->conf->add("parent", "node");
      cmod->conf->add_const("mime-type", std::string("x86 boot sector"));
      cmod->tags = "fs";	
    }
  };
  proxy p;
}*/
