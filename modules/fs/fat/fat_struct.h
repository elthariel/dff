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

#ifndef __FAT_STRUCT_H__
#define __FAT_STRUCT_H__

#define ATTR_READ_ONLY	(char)0x01
#define ATTR_HIDDEN 	(char)0x02
#define ATTR_SYSTEM 	(char)0x04
#define ATTR_VOLUME_ID 	(char)0x08
#define ATTR_DIRECTORY	(char)0x10
#define ATTR_ARCHIVE  	(char)0x20
#define ATTR_LONG_NAME 	(char)(ATTR_READ_ONLY | ATTR_HIDDEN | ATTR_SYSTEM | ATTR_VOLUME_ID)
#define ATTR_LONG_NAME_MASK (char)(ATTR_READ_ONLY | ATTR_HIDDEN | ATTR_SYSTEM | ATTR_VOLUME_ID | ATTR_DIRECTORY | ATTR_ARCHIVE)

typedef std::basic_string<short> ustring;

#ifdef WIN32
#define PACK
#else
#define PACK __attribute__((packed))
#endif

/* /=======================================\ */
/* | Structures inherent to FAT FileSystem | */
/* \=======================================/ */
#ifdef WIN32
#pragma pack(1)
#endif
typedef struct s_BiosParameterBlock
{
  unsigned char		JmpBoot[3];
  unsigned char		Name[8];
  unsigned short	BytesPerSector;
  unsigned char		SectorsPerCluster;
  unsigned short	ReservedSector;
  unsigned char		NumberOfFat;
  unsigned short	RootEntrySize;
  unsigned short	TotalSector16; //16 bits
  unsigned char		Media;
  unsigned short	FatSize; // in sector
  unsigned short	SectorPerTrack;
  unsigned short	NumHeads;
  unsigned int		HiddenSectors;
  unsigned int		TotalSector32; //32 bits
}			PACK BiosParameterBlock;

#ifdef WIN32
#pragma pack(1)
#endif
typedef struct	s_BiosParameterBlock1216
{
  unsigned char	DiskId;
  unsigned char	not_use;
  unsigned char	Signature;
  unsigned int	Disk_serial;
  unsigned char	Disk_Name[11];
  unsigned char	FS_Type[8];
}PACK BiosParameterBlock1216;

#ifdef WIN32
#pragma pack(1)
#endif
typedef struct	s_BiosParameterBlock32
{
  unsigned int	FAT_sector_size;
  unsigned short	disk_attrib;
  unsigned char	Major_version;
  unsigned char	minor_version;
  unsigned int	root_dir_cluster;
  unsigned short	additional_info;
  unsigned short	Sector_of_BS;
  unsigned char  not_use[12];
  unsigned char	Disk_Id;
  unsigned char	not_use1;
  unsigned char  Signature;
  unsigned int	Disk_Serial;
  unsigned char	Disk_Name[11];
  unsigned char	FS_Type[8];
}PACK BiosParameterBlock32;

#ifdef WIN32
#pragma pack(1)
#endif
typedef struct s_RootDir
{
  unsigned char	Name[8];
  unsigned char Ext[3];
  unsigned char	Attr;
  unsigned char	NtRes;
  unsigned char	CreatedTimeTenth;
  unsigned short CreatedTime;
  unsigned short CreatedDate;
  unsigned short LastAccessedDate;
  unsigned short FirstClusterHi;
  unsigned short LastModifiedTime;
  unsigned short LastModifiedDate;
  unsigned short FirstClusterLo;
  unsigned int	FileSize;
}PACK RootDir;

#ifdef WIN32
#pragma pack(1)
#endif
typedef struct s_LongFileName
{
  unsigned char	order;
  unsigned char fivechar[10];
  unsigned char	attrib;
  unsigned char	reserved;
  unsigned char	checksum;
  unsigned char sixchar[12];
  unsigned short cluster;
  unsigned char twochar[4];
}PACK		LongFileName;

#endif
