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

#include "extract.hpp"
#include <fcntl.h>
#include <dirent.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <errno.h>

void extract::start(argument* arg)
{
  string	path;
  Node*		parent;
  VFile*	file;
  void*		buff;
  int		n;
  int		fd;  

  arg->get("parent", &parent);
  arg->get("path", &path);
  file = parent->open();
  if ((fd = open(path.c_str(), O_RDWR | O_CREAT | O_TRUNC , 0666)) > 0)
  {
     buff = malloc(4096);
     try 
     {
       while ((n = file->read(buff, 4096)) > 0)
       {
         write(fd, buff, n);           
       } 
     }
     catch (vfsError e)
     {
       res->add_const("error", std::string(e.error));
       return ;
     } 
     file->close();
     close(fd);  
     res->add_const("result", std::string("no problem")); 
     return ;
  }
  res->add_const("result", std::string("Can't open path")); 
  return ;
}

unsigned int	extract::status(void)
{
  return (0);
}

extern "C" 
{
  fso* create(void)
  {
    return (new extract("extract"));
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
     CModule* cmod = new CModule("Cextract", create);
     cmod->conf->add("path", "string");
     cmod->conf->add( "parent", "node");
     cmod->conf->add_const("mime-type", std::string("data")); 
     cmod->tags = "process";
    }
  };
  proxy p;
}

