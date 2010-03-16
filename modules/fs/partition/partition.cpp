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

#include "partition.hpp"
#include "common.hpp"


int	Partition::vclose(int fd)
{
  FileInfo *fi;

  this->fdm->ClearFD(fd);
  return 0;
}

int	Partition::Open()
{
  try 
    {
      File = ParentNode->open();
    }
  catch(vfsError e)
    {
      cout << e.error << endl;
      return (0);
    }
}

int	Partition::Read(void *buff, unsigned int size)
{
  try 
    {
      return (File->read(buff, size));
    }
  catch(vfsError e)
    {
      cout << e.error << endl;
      return (0);
    }
}

dff_ui64	Partition::Seek(dff_ui64 offset)
{
  try
    {
      offset = File->seek(offset);
      return (offset);
    }
  catch(vfsError e)
    {
      cout << e.error << endl;
      return (0);
    }
}

int	Partition::Close()
{
  try
    {
      File->close();
    }
  catch(vfsError e)
    {
      cout << e.error << endl;
      return (0);
    }
}

int	Partition::vopen(Handle* handle)
{
  FileInfo	*fi;
  FDInfo	*fd;

  if (handle == NULL)
     throw vfsError("Partition::vopen handle null\n"); 
  //cout << *((string*)(handle)) << endl;
  if ((fi = this->filehandler->get(handle->id)) != NULL)
    {
      fd = new FDInfo;
      fd->fdata = fi;
      fd->current = 0;
      int i = this->fdm->AllocFD(fd);
      return (i);
    }
  throw vfsError("Partition::vopen can't find\n");
}

void	*CopyBuffer(char *dst, char *src, unsigned int start, unsigned int size)
{
  char	*dstptr;
  char	*srcptr;
  int	i;

  for (i = 0, dstptr = dst + start, srcptr = src; i != size; i++, dstptr++, srcptr++)
    *dstptr = *srcptr;
  return ((void*)dstptr);
}

int	Partition::vread(int fd, void *buff, unsigned int size)
{
  dff_ui64	BytesRead;
  dff_ui64	Size;
  dff_ui64	real_size;
  dff_ui64	TotalBytesRead;
  dff_ui64	RealOffset;
  FDInfo	*vfd;
  FileInfo	*fi;
  
  vfd = this->fdm->GetFDInfo(fd);
  if (vfd != NULL)
    {
      fi = (FileInfo*)vfd->fdata;
      if (fi != NULL)
	{
	  Size = -1;
	  //memset(buff, '0', size);
	  // if file offset > size of file
	  if (vfd->current >= fi->size)
	    return (0);
	  //Requested size exceed file size ?
	  if (size > (fi->size - vfd->current))
	    Size = fi->size - vfd->current;
	  else
	    Size = size;
	  if (Size >= 0)
	    {
	      TotalBytesRead = 0;
	      while (TotalBytesRead < Size)
		{
		  RealOffset = (unsigned long long)fi->start + vfd->current;
		  Seek(RealOffset);
		  void *buffer = malloc(sizeof(char) * Size);
		  memset(buffer, '\0', Size);
		  BytesRead = (dff_ui64)Read(buffer, Size);
		  //printf("vread() -- BytesRead: %d\n", BytesRead);
		  CopyBuffer((char*)buff, (char*)buffer, TotalBytesRead, BytesRead);
		  free(buffer);
		  // Is EOF ?
		  // errors are catched in Read()
		  if (BytesRead == 0)
		    return (TotalBytesRead);
		  TotalBytesRead += BytesRead;
		  vfd->current += BytesRead;
		}
	      return TotalBytesRead;
	    }
	  //printf("Size Problem\n");
	  return -1;
	}
      else
	printf("FI NULL !!!!\n");
    }
  else
    printf("FD NULL\n");
  return -1;
}

dff_ui64	Partition::vseek(int fd, dff_ui64 offset, int whence)
{
  FDInfo *vfd;
  FileInfo	*fi;

  vfd = this->fdm->GetFDInfo(fd);
  fi = (FileInfo*)vfd->fdata;
  if (whence == 0)
    if (offset < fi->size)
    vfd->current = offset;
  if (whence == 1)
    if ((vfd->current + offset) < fi->size)
      vfd->current += offset;
    else
      return 0; //Gestion des erreurs !!!
  if (whence == 2)
    vfd->current = fi->size;
  return vfd->current;
}

bool	Partition::isExtended(char type)
{
   char	ext[] = "\x05\x0F\x85\x91\x9B\xD5";
   unsigned int	i;
   bool	res;
  
   res = false;
   for (i = 0; ext[i]; i++)
     if (ext[i] == type)
       res = true;
   return res;
}

