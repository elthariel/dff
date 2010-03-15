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

#include "env.hpp"

void env::add_var_descr(v_descr *v)
{
  mapdb_t::iterator i = vars_db.find(v->name);
  if (i == vars_db.end())
    vars_db[v->name] = new v_key();
  vars_db[v->name]->add_var_descr(v);  
}

void env::add_var_val(v_val *v)
{
  mapdb_t::iterator i = vars_db.find(v->name);
  if (i == vars_db.end())
    vars_db[v->name] = new v_key();
  vars_db[v->name]->add_var_val(v);
}

v_key::v_key(void)
{
}

v_key::~v_key(void)
{
}

void v_key::add_var_descr(v_descr *v)
{ 
  descr_l.push_back(v);
}
void v_key::add_var_val(v_val *v)
{
  val_l.push_back(v);
}
