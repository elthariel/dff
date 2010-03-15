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
 *  Solal J. <sja@digital-forensic.org>
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
#include "type.hpp"
#include <string.h>

class argument
{
  class env* km;
  string from;	
 public:
   map<string, class v_val * > val_m; 

  EXPORT argument(string who);
  EXPORT argument();

//add_type

  EXPORT void 	add_int(string, int);
  EXPORT void 	add_string(string, string);
  EXPORT void 	add_bool(string, bool);
  EXPORT void 	add_node(string, Node*);
//  EXPORT void 	add_path(string, Path*);
  EXPORT void   add_path(string, string);
  EXPORT void	add_lnode(string, list<Node *> *);


//get( type)

  EXPORT void 	get(string name, int *v);
  EXPORT void 	get(string name, bool *v);
  EXPORT void 	get(string name, Node **v);
  EXPORT void 	get(string name, string *v);
  EXPORT void 	get(string name, Path **v);
  EXPORT void   get(string name, list<Node *> **v);
//

//get_type

  EXPORT int 		get_int(string name);
  EXPORT bool 		get_bool(string name);
  EXPORT string 	get_string(string name);
  EXPORT Node*  	get_node(string name);
  EXPORT Path*  	get_path(string name);
  EXPORT list<Node *>*	get_lnode(string name);
};
#endif
