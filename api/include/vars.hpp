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

#ifndef __VARS_HPP__
#define __VARS_HPP__

#include "export.hpp"
#include "type.hpp"
#include <string>
#include <iostream>
#include <list>

using namespace std;
class vars
{
public:
 string name;		
 string description;
 string type;		
 string from;	
 bool	optional;	
};


/* v_descr */

class v_descr : public vars
{
};


class v_descr_int : public v_descr
{
public:
  int max;			
  int min;
  string descr;		

  EXPORT v_descr_int(string f, string n, bool opt, string description);
  EXPORT v_descr_int(string f, string n, int x, int y, bool opt, string description);
  EXPORT int  check_val(int v);
};


class v_descr_string : public v_descr
{
public:
  EXPORT v_descr_string(string f, string n, bool opt, string description);
};


class v_descr_bool : public v_descr
{
public:
  EXPORT v_descr_bool(string f, string n, bool opt, string description);
};

class v_descr_path : public v_descr
{
public:
  EXPORT v_descr_path(string f, string n, bool opt, string description);
};

class v_descr_node : public v_descr
{
public:
  EXPORT v_descr_node(string f, string n, bool opt, string description);
};

class v_descr_lnode : public v_descr
{
public:
  EXPORT v_descr_lnode(string f, string n, bool opt, string description);

};


/* v_val */

class v_val : public vars
{
public:
 EXPORT int get_int(void);
 EXPORT string get_string(void);
 EXPORT class Node* get_node(void);
 EXPORT class Path* get_path(void);
 EXPORT bool get_bool(void);
 EXPORT list<Node *>* get_lnode(void);
};

class v_val_int : public v_val
{
public:
  int	value;		

  EXPORT v_val_int(string f, string n, int v);
};


class v_val_string : public v_val
{
public:
  string value;		
  EXPORT v_val_string(string f, string n, string v);
};


class v_val_bool : public v_val
{
public:
  bool value;		

  EXPORT v_val_bool(string f, string n, bool v);
};


class v_val_node : public v_val
{
public:
  class Node* value;	

  EXPORT v_val_node(string f, string n, Node* v);
};

class v_val_path : public v_val
{
public:
  class Path*	value;	

   EXPORT v_val_path(string f, string n, Path* v);
};

class v_val_lnode : public v_val
{
public:
  list<Node *>* value;

  EXPORT v_val_lnode(string f, string n, list<Node *>* v);
};

#endif
