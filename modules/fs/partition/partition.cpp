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

#include "partition.hpp"

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
  if ((fi = FI.find(handle->name)->second) != NULL)
    {
      fd = new FDInfo;
      fd->fdata = (void*)fi;
      fd->current = 0;
      int i = fdm.AllocFD(fd);
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

// TODO
// Revoir le systeme de l extract : lecture de 512 a passer en 4096 ?
// sinon c'est long...
int	Partition::vread(int fd, void *buff, unsigned int size)
{
  dff_ui64	BytesRead;
  dff_ui64	Size;
  dff_ui64	real_size;
  dff_ui64	TotalBytesRead;
  dff_ui64	RealOffset;
  FDInfo	*vfd;
  FileInfo	*fi;
  
  vfd = fdm.GetFDInfo(fd);
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

int	Partition::vclose(int fd)
{
  FileInfo *fi;

  fdm.ClearFD(fd);
  return 0;
}

dff_ui64	Partition::vseek(int fd, dff_ui64 offset, int whence)
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
      return 0; //Gestion des erreurs !!!
  if (whence == 2)
    vfd->current = fi->size;
  return vfd->current;
}

// int	Partition::GetExtended()
// {
// }

int	Partition::ListAll()
{
  MBR	mbr;
  int	i;
  int	j;
  char	ext[] = "\x05\x0F\x85\x91\x9B\xD5";
  ExtendedBootRecords Ebr;
  unsigned long int test;
  unsigned long long int tmp; 
  FileInfo	*fi;
  string	path;

  memset(&mbr, 0, 512);
  Read(&mbr, 512);
  printf("/---------------------------------\\\n");
  printf("| Master Boot Record Information: |\n");
  printf("\\---------------------------------/\n");
  printf("Disk Signature: 0x%x\n", mbr.DiskSignature);
  printf("Mbr Signature:  0x%hx\n", mbr.MbrSignature);
  printf("\n/------------------------\\\n");
  printf("| Partition Information: |\n");
  printf("\\------------------------/\n");
  i = 0;
  while ((i !=4) && (mbr.Pp[i].PartitionType != 0))
    {
      printf("\n/-------------\\\n");
      printf("| Partition %i |\n", i + 1);
      printf("\\-------------/\n");
      printf("Boot flags:     0x%hhx\n", mbr.Pp[i].Status);
      printf("Partition Type: 0x%hhx\n", mbr.Pp[i].PartitionType);
      printf("Start Sector:   %d -- 0x%x\n", mbr.Pp[i].Lba, mbr.Pp[i].Lba);
      test = mbr.Pp[i].Lba * 512;
      tmp = (unsigned long long int)(mbr.Pp[i].TotalSectors) * 512;
      //tmp = tmp * 512;
      //tmp = 12345678901234ULL;
      printf("Start Offset:   0x%lx\n", test);
      printf("Size: %llu\n", tmp);

      //printf("TESTING: %llu\n", mbr.Pp[i].TotalSectors * 512);
      string handle;
      attrib	*attr = new attrib;

      path = "part";
      char* res = new char[1024];
      sprintf(res, "%d", i);
      path += res;
      handle = path;
      fi = new FileInfo;
      fi->start = mbr.Pp[i].Lba * 512;
      fi->size = tmp;
      attr->handle = new Handle(handle);
      attr->size = tmp;
      FI.insert(pair<string, FileInfo*>(path, fi));
      CreateNodeFile(ParentNode, path, attr);
      
      for (j = 0; ext[j]; j++)
	if (mbr.Pp[i].PartitionType == ext[j])
	  {
	    printf("Extended Partition\n");
	    //Seek(mbr.Pp[i].Lba*512)
	  }
      i++;
    }
  return 0;
}

// int	Partition::GetMbr(MBR *mbr)
// {
// }

// int	Partition::GetPartitionEntry()
// {
// }

// Analyse de sparse (Recherche de Cluster non allouees dans la Fat)
// Parsing de la Fat : si non alloue, allez voir le contenu du cluster
void Partition::start(argument* arg)
{
  attrib	*attr;
  //Node	*root;
  string path;
  Info	*info;

  attr = new attrib;
  arg->get("parent", &this->ParentNode);
  printf("sizeof unsigned long long int: %d\n", sizeof(unsigned long long int));
  //root = CreateNodeDir(parent, "Partition", attr);
  Open();
  ListAll();
  //SetResult();
  cout << endl;
  return;
}

int	Partition::SetResult()
{
  //char* cres	= new cres[1024];
  //String Result;

  //  "Partition Table Information\n";
//   sprintf(res, "Type of Fat: %d\n", FatType);
  // Result = cres;
//   sprintf(res, "Number of Fat %d\n", Bpb.NumberOfFat);
//  Result += res;
  //Result += "----------------------\n";
  return (0);
}

unsigned int Partition::status(void)
{
  return (fdm.fdallocated);
}

Partition::~Partition()
{
  //Free All Memory !!!
  cout << "Dump Closed successfully" << endl;
}

Partition::Partition(string dname)
{
  name = dname;
  fdm.InitFDM();
  //total_file = 0;
  //total_dir = 0;
  //deleted_file = 0;
  //deleted_dir = 0;
  res = new results(dname);
}

extern "C"
{
  fso* create(void)
  {
    return (new Partition("partition"));
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
      CModule* cmod = new CModule("partition", create);
      cmod->conf->add("parent", "node");
      cmod->tags = "fs";
      //drv->conf->add_const("mime-type", std::string("x86 boot sector"));
    }
  };

  proxy p;
}
