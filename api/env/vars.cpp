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
 *  Frederic B. <fba@digital-forensic.org>
 */

#include "vars.hpp"

/* v_descr */

v_descr_int::v_descr_int(string f, string n, bool opt, string descr)
{
  name = n; 
  from = f;
  type = "int";
  optional = opt;
  description = descr;
}

v_descr_int::v_descr_int(string f, string n, int x, int y, bool opt, string descr) 
{
  from = f;
  name = n;
  min = x;
  max = y;
  type = "int";
  optional = opt;
  description = descr;
}

v_descr_string::v_descr_string(string f, string n, bool opt, string descr)
{
  from = f;
  name = n;
  type = "string";
  optional = opt;
  description = descr;
}

v_descr_bool::v_descr_bool(string f, string n, bool opt, string descr)
{
  from = f;
  name = n;
  type = "bool";
  optional = opt;
  description = descr;
}

v_descr_node::v_descr_node(string f, string n, bool opt, string descr)
{
  from = f;
  name = n;
  type = "node";
  optional = opt;
  description = descr;
}

v_descr_path::v_descr_path(string f, string n, bool opt, string descr)
{
  from = f;
  name = n;
  type = "path";
  optional = opt;
  description = descr;
}

int  v_descr_int::check_val(int v)
{
  if (min != 0 && max != 0)
    if (v < min || v > max)
       return (0);
  return (1);
}

v_descr_lnode::v_descr_lnode(string f, string n, bool opt, string descr)
{
  from = f;
  name = n;
  type = "lnode";
  optional = opt;
  description = descr;
}

/* v_val get*/

int v_val::get_int(void)
{
  return (((v_val_int *)this)->value);
}

bool v_val::get_bool(void)
{
  return (((v_val_bool *)this)->value);
}

string v_val::get_string(void)
{
  return (((v_val_string *)this)->value);
}

Node* v_val::get_node(void)
{
  return (((v_val_node *)this)->value);
}

Path* v_val::get_path(void)
{
  return (((v_val_path *)this)->value);
}

list<Node* >* v_val::get_lnode(void)
{
  return (((v_val_lnode *)this)->value);
} 

/* v_val_type */

v_val_int::v_val_int(string f,string n, int v)
{
  from = f;
  name = n;
  value = v;
  type = "int";
}

v_val_bool::v_val_bool(string f,string n, bool v)
{
  from = f;
  name = n;
  value = v;
  type = "bool";
}

v_val_string::v_val_string(string f, string n, string v)
{
  from = f;
  name = n;
  value = v;
  type = "string";
}

v_val_node::v_val_node(string f, string n, Node *v)
{
  from = f;
  name = n;
  value = v;
  type = "node";
}

v_val_path::v_val_path(string f, string n, Path *v)
{
  from = f;
  name = n;
  value = v;
  type = "path";
}

v_val_lnode::v_val_lnode(string f, string n, list<Node* >* v)
{
  from = f;
  name = n;
  value = v;
  type = "lnode";
}
