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

#include "local.hpp"
#include <String>
#include <windows.h>
#include <shlwapi.h>

void local::frec(char *name, Node *rfv)
{
  HANDLE hd;
  WIN32_FIND_DATAA  find;
  string  	  		nname;

  string searchPath = name;
  searchPath +=  "\\*";  
  
  if((hd = FindFirstFileA(searchPath.c_str(), &find)) != INVALID_HANDLE_VALUE)
    {
      do
	{
	  Node* tmp; //= new Node;
	  
	  if (!strcmp(find.cFileName, ".")  || !strcmp(find.cFileName, ".."))
	    continue ;
	  nname = name;
	  nname += "\\";
	  nname += find.cFileName;
	  string handle;
	  handle += nname; 
	  attrib*   attr = new w_attrib(find);
	  if (find.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY)
	    {
	      tmp = CreateNodeDir(rfv, find.cFileName, attr);
	      frec((char *)nname.c_str(), tmp);
	    }
	  else
	    { 
	      attr->handle = new Handle(handle);
	      tmp = CreateNodeFile(rfv, find.cFileName, attr);
	    }
	}  while(FindNextFileA(hd, &find));
      
      FindClose(hd);
    }
}

local::local()
{
  res = new results("local");
  this->name = "local";
}

void local::start(argument *arg)
{
  attrib*	attr;
  string 	path;
  Path		*lpath;
  Node*		root;
  Node*		parent;
  WIN32_FILE_ATTRIBUTE_DATA info;

  try
  {	 
    arg->get("parent", &parent);
  }
  catch (envError e)
  {
    parent = VFS::Get().GetNode("/");
  }
  try 
  {
    arg->get("path", &lpath);
  } 
  catch (envError e)
  {
     res->add_const("error", "conf " + e.error);
     return ;
  }
  if ((lpath->path.rfind('/') + 1) == lpath->path.length())
    lpath->path.resize(lpath->path.rfind('/'));
  if ((lpath->path.rfind('\\') + 1) == lpath->path.length())
    lpath->path.resize(lpath->path.rfind('\\'));
  path = lpath->path;
  if (path.rfind("\\") <= path.size())
    path = path.substr(path.rfind("\\") + 1);
  else 
    path = path.substr(path.rfind("/") + 1);

  if(!GetFileAttributesExA(lpath->path.c_str(), GetFileExInfoStandard, &info))
  {
	  res->add_const("error", string("error stating file:" + path)); 
      return ;
  }
  attr = new w_attrib(info);	
  if (info.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY)
  {
    root = CreateNodeDir(parent, path, attr);
    frec((char *)(lpath->path.c_str()), root);
  }
  else 
  {
    string handle;
    handle += lpath->path.c_str();
    attr->handle = new Handle(handle);
    root = CreateNodeFile(parent, path, attr);
  }
  res->add_const("result", std::string("no problem")); 
  res->add_const("root", root);

 return ;
}

int local::vopen(Handle* handle)
{
  if (handle != NULL)
    return ((int)CreateFileA(handle->name.c_str(), GENERIC_READ, FILE_SHARE_READ,
			     0, OPEN_EXISTING,FILE_ATTRIBUTE_NORMAL, 0));
  else
    return -1;
}

int local::vread(int fd, void *buff, unsigned int size)
{
  DWORD readed;
  
  if (ReadFile((HANDLE)fd, buff, size,  &readed ,0))
    return (readed);
  else
    return (0);
}

int local::vclose(int fd)
{
  return (!CloseHandle((HANDLE)fd));
}

dff_ui64 local::vseek(int fd, dff_ui64 offset, int whence)
{
  if (whence == 0)
    whence = FILE_BEGIN;
  else if (whence == 1)
    whence = FILE_CURRENT;
  else if (whence == 2)
    whence = FILE_END;
  return (SetFilePointer((HANDLE)fd, offset, 0, whence)); 
}

unsigned int local::status(void)
{
//status called

  return (nfd);
}

//XXX


//extern "C" 
//{
//  fso* create(void)
//  {
//    return (new local(string("local")));
//  }
//    
//  void destroy(fso *p)
//  {
//    delete p;
//  }
//
//  class proxy 
//  {
//    public :
//    proxy()
//    {
//     CModule* mod = new CModule("local", create);
//     mod->conf->add("path", "path");
//     mod->conf->add("parent", "node");
//     mod->conf->add_const("mime-type", std::string("data"));
//	 mod->tags = "fs";
//    }
//  };
//  proxy p;
//}
