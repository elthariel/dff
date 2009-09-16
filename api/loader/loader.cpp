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

#include "loader.hpp"

 
LoaderError::LoaderError(string emsg)
{
     error = emsg;
}

string *LoaderError::GetError(void)
{
  return (&error);
}

Loader*   Loader::Get()
{ 
  static Loader single; 
  return &single; 
}
 
#ifdef WIN32

int Loader::LoadCModule(string path)
{
  HMODULE handle;

  if (!(handle = LoadLibrary(path.c_str())))
  {
	  string err = "Loadlibrary error";
	  throw LoaderError(err);
  }
  return (1);
}
#else
int Loader::LoadCModule(string path)
{
  void* handle;

  if (!(handle = dlopen(path.c_str(), RTLD_NOW)))
    {
      string err = "dlopen error: ";
      err += dlerror();
      throw LoaderError(err);
    }
  dlerror();
  return (1);
}
#endif
