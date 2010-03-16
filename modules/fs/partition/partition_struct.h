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

#ifndef __PARTITION_STRUCT_HPP__
#define __PARTITION_STRUCT_HPP__

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

typedef struct		s_partition_entry
{
  char			status;//0x80 = bootable, 0x00 = non-bootable, other = invalid
  char			start_head;
  char		        start_sector; //sector in bit 5-0, bits 9-8 of cylinders are in bits 7-6...
  char			start_cylinder; // bits 7-0
  char			type;
  char			end_head;
  char			end_sector; //sector in bit 5-0, bits 9-8 of cylinders are in bits 7-6...
  char			end_cylinder; //bits 7-0
  unsigned int		lba;
  unsigned int		total_blocks;
}PACK		        partition_entry;

typedef struct		s_ebr
{
/*   Usually NULL, could contain another boot loader or smthg else... */
/*   could also contain IBM Boot Manager starting at 0x18A */
  char			code[446];

  partition_entry	part[4];

/*   Normally, there are only two partition entries in extended boot records */
/*   followed by 32 bytes of NULL byte. It could be used to hide data or even */
/*   2 other partition entries !!! */
/*   partition_entry	part[2]; */
/*   char		padding[32]; Usually NULL but could be used to hide smthg */

  short			mbr_signature;
}PACK			ebr;


typedef struct		s_mbr
{
  char			code[440];
  int			disk_signature;//or char DS[4];
  short			padding; //Usually NULL but could be used to hide smthg...
  partition_entry	part[4];
  short			mbr_signature; //0xAA55
}PACK			mbr;

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
#endif
