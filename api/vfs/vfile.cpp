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
 *  Solal J. <sja@digital-forensic.org>
 *
 */

#include "vfile.hpp"

int VFile::read(void *buff, unsigned int size)
{  
  int n;

  try 
  {
    n = node->fsobj->vread(fd, buff, size);
    return (n);
  }
  catch (vfsError e)
  {
    throw vfsError("Vfile::read(buff, size) throw\n" + e.error); 
  }
}

pdata* VFile::read(void)
{
  int n;
  pdata* data = new pdata;
  data->buff = malloc(node->attr->size);
  data->len = node->attr->size;
  try 
  {
    n = node->fsobj->vread(fd, (void*)data->buff, node->attr->size);
    data->len = n;	
    return (data);
  }
  catch (vfsError e)
  {
    free(data->buff);
    free(data);
    throw vfsError("VFile::read() throw\n" + e.error);
  }
}

pdata* VFile::read(unsigned int size)
{
  int n;
  pdata* data = new pdata;
  data->buff = malloc(size); 
  data->len = size;

  memset(data->buff, 0, size);
  try 
  { 
    n = node->fsobj->vread(fd, (void*)data->buff, size);
    data->len = n;	
    return (data);
  }
  catch (vfsError e)
  {
    free(data->buff);
    free(data);
    throw vfsError("VFile::read(size) throw\n" + e.error);
  }
}

int VFile::close(void)
{
  try 
  {
    node->fsobj->vclose(fd);
  }
  catch (vfsError e)
  {
     throw vfsError("Vfile::close() throw\n" + e.error);
  }
  return 0;
}


int VFile::write(string buff)
{
  int n;
   
  fso *fsobj = node->fsobj;
   try 
   {
     n = fsobj->vwrite(fd, (void *)buff.c_str(), buff.size());
     node->attr->size += n;
     return (n);
   }
   catch (vfsError e)
   {
      throw vfsError("VFile::write(string) throw\n" + e.error);
   }
}

int VFile::write(char *buff, unsigned int size)
{
  int n;
  fso *fsobj = node->fsobj;

   try 
   {
     n = fsobj->vwrite(fd, buff, size);
     node->attr->size += n;
     return (n);
   }
   catch (vfsError e)
   {
      throw vfsError("VFile::write(buff, size) throw\n" + e.error);
   }
}

dff_ui64 VFile::seek(dff_ui64 offset)
{
  try
  {
    return (node->fsobj->vseek(fd, offset, 0));
  }
  catch (vfsError e)
  {
    throw vfsError("VFile::seek(dff_ui64) throw\n" + e.error);
  }
}

dff_ui64  VFile::seek(dff_ui64 offset, char *cwhence)
{
  int wh;
  string whence = cwhence;   

  if (whence == string("SET"))
    wh = 0;
  else if (whence == string("CUR"))
    wh = 1;
  else if (whence == string("END"))
    wh = 2;
  else
  {
     throw vfsError("VFile::vseek(dff_ui64, char *) error whence not defined ( SET, CUR, END )");
  }
  try
  { 
   return (node->fsobj->vseek(fd, offset, wh));
  }
  catch (vfsError e)
  {
    throw vfsError("VFile::seek(dff_ui64, char*) throw\n" + e.error);
  }
}

dff_ui64  VFile::seek(dff_ui64 offset, int whence)
{
  if (whence > 2)
  {
     throw vfsError("VFile::vseek(offset, whence) error whence not defined ( SET, CUR, END )");
     return 0;
  }
  try
  {
    return (node->fsobj->vseek(fd, offset, whence));
  }
  catch (vfsError e)
  {
    throw vfsError("VFile::seek(dff_ui64, whence) throw\n" + e.error);
  }
}

long long  VFile::seek(int offset, int whence)
{
  if (whence > 2)
  {
     throw vfsError("VFile::vseek(offset, whence) error whence not defined ( SET, CUR, END )");
     return 0;
  }
  try
  {
    return (node->fsobj->vseek(fd, (long long)offset, whence));
  }
  catch (vfsError e)
  {
    throw vfsError("Vfile::seek(int offset, int whence) throw\n" + e.error);
  }
 
}

int  VFile::fileno()
{
  return (fd);
}

dff_ui64 VFile::tell()
{  
  try
  {
    return (node->fsobj->vseek(fd, 0, 1));
  }
  catch (vfsError e)
  {
    throw vfsError("VFile::tell() throw\n" + e.error);
  }
}
