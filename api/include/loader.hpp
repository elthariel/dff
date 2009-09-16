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

#ifndef __LOADER_HPP__
#define __LOADER_HPP__

#include <deque>
#include <list>
#include <set>
#include <map>
#include <vector>
#include <string>
#ifndef WIN32
#include "dlfcn.h"
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <dirent.h>
#include <fcntl.h>
#endif
#include "cmodule.hpp"

using namespace std;

/**
 * @file   loader.hpp
 * @author  <sja@digital-forensic.org>
 * @date   Mon Aug 17 17:57:59 2009
 * 
 * @brief  This class is raised when a exceptions occur in the loader
 * 
 * 
 */
class LoaderError
{
public:
  string error;			/**<  */

  /** 
   * 
   * 
   * @param msg 
   */
  LoaderError(string msg);

  /** 
   * 
   * 
   * 
   * @return 
   */
  string *GetError(void);
};


/**
 * @file   loader.hpp
 * @author  <solal.jacob@arxsys.fr>
 * @date   Mon Aug 17 17:58:03 2009
 * 
 * @brief  This singleton class permit to load module
 * 
 * 
 */
class	Loader 
{
private:
  /** 
   * 
   * 
   */
  Loader() {};

  /** 
   * 
   * 
   */
  ~Loader() {};

  /** 
   * 
   * 
   * 
   * @return 
   */
  Loader& operator=(Loader&);

  /** 
   * 
   * 
   */
  Loader(const Loader&);

  map<string, void* > HandleMap; /**<  */
public:
  map<string, class CModule* > cmodules_db; /**<  */

  /** 
   * 
   * 
   * 
   * @return 
   */
  EXPORT static Loader* Get();

  /** 
   * 
   * 
   * @param pathname 
   * 
   * @return 
   */
  int	LoadCModule(string pathname);
};

#endif
