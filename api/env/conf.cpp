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
 *  Frederic B. <fba@digital-forensic.org>
 *
 */

#include  "conf.hpp"

config::config(string who)
{
  km = env::Get();
  from = who;
}

void	config::add(string name, string type, bool opt, string descr)
{
  v_descr *v;
  
  if (!strcmp(type.c_str(), "int"))
    v = new v_descr_int(from, name, opt, descr);
  else if (!strcmp(type.c_str(), "string"))
    v = new v_descr_string(from, name, opt, descr);
  else if (!strcmp(type.c_str(), "node"))
    v = new v_descr_node(from, name, opt, descr);
  else if (!strcmp(type.c_str(), "path"))
    v = new v_descr_path(from, name, opt, descr);
  else if (!strcmp(type.c_str(), "bool"))
    v = new v_descr_bool(from, name, opt, descr);
  else
  {
    cout << "Can't find type" << endl;
    return ;
  }
  descr_l.push_back(v);
  km->add_var_descr(v);
}

void 	config::add(string name, string type, int min, int max, bool opt, string descr)
{
  v_descr *v;

  if (!strcmp(type.c_str(), "int"))
    v = new v_descr_int(from, name, min, max, opt, descr);
  else if (!strcmp(type.c_str(), "string")) //min max == size min/max
    v = new v_descr_string(from, name, opt, descr);
  else
  {
    cout << "Can't find type" << endl;
    return ;
  }
  descr_l.push_back(v);
  km->add_var_descr(v);
}


void config::add_const(string name, string val)
{
   v_val *v;
  
  v = new v_val_string(from, name, val);
  val_l.push_back(v);
  km->add_var_val(v); 
}

void config::add_const(string name, int val)
{
   v_val *v;
  
  v = new v_val_int(from, name, val);
  val_l.push_back(v);
  km->add_var_val(v); 
}

void config::add_const(string name, bool val)
{
   v_val *v;
  
  v = new v_val_bool(from, name, val);
  val_l.push_back(v);
  km->add_var_val(v); 
}

void config::add_const(string name, Node* val)
{
   v_val *v;
  
  v = new v_val_node(from, name, val);
  val_l.push_back(v);
  km->add_var_val(v); 
}

void config::add_const(string name, Path* val)
{
   v_val *v;
  
  v = new v_val_path(from, name, val);
  val_l.push_back(v);
  km->add_var_val(v); 
}
