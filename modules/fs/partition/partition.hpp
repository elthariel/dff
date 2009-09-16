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
 *  Solal Jacob <sja@digital-forensic.org>
 *
 */

#ifndef __PARTITION_HPP__
#define __PARTITION_HPP__

#include "common.hpp"
#include "fdmanager.hpp"

#define SWAP_INT64(x) (   (((x)>>56) & 0x00000000000000FFLL)	\
			| (((x)>>40) & 0x000000000000FF00LL)	\
			| (((x)>>24) & 0x0000000000FF0000LL)	\
			| (((x)>>8)  & 0x00000000FF000000LL)	\
			| (((x)<<8)  & 0x000000FF00000000LL)	\
			| (((x)<<24) & 0x0000FF0000000000LL)	\
			| (((x)<<40) & 0x00FF000000000000LL)	\
			| (((x)<<56) & 0xFF00000000000000LL) )

#define SWAP_INT32(x) (   (((x)>>24) & 0x000000FFL) \
			| (((x)>>8)  & 0x0000FF00L)	\
			| (((x)<<8)  & 0x00FF0000L)	\
			| (((x)<<24) & 0xFF000000L) )

#define SWAP_INT16(x) (   (((x)>>8)  & 0x00FFL)	\
			| (((x)>>8)  & 0xFF00L)  )	\

#ifdef WIN32
#define PACK
#else
#define PACK __attribute__((packed))
#endif

#ifdef WIN32
#pragma pack(1)
#endif

typedef struct		s_PrimaryPartition
{
  char			Status;//0x80 = bootable, 0x00 = non-bootable, other = invalid
  char			StartHead;
  char			StartSectors; //sector in bit 5-0, bits 9-8 of cylinders are in bits 7-6...
  char			StartCylinders;
  char			PartitionType;
  char			LastHead;
  char			LastSectors; //sector in bit 5-0, bits 9-8 of cylinders are in bits 7-6...
  char			LastCylinders;
  unsigned int		Lba;
  unsigned int		TotalSectors;
}PACK			PrimaryPartition;

typedef struct		s_ExtendedBootRecords
{
  char			Unused[446];
  PrimaryPartition	Pp[2];
  char			Unused2[32];
  short			Signature;
}PACK			ExtendedBootRecords;


typedef struct		s_MBR
{
  char			CodeArea[440];
  int			DiskSignature;//or char DS[4];
  short			NullBytes;
  PrimaryPartition	Pp[4];
  short			MbrSignature; //0xAA55
}PACK			MBR;

typedef	struct s_Info
{
  dff_ui64	offset;
  unsigned int	cluster;
  unsigned int	total_read;
  string	filename;
  string	nname;
  Node		*parent;
  unsigned char deleted;
  unsigned char directory;
}		Info;

class Partition : public fso
{
private:
  //Private variables
  string			Result;
  Node				*ParentNode;
  map<string, FileInfo*>	FI;
  fdmanager			fdm;
  VFile				*File;

  //Private Methods
  int		Open();
  int		Read(void *buff, unsigned int size);
  dff_ui64	Seek(dff_ui64 offset);
  int		Close();
  int		SetResult();
  int		ListAll();
public:
  //public Method : pure virtual method for API
  Partition(string drvname);
  ~Partition();
  string Init(Node* node, string arg);
  virtual void		start(argument* arg);
  virtual unsigned int	status(void);
  virtual int vopen(Handle* handle);
  virtual int vread(int fd, void *buff, unsigned int size);
  virtual int vclose(int fd);
  virtual dff_ui64 vseek(int fd, dff_ui64 offset, int whence);
  virtual int vwrite(int fd, void *buff, unsigned int size){return 0;};
};

#endif
