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

%module(package="api.env") libenv

%include "std_string.i" 
%include "std_list.i" 
%include "std_map.i"
%import  "../exceptions/libexceptions.i"

%catches(envError) argument::get_int(string name);
%catches(envError) argument::get_string(string name);
%catches(envError) argument::get_bool(string name);
%catches(envError) argument::get_node(string name);
%catches(envError) argument::get_path(string name);
%catches(envError) v_val::get_int(void);
%catches(envError) v_val::get_string(void);
%catches(envError) v_val::get_bool(void);
%catches(envError) v_val::get_node(void);
%catches(envError) v_val::get_path(void);

%{
#include "../include/export.hpp"
#include "../include/env.hpp"
#include "../include/vars.hpp"
#include "../include/conf.hpp"
#include "../include/argument.hpp"
#include "../include/results.hpp"
%}
%include "../include/export.hpp"
%include "../include/env.hpp"
%include "../include/vars.hpp"
%include "../include/conf.hpp"
%include "../include/argument.hpp"
%include "../include/results.hpp"



%traits_swigtype(v_key);
%fragment(SWIG_Traits_frag(v_key));
%traits_swigtype(v_val);
%fragment(SWIG_Traits_frag(v_val));
namespace std
{
%template(ListDescr)    list<v_descr*>;
%template(MapVal)       map<string, v_val* >;
%template(ListVal)      list<v_val*>;
%template(MapKey)       map< string, v_key* >;
};
