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
 *  Frederic B. <fba@digital-forensic.org>
 */

%module(package="api.search") libsearch

%include "std_string.i"
%include "std_list.i"
%include "windows.i"

%{
#include "../include/export.hpp"
#include "../include/search.hpp"
#include "boyer_moore.hpp"
%}
%import "../include/export.hpp"
%include "../include/search.hpp"
%include "boyer_moore.hpp"

typedef unsigned long long dff_ui64;

namespace std
{
  %template(Listui64) list<dff_ui64>;
};
