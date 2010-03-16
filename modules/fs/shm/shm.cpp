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
 *  Solal Jacob <sja@digital-forensic.org>
 */

#include "shm.hpp"

shm::shm()
{
  name = "shm";
  fdm = new fdmanager;
  fdm->InitFDM();
  res = new results(name);
}

void shm::start(argument* arg)
{
  Node* parent;
  string filename;

  arg->get("parent", &parent);
  arg->get("filename", &filename);

  addnode(parent, filename);
  string n = "file " + filename + " created\n";
  res->add_const("result", n);
 //res->add_const("node", file);

  return ;
}

Node* shm::addnode(Node* parent, string filename)
{
  attrib *attr = new attrib;
  attr->size = 0;

  fileInfo* fi = new fileInfo;
  handleList.push_back(fi);
  attr->handle = new Handle(handleList.size() - 1);
  Node* node = CreateNodeFile(parent, filename, attr, true);
  fi->node = node;
 
  return node;
}

int shm::vopen(Handle *handle)
{
  if (handle == NULL)
     throw vfsError("shm::bad\n"); 
  fileInfo *fi = handleList[handle->id];
  if (fi != NULL)
  {
    filePos* fd = new filePos(fi); 
    int i = fdm->AllocFD(fd); 
    return (i);
  }
 return (0);
}

int shm::vread(int fd, void *buff, unsigned int size)
{
  filePos* fp = fdm->GetFDInfo(fd);
  fileInfo* fi = fp->fi;

  if (!fi->buff)
    return (0);

  if ((int)(fi->size - fp->current) <= 0)
    return (0);
  if (size >  fi->size - fp->current)
    size = fi->size - fp->current;
  memcpy(buff,(char *)fi->buff + fp->current, size);
  fp->current += size;
  return (size);
}

int shm::vwrite(int fd, void *buff, unsigned int size) 
{
  filePos* fp = fdm->GetFDInfo(fd);
  fileInfo* fi = fp->fi;

  if (!fi->size) 
  {
     fi->buff = new char[size];
     fi->size = size;
  }				
  else if (fp->current + size > fi->size) 
  {
    size = fp->current + size - fi->size;
    fi->buff = realloc(fi->buff, sizeof(char) * (fi->size + size));
    fi->size += size;
  }
  memcpy((char*)fi->buff + fp->current, buff, size);
  fp->current += size;
  fi->node->attr->size = fi->size; 

  return (size); 
}

dff_ui64 shm::vseek(int fd, dff_ui64 offset, int whence)
{
  filePos* fp = fdm->GetFDInfo(fd);
  fileInfo* fi = fp->fi;
 
  if (whence == 0)
    fp->current = offset;
  else if (whence == 1)
    fp->current += offset;
  else if (whence == 2)
    fp->current = fi->size + offset;
  return (fp->current);
}

int shm::vclose(int fd)
{
//XXX del fp
  fdm->ClearFD(fd);

  return (0); 
}

unsigned int shm::status(void)
{
  return (0);
}
