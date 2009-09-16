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

#ifndef __ARGUMENT_HPP__
#define __ARGUMENT_HPP__

#include <string>
#include <list>
#include <map>
#include <iostream>
#include "env.hpp"
#include "vars.hpp"
#include "export.hpp"
#include <string.h>

/**
 * @file   argument.hpp
 * @author  <sja@digital-forensic.org>
 * @date   Mon Aug 17 17:43:44 2009
 * 
 * @brief This class permit to get and set argument of a modules 
 * 
 * 
 */
class argument
{
  class env* km;		/**<  */
  string from;			/**<  */
 public:
   map<string, class v_val * > val_m; /**<  */

  /** 
   * 
   * 
   * @param who  a string which represent from who come the argument (modules name, ui, gui, ...)
   * 
   */
  EXPORT argument(string who);

  /** 
   * 
   * 
   * 
   */
  EXPORT argument();
//c++ interface
//  void add(v_val *);down cast python ...

/** 
 * 
 * 
 * @param string name of the argument
 * @param int value of the argument 
 */
  EXPORT void 	add_int(string, int);

  /** 
   * 
   * 
   * @param string name of the argument
   * @param string value of the argument
   */
  EXPORT void 	add_string(string, string);

  /** 
   * 
   * 
   * @param string name of the argument
   * @param bool value of the argument
   */
  EXPORT void 	add_bool(string, bool);

  /** 
   * 
   * 
   * @param string name of the argument 
   * @param Node class argument
   */
  EXPORT void 	add_node(string, Node*);

  /** 
   * 
   * 
   * @param string name of the argument
   * @Path class argument 
   */
  EXPORT void 	add_path(string, Path*);

  /** 
   * 
   * 
   * @param name of the argument to get
   * @param int pointer to get value
   */
  EXPORT void 	get(string name, int *v);

  /** 
   * 
   * 
   * @param name of the argument to get
   * @param bool v, bool pointer to get the value  
   */
  EXPORT void 	get(string name, bool *v);

  /** 
   * 
   * 
   * @param name of the argument to get
   * @param Node**, Node pointer pointer to get the value 
   */
  EXPORT void 	get(string name, Node **v);

  /** 
   * 
   * 
   * @param name of the argument to get
   * @param string pointer to get the value
   */
  EXPORT void 	get(string name, string *v);

  /** 
   * 
   * 
   * @param name of the argument to get
   * @param Path pointer to get the value
   */
  EXPORT void 	get(string name, Path **v);
//virer c inteface ? passsage par map ? 

/** 
 * 
 * 
 * @param name of the argument to get
 * @return int value of the argument
 */
  EXPORT int 	get_int(string name);

  /** 
   * 
   * 
   * @param name of the argument to get
   * @return bool value of the argument
   */
  EXPORT bool 	get_bool(string name);

  /** 
   * 
   * 
   * @param name  of the argument to get
   * @return string value of the argument
   */
  EXPORT string get_string(string name);

  /** 
   * 
   * 
   * @param name of the argument to get
   * 
   * @return Node pointer to  value of the argument
   */
  EXPORT Node*  get_node(string name);

  /** 
   * 
   * 
   * @param name of the argument to get 
   * 
   * @return Path pointer to value of the argument
   */
  EXPORT Path*  get_path(string name);
};
#endif
