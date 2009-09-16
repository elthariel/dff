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
 *
 */

%module(package="api.module") libcmodule
%include "std_string.i"
%include "std_list.i"
%include "std_map.i"
%include "std_except.i"

typedef unsigned long long dff_ui64;

//%catches(vfsError, envError) CModule::OpenDump(argument* arg);
%{
#include "export.hpp"
#include "cmodule.hpp"
//#include "conf.hpp"
#include "fdmanager.hpp"
%}
%include "../include/export.hpp"
%include "../include/cmodule.hpp"
//%include "../include/conf.hpp"
%include "../include/fdmanager.hpp"

namespace std
{
%template(listCModule)   list<CModule*>;
%template(mapcmodule)    map<string, CModule*>;
%template(listString)   list<string>;
};
