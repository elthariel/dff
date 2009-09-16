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

#ifndef __EXCEPTIONS_HH__
#define __EXCEPTIONS_HH__

#include <string>
#include "export.hpp"

using namespace std;

/**
 * @file   exceptions.hpp
 * @author  <sja@digital-forensic.org>
 * @date   Mon Aug 17 17:55:55 2009
 * 
 * @brief  This class is raised when an exception occur in the environnement
 * 
 * 
 */
class envError
{
public:
  string error;			/**<  */

  /** 
   * 
   * 
   * @param msg 
   * 
   * @return 
   */
  EXPORT envError(string msg);
};


/**
 * @file   exceptions.hpp
 * @author  <jacob.solal@arxsys.fr>
 * @date   Mon Aug 17 17:56:00 2009
 * 
 * @brief  This class is raised when an exception occur in the vfs
 * 
 * 
 */
class vfsError
{
public:
  string error;			/**<  */

  /** 
   * 
   * 
   * @param msg 
   * 
   * @return 
   */
  EXPORT vfsError(string msg);
};


#endif 
