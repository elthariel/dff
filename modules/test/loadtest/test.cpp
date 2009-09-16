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

#include "test.hpp"
#include <fcntl.h>
#include <dirent.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <errno.h>
#include <sys/time.h>

void test::start(argument* arg)
{
  attrib*	attr;
  Node* 	parent;  

  try 
  { 
    arg->get("parent", &parent);
  }
  catch (envError e)
  {
    res->add_const("error", "conf " + e.error);
    return ;
  }

  for (int i = 0;  i < 3000000; i++)
  {
    attr = new attrib();
    string handle = "test";
    attr->handle = new Handle(handle);
    string name;
    char cname[1024];
    char percent[1024];
    sprintf(cname, "file_%d", i);
    name = cname;
    if (!(i%30000))
    {
      sprintf(percent, "(%d %)", (i /30000));
      stateinfo = string(percent) + "  creating node: " + cname + "\n";
    }  	
    CreateNodeFile(parent, name, attr);
  }
  res->add_const("result", std::string("no problem"));
//  cout << "loadtest finish" << endl; 
//  res->add_const("root", root);

  return ;
}

int test::vopen(Handle* handle)
{
  int n;
   
  return 0;
}

int test::vread(int fd, void *buff, unsigned int size)
{
  int n;
  
  return 0;
}

int test::vclose(int fd)
{
  return (0);
}

dff_ui64 test::vseek(int fd, dff_ui64 offset, int whence)
{
 return (-1);
}

unsigned int test::status(void)
{
//status called

  return (0);
}

extern "C" 
{
  fso* create(void)
  {
    return (new test(string("test")));
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
     CModule* cmod = new CModule("testload", create);
     cmod->conf->add("parent", "node");
     cmod->tags = "test";
    }
  };
  proxy p;
}
