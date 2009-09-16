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

#include "argument.hpp"

argument::argument()
{

}

argument::argument(string who)
{
  from = who;
  km = env::Get();
}

void argument::add_int(string name, int v)
{
  v_val *v_v;

  v_v = new v_val_int(from, name, v);
  val_m[name] = v_v;
  km->add_var_val(v_v);
}

void argument::add_string(string name, string v)
{
  v_val *v_v;

  v_v = new v_val_string(from, name, v);
  val_m[name] = v_v;
  km->add_var_val(v_v);
}

void argument::add_bool(string name, bool v)
{
  v_val *v_v;

  v_v = new v_val_bool(from, name, v);
  val_m[name] = v_v;
  km->add_var_val(v_v);
}

void argument::add_node(string name, Node* n)
{
  v_val* v;

  v = new v_val_node(from, name, n);
  val_m[name] = v;
  km->add_var_val(v);
}

void argument::add_path(string name, Path* n)
{
  v_val* v;

  v = new v_val_path(from, name, n);
  val_m[name] = v;
  km->add_var_val(v);
}

/* //merde avec python ?
void argument::add(v_val *v)
{
  val[v->name] = v;
  vars_db[v->name].add_var_val(v);
}
*/
void argument::get(string name, int* v)
{
  v_val_int *t;

  t = (v_val_int *)val_m[name];
  if (!t)
    throw envError("argument " + name + " doesn't exist");
  else  
    *v = t->value;
}

void argument::get(string name, string* v)
{
  v_val_string *t;

  t = (v_val_string *)val_m[name];
  if (!t)
   throw envError("argument " + name + " doesn't exist");
  else 
   *v = t->value;
}

void argument::get(string name, bool* v)
{
  v_val_bool *t;

  t = (v_val_bool *)val_m[name];
  if (!t)
   throw envError("argument " + name + " doesn't exist");
  else 
   *v = t->value;
   
}

void argument::get(string name, Node** v)
{
  v_val_node* t;

  t = (v_val_node*)val_m[name];
  if (!t)
   throw envError("argument " + name + " doesn't exist"); 
  else
  {
   if (!t->value)
   {
	 throw envError("argument " + name + " value not set");
   }
   *v = t->value;
  }
}


void argument::get(string name, Path** v)
{
  v_val_path* t;

  t = (v_val_path*)val_m[name];
  if (!t)
   throw envError("argument " + name + " doesn't exist"); 
  else
  {
    if (!t->value)
      throw envError("argument " + name + " value not set");
    *v = t->value;
  }
}

int argument::get_int(string name)
{
  v_val_int *t;

  t = (v_val_int *)val_m[name];
  if (!t)
    throw envError("argument " + name + " doesn't exist");
  else  
    return t->value;
}

string argument::get_string(string name)
{
  v_val_string *t;

  t = (v_val_string *)val_m[name];
  if (!t)
   throw envError("argument " + name + " doesn't exist");
  else 
   return t->value;
}

bool argument::get_bool(string name)
{
  v_val_bool *t;

  t = (v_val_bool *)val_m[name];
  if (!t)
   throw envError("argument " + name + " doesn't exist");
  else 
   return t->value;
}

Node* argument::get_node(string name)
{
  v_val_node* t;

  t = (v_val_node*)val_m[name];
  if (!t)
   throw envError("argument " + name + " doesn't exist"); 
  else
  {
   if (!t->value)
   {
	 throw envError("argument " + name + " value not set");
   }
   return t->value;
  }
}

Path* argument::get_path(string name)
{
  v_val_path* t;

  t = (v_val_path*)val_m[name];
  if (!t)
   throw envError("argument " + name + " doesn't exist"); 
  else
  {
   if (!t->value)
   {
	 throw envError("argument " + name + " value not set");
   }
   return  t->value;
  }
}
