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

#include "local.hpp"
#include <fcntl.h>
#include <dirent.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <errno.h>
#include <sys/time.h>


void local::iterdir(Node* dir)
{
    struct stat		stbuff; 
    struct dirent*	dp;
    DIR*		dfd;
    list<Node* >	ldir;

    unsigned long long total = 0;
    ldir.push_back(dir);
    while (!ldir.empty()) 
    {
      Node* cnode = ldir.front();
      ldir.pop_front();

      string cpath = cnode->attr->handle->name; 

      if ((dfd = opendir(cpath.c_str())))
      {
        while ((dp = readdir(dfd)))
        {
          Node*		tmp; 
  	  u_attrib*   	attr;

          if (!strcmp(dp->d_name, ".")  || !strcmp(dp->d_name, ".."))
	     continue; 
          string upath =  string(cpath + string("/") + string(dp->d_name));
          if (lstat(upath.c_str(), &stbuff) != -1)
          {
            attr = new u_attrib(&stbuff);
 	    attr->handle = new Handle(upath);
            if (((stbuff.st_mode & S_IFMT) == S_IFDIR ))
            {
	      tmp = CreateNodeDir(cnode, dp->d_name, attr);
	      ldir.push_back(tmp);
              total++;
            }
            else
            {
	      tmp = CreateNodeFile(cnode, dp->d_name, attr);
              total++;
            }
          }
        }
        closedir(dfd);
      }
    }
    res->add_const("nodes created", total);
}
void local::start(argument* ar)
{
  u_attrib*	attr;
  string 	path;
  Path		*tpath;
  struct stat 	stbuff;
  Node*		root;
  Node*		parent;
  arg = ar; 

  nfd = 0;
  try 
  { 
    arg->get("parent", &parent);
    arg->get("path", &tpath);
  }
  catch (envError e)
  {
    res->add_const("error", "conf " + e.error);
    return ;
  }
  if ((tpath->path.rfind('/') + 1) == tpath->path.length())
    tpath->path.resize(tpath->path.rfind('/'));
  path = tpath->path.substr(tpath->path.rfind("/") + 1);
  if (stat(tpath->path.c_str(), &stbuff) == -1)
  {
    res->add_const("error", "stat: " + std::string(strerror(errno)));    	
    return ;
  }
  attr = new u_attrib(&stbuff);
  string handle;
  handle += tpath->path;
  attr->handle = new Handle(handle);
  if (((stbuff.st_mode & S_IFMT) == S_IFDIR ))
  {
    root = CreateNodeDir(parent, path, attr);
    iterdir(root);
  }
  else 
  {
    root = CreateNodeFile(parent, path, attr);
  }
  res->add_const("result", std::string("no problem")); 

  return ;
}

int local::vopen(Handle* handle)
{
  int n;
  struct stat 	stbuff;

  if ((n = open((handle->name).c_str(), O_RDONLY | O_LARGEFILE)) == -1)
    throw vfsError("local::open error can't open file");
  if (stat((handle->name).c_str(), &stbuff) == -1)
    throw vfsError("local::open error can't stat");
  if (((stbuff.st_mode & S_IFMT) == S_IFDIR ))
    throw vfsError("local::open error can't open directory");
  nfd++;
  return (n);
}

int local::vread(int fd, void *buff, unsigned int size)
{
  int n;
  
  n = read(fd, buff, size);
  if (n < 0)
  {
    throw vfsError("local::vread error read = -1");
  }
  return n;
}

int local::vclose(int fd)
{
  if (close(fd) == -1)
  {
    throw vfsError("local::close error can't close");
  }
  nfd--;
  return (0);
}

dff_ui64 local::vseek(int fd, dff_ui64 offset, int whence)
{
 dff_ui64  n = 0;
 
  if (whence == 0)
    whence = SEEK_SET;
  else if (whence == 1)
    whence = SEEK_CUR;
  else if (whence == 2)
    whence = SEEK_END;
 n = lseek64(fd, offset, whence);
 if (n == -1)
 {
   throw vfsError("local::vseek can't seek error " + string(strerror(errno)));
 }
 return (n);
}

unsigned int local::status(void)
{
  return (nfd);
}

extern "C" 
{
  fso* create(void)
  {
    return (new local(string("local")));
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
     CModule* cmod = new CModule("local", create);
     cmod->conf->add("path", "path");
     cmod->conf->add("parent", "node");
     cmod->conf->add_const("mime-type", std::string("data"));
     cmod->tags = "fs";
    }
  };
  proxy p;
}
