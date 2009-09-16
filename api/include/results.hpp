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

#ifndef __RESULTS_HPP__
#define __RESULTS_HPP__

#include <string>
#include <list>
#include <map>
#include <iostream>
#include "env.hpp"
#include "argument.hpp"
#include "vars.hpp"
#include "type.hpp"
#include "export.hpp"
#include <string.h>


/**
 * @file   results.hpp
 * @author  <sja@digital-forensic.org>
 * @date   Mon Aug 17 17:59:21 2009
 * 
 * @brief  This class permit to return the results of modules
 * 
 * 
 */
class results : public argument
{
  env* km;			/**<  */
 public:
  string	from;		/**<  */

  /** 
   * 
   * 
   * @param who, from who come the result
   * 
   * @return 
   */
  EXPORT 	results(string who);

/** 
 * 
 * 
 * @param name, name of the constant 
 * @param val, value of the constant as string 
 */
  EXPORT void	add_const(string name, string val);

  /** 
   * 
   * 
   * @param name of the constant 
   * @param val, value of the constant as int
   */
  EXPORT void 	add_const(string name, int val);

  /** 
   * 
   * 
   * @param name of the constant
   * @param val, value of the constant as Node 
   */
  EXPORT void 	add_const(string name, Node* val);

  /** 
   * 
   * 
   * @param name of the constant  
   * @param val, value of the constant as Path 
   */
  EXPORT void 	add_const(string name, Path* val);
};

#endif
