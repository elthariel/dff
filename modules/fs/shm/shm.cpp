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

#include "shm.hpp"

void shm::start(argument* arg)
{
  Node* parent;
  string filename;
  arg->get("parent", &parent);
  arg->get("filename", &filename);
  data* ndata = new data;
  ndata->size = 0;
  blist.push_back(ndata);
  int nhandle;
  nhandle = blist.size();
  
  attrib *attr = new attrib;
  attr->size = 0;
  attr->handle = new Handle(nhandle);
  Node* file = CreateNodeFile(parent, filename, attr);
  string n = "file " + filename + " created\n";
  res->add_const("result", n);
  return ;
}

int shm::vopen(Handle *handle)
{
  odata *data = new odata;
  data->offset = 0;
  data->handle = handle->id; 
  olist.push_back(data);
  return (olist.size());
}

int shm::vread(int fd, void *buff, unsigned int size)
{
  odata *od = olist[fd - 1]; 
  data *ndata = blist[od->handle - 1];
  if (!ndata->buff)
  {
    return (0);
  }

  if ((int)(ndata->size - od->offset) <= 0)
    return (0);
  if (size >  ndata->size - od->offset)
    size = ndata->size - od->offset;
  memcpy(buff,(char *)ndata->buff + od->offset, size);
  od->offset += size;
  return (size);
  
}

int shm::vwrite(int fd, void *buff, unsigned int size) 
{
  odata *od = olist[fd - 1];
  data *ndata = blist[od->handle - 1];

  if (!ndata->size)  
     ndata->buff = new char[size];
  else if (od->offset + size > ndata->size)
    ndata->buff = realloc(ndata->buff, sizeof(char) * (ndata->size + size));
  ndata->size += size;
  memcpy((char*)ndata->buff + od->offset, buff, size);
  od->offset += size; 
 
  return (size); 
}

dff_ui64 shm::vseek(int fd, dff_ui64 offset, int whence)
{
  odata *od = olist[fd - 1];
  data *ndata = blist[od->handle - 1];  

  if (whence == 0)
    od->offset = offset;
  else if (whence == 1)
    od->offset += offset;
  else if (whence == 2)
    od->offset = ndata->size + offset;
  return (od->offset);
}

int shm::vclose(int fd)
{
  return (0); 
}

unsigned int shm::status(void)
{
  return (0);
}

extern "C" 
{
  void destroy(fso* p)
  {
    delete p;
  }

  fso*  create(void)
  {
    return ( new shm("shm"));
  }

  class proxy
  {
    public:
    proxy()
    {
      CModule* cmod = new CModule("shm", create);
      cmod->conf->add("filename", "string");
      cmod->conf->add("parent", "node");
      cmod->tags = "fs";
    }
  };
  proxy p;
}
