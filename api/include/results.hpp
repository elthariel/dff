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


class results : public argument
{
  env* km;			
 public:
  string	from;		

  EXPORT 	results(string who);
  EXPORT void	add_const(string name, string val);
  EXPORT void 	add_const(string name, int val);
  EXPORT void 	add_const(string name, Node* val);
  EXPORT void 	add_const(string name, Path* val);
  EXPORT void 	add_const(string name, list<Node *>* val);
};

#endif
