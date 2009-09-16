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

#ifndef __CONF_HPP__
#define __CONF_HPP__

#include <string>
#include <list>
#include <map>
#include <iostream>
#include "env.hpp"
#include "vars.hpp"
#include "export.hpp"
#include <string.h>

using namespace std;

/**
 * @file   conf.hpp
 * @author  <sja@digital-forensic.org>
 * @date   Mon Aug 17 17:46:41 2009
 * 
 * @brief This class permit to descrive the argument need by a module 
 * 
 * 
 */


class config
{
  class env* 	km;		/**<  */
  string 		from;	/**<  */
  public:

  /** 
   * 
   * 
   * @param from wich module come the config
   * 
   * @return 
   */
  EXPORT 		config(string from);

  list<class v_descr *> descr_l;//  } list<class vars> v_l + cast /**<  */
  list<class v_val *>	val_l; //   } /**<  */
  string		description; /**<  */
//c+++ interface 
/** 
 * 
 * 
 * @param name of the argument
 * @param type of the argument
 * @param opt is argument optional
 * @param descr, description of the argument
 */
  EXPORT void 		add(string name, string type, bool opt = false, string descr = "");

  /** 
   * 
   * 
   * @param name of the argument 
   * @param type of the arugment 
   * @param min, minimal value of the integer
   * @param max, maximal value of the interger
   * @param opt, is argument optional
   * @param descr, description of the argument
   */
  EXPORT void 		add(string name, string type, int min, int max, bool opt = false, string descr = "");

  /** 
   * 
   * 
   * @param name of the argument 
   * @param val, add constant as string
   */
  EXPORT void 		add_const(string name, string val); //def define ? 

  /** 
   * 
   * 
   * @param name of the argument  
   * @param val, add a constant as bool
   */
  EXPORT void 		add_const(string name, bool val); //def define ? 

  /** 
   * 
   * 
   * @param name  of the argument 
   * @param val, add a constant as int
   */
  EXPORT void 		add_const(string name, int val); //def define ? 

  /** 
   * 
   * 
   * @param name  of the argument 
   * @param val, add a constant as Node 
   */
  EXPORT void 		add_const(string name, Node* val); //def define ? 

  /** 
   * 
   * 
   * @param name  of the argument 
   * @param val, add a constant as Path 
   */
  EXPORT void 		add_const(string name, Path* val); //def define ? 
//void add_info info 
// void add_from -> fso::helper -> modname
//XXX
};

#endif
