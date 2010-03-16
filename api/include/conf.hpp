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

class config
{
  class env* 	km;		
  public:
  string 	from;

  EXPORT 		config(string from);

  list<class v_descr *> descr_l;
  list<class v_val *>	val_l; 
  string		description; 
//c+++ interface 
  EXPORT void 		add(string name, string type, bool opt = false, string descr = "");
  EXPORT void 		add(string name, string type, int min, int max, bool opt = false, string descr = "");
  EXPORT void 		add_const(string name, string val); 
  EXPORT void 		add_const(string name, bool val); 
  EXPORT void 		add_const(string name, int val); 
  EXPORT void 		add_const(string name, Node* val); 
  EXPORT void 		add_const(string name, Path* val); 
  EXPORT void 		add_const(string name, list<Node *>* val); 
};

#endif
