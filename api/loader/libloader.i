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

%module(package="api.loader") libloader
%include "std_string.i"
%include "std_list.i"
%include "std_set.i"
%include "std_map.i"
%include "windows.i"
%import "../module/libcmodule.i"

%catches(LoaderError) Loader::LoadCModule(string path);
%{
#include "../include/export.hpp"
#include "../include/loader.hpp"
%}
%include "../include/export.hpp"
%include "../include/loader.hpp"
%import "../include/cmodule.hpp"

namespace std 
{
%template(mapcmodule)    map<string, CModule * >;
};
