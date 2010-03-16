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

#ifndef __FAT_HPP__
#define __FAT_HPP__

#include "common.hpp"
#include "fat_struct.h"
#include "fdmanager.hpp"
#include "log.hpp"
#include "filehandler.hpp"

#define LFNATTRIB	0x0f
#define GETCLUSTEROFFSET(cluster, clustersize, dataoffset) ((cluster - 2) * clustersize) + dataoffset
#define FAT12	(char)12
#define FAT16	(char)16
#define FAT32	(char)32
#define DIR	(char)1

#define NORMAL (char)0
#define SLACK (char)1
#define DELETED (char)2
#define BAD (char)3

typedef	struct s_Info
{
  dff_ui64	offset;
  unsigned int	cluster;
  unsigned int	total_read;
  string	filename;
  string	nname;
  Node		*parent;
  list<LongFileName*>	LongDirEntries;
  unsigned char deleted;
  unsigned char directory;
}		Info;

int	is_valid_char(char c);
void	*CopyBuffer(char *dst, char *src, unsigned int start, unsigned int size);

class Fat : public fso
{
private:
  stack<Info*>			info_stack;
  map<unsigned int, bool>	parsed_clusters;
  int				total_file;
  int				total_dir;
  int				deleted_file;
  int				deleted_dir;
  string			dumpname;
  string			modtype;
  Node				*DeletedItems;
  Node				*SlackNode;
  Node				*BaseTree;
  Log				*log;
  void				*FatAddr;
  char				FatType;
  BiosParameterBlock		Bpb;
  map<string, FileInfo*>	FI;

  EXPORT int	Open();
  EXPORT int	Read(void *buff, unsigned int size);
  EXPORT dff_ui64	Seek(dff_ui64 offset);
  EXPORT dff_ui64	Seek(dff_ui64 offset, int whence);
  EXPORT int	Close();
  unsigned int	GetNextClusterEntry(unsigned int cluster);
  int	DefineFatType();
  int	SetResult();
  unsigned long long	RegisterFile(RootDir rd, string nname, char deleted);
  int	ListRec(string name, dff_ui64 offset, Node *node, unsigned int current_cluster, char deleted);
  int	GetSlack(FileInfo *owner);
  int	EntryReader(unsigned char *buff);
  int	LongDirectoryEntry(unsigned char *Entry);
  int	ShortDirectoryEntry(unsigned char *Entry);
  int	GetDirectory(unsigned char *Entry);
  int	GetFile(unsigned char *Entry);
  int	GetVolumeLabel(unsigned char *Entry);
  void	SetAttr(RootDir rd, attrib *attr);
  vtime	*date_dos2vtime(unsigned short dos_time, unsigned short dos_date);
  int	FreeSpace();
  Node				*ParentNode;
public:
//must use arg* and init to reinit opened file
  string                        ParentNodePath;
  VFile				*File;
  unsigned int			FatOffset;
  unsigned int			ClusterSize;
  unsigned int			RootDirOffset;
  unsigned int			TotalCluster;
  unsigned int			TotalSector;
  unsigned int			DataOffset;
  unsigned int			FatSize;
  unsigned int			RootDirSize;
  unsigned long long		DumpSize;
  FileHandler			*filehandler;
  fdmanager 			*fdm;
  Fat();
  ~Fat();
  virtual void		start(argument *arg);
  virtual int vopen(Handle *handle);
  virtual int vread(int fd, void *buff, unsigned int size);
  virtual int vclose(int fd);
  virtual dff_ui64 vseek(int fd, dff_ui64 offset, int whence);
  virtual int vwrite(int fd, void *buff, unsigned int size){return 0;};
  virtual unsigned int status();
};

#endif