Node	*Partition::createPart(Node *parent, unsigned int sector_start, unsigned int size)
{
  attrib		*attr;
  FileInfo		*fi;
  unsigned long long	handle;

  std::ostringstream os;

  attr = new attrib;
  fi = new FileInfo();
  fi->start = sector_start * 512;
  fi->size = size * 512;
  handle = this->filehandler->add(fi);
  attr->size = fi->size;
  attr->handle = new Handle(handle);
  os << "Partition " << this->part_count;
  this->part_count += 1;
  return CreateNodeFile(parent, os.str(), attr);
}

string	Partition::hexilify(char type)
{
  std::ostringstream		res;
  
  res << std::hex << std::setiosflags(ios_base::showbase | ios_base::uppercase);
  res << (int)type;
  return res.str();
}

void	Partition::readExtended(Node *parent, unsigned int start, unsigned int next_lba)
{
  ebr			ebrEntry;
  unsigned long long	startOffset;
  unsigned long long	endOffset;
  unsigned int	        i;
  bool			jumped;
  partition_entry	*part;
 
  startOffset = start + next_lba;
  this->Seek(startOffset * 512);
  memset(&ebrEntry, 0, sizeof(ebr));
  if (this->Read(&ebrEntry, sizeof(ebr)) != 0)
    {
      jumped = false;
      part = (partition_entry*)malloc(sizeof(partition_entry));
      for (i = 0; i != 4; i++)
	{
	  if (ebrEntry.part[i].type != 0)
	    {
	      memcpy(part, &(ebrEntry.part[i]), sizeof(partition_entry));
	      if (((i < 2) && jumped) || (i >= 2))
		this->Result << "Hidden partition !!!" << endl;
	      if (isExtended(part->type))
		this->readExtended(parent, start, part->lba);
	      else
		{
		  this->Result << "   +- Partition " << this->part_count << endl;
		  this->Result << "      |-- type  : " << this->hexilify(part->type) << endl;
		  this->Result << "      |-- start : " << part->lba + startOffset << endl;
		  this->Result << "      |-- end   : " << part->lba - 1 + part->total_blocks << endl;
		  this->Result << "      |-- size  : " << part->total_blocks << endl;
		  this->createPart(parent, part->lba + startOffset, part->total_blocks);
		}
	    }
	  else if (i < 2)
	    jumped = true;
	}
    }
}


//Only checking the type is not enough !!!
//anybody could set type to 0 to fake partition manager...
void	Partition::readMbr()
{
  mbr			mbrEntry;
  unsigned int		i;
  partition_entry	*part;
  bool			jumped;
  Node			*node;

  memset(&mbrEntry, 0, sizeof(mbr));
  if (this->Read(&mbrEntry, sizeof(mbr)) != 0)
    {
      jumped = false;
      part = (partition_entry*)malloc(sizeof(partition_entry));
      for (i = 0; i != 4; i++)
	{
	  if (mbrEntry.part[i].type != 0)
	    {
	      if (jumped)
		this->Result << "Hidden primary partition entry" << endl;
	      memcpy(part, &(mbrEntry.part[i]), sizeof(partition_entry));
	      if (this->isExtended(part->type))
		{
		  this->Result << "+- Partition " << this->part_count << " (extended)" << endl;
		  this->Result << "    |-- type  : " << this->hexilify(part->type) << endl;
		  this->Result << "    |-- start : " << part->lba << endl;
		  this->Result << "    |-- end   : " << part->lba - 1 + part->total_blocks << endl;
		  this->Result << "    |-- size  : " << part->total_blocks << endl;
		  node = this->createPart(this->ParentNode, part->lba, part->total_blocks);
		  this->readExtended(node, part->lba, 0);
		}
	      else
		{
		  this->Result << "+- Partition " << this->part_count << " (primary)" << endl;
		  this->Result << "    |-- type  : " << this->hexilify(part->type) << endl;
		  this->Result << "    |-- start : " << part->lba << endl;
		  this->Result << "    |-- end   : " << part->lba - 1 + part->total_blocks << endl;
		  this->Result << "    |-- size  : " << part->total_blocks << endl;
		  this->createPart(this->ParentNode, part->lba, part->total_blocks);
		}
	    }
	  else
	    jumped = true;
	}
      free(part);
    }
}

void Partition::start(argument* arg)
{
  attrib	*attr;
  string path;
  Info	*info;

  this->fdm = new fdmanager;
  this->fdm->InitFDM();
  this->filehandler = new FileHandler();
  this->part_count = 1;
  this->name = "partition";
  attr = new attrib;
  arg->get("parent", &this->ParentNode);
  Open();
  this->Result << endl;
  this->readMbr();
  if (this->part_count > 1)
    this->res->add_const("partitions found", this->Result.str());
  else
    this->res->add_const("no partition found", "");
  return;
}

int	Partition::SetResult()
{
  return (0);
}

unsigned int Partition::status(void)
{
  return (this->fdm->fdallocated);
}
Partition::Partition()
{
  this->name = "partition";
  res = new results(this->name);
}
Partition::~Partition()
{
  //Free All Memory !!!
  cout << "Dump Closed successfully" << endl;
}
