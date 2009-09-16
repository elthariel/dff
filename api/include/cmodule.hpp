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

#ifndef __DRIVER_HPP__
#define __DRIVER_HPP__

#include <list>
#include <string>
#include "export.hpp"
#include "exceptions.hpp"
#include "vfs.hpp"
#include "conf.hpp"
#include "results.hpp"
#include "loader.hpp"

using namespace std;

typedef fso*  create_t(void);
//recup ds le fso

/**
 * @file   cmodule.hpp
 * @author  <sja@digital-forensic.org>
 * @date   Mon Aug 17 18:03:29 2009
 * 
 * @brief  From this class derivate DFF modules wrote in CPP 
 * 
 * 
 */
class CModule	
{
public:
  /** 
   * 
   * 
   */
  CModule() { };

  /** 
   * 
   * 
   * @param drvname name of the module
   * @param cr C proxy to create the module and permit to import it 
   * 
   * @return 
   */
  EXPORT			CModule(string drvname, create_t cr);

  /** 
   * 
   * 
   * 
   * @return 
   */
  EXPORT			~CModule() { };
  create_t*			fcreate; /**<  */
  config* 			conf; /**<  */
  string			tags; /**<  */
  list<string>			flags; /**<  */
  string			name; /**<  */
  void*				handle;	/**<  */

  /** 
   * 
   * 
   * 
   * @return 
   */
  EXPORT fso*			getfso(void);
};

#endif
