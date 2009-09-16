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

#include "results.hpp"

results::results(string who)
{
    from = who;
    km = env::Get();
}

void results::add_const(string name, string v)
{
  v_val *v_v;
  
  v_v = new v_val_string(from, name, v);
  val_m[name] = v_v;
  km->add_var_val(v_v); 
}

void results::add_const(string name, int v)
{
   v_val *v_v;
  
  v_v = new v_val_int(from, name, v);
  val_m[name] = v_v;
  km->add_var_val(v_v); 
}

void results::add_const(string name, Node* v)
{
   v_val *v_v;
  
  v_v = new v_val_node(from, name, v);
  val_m[name] = v_v;
  km->add_var_val(v_v); 
}

void results::add_const(string name, Path* v)
{
   v_val *v_v;
  
  v_v = new v_val_path(from, name, v);
  val_m[name] = v_v;
  km->add_var_val(v_v); 
}
