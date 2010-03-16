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

%module(package="api.type") libtype
%ignore attrib::attrib(struct stat*);
%ignore attrib::get_stat(struct stat*);
%include "std_string.i"
%include "std_map.i"
%include "windows.i"

typedef unsigned long long dff_ui64; 

%{
#include <sys/stat.h>
#include <datetime.h>
#include "export.hpp"
#include "type.hpp"
#include "vtime.hpp"
#include "attrib.hpp"
%}
%include "../include/export.hpp"
%include "../include/type.hpp"
%include "../include/vtime.hpp"
%include "../include/attrib.hpp"

%extend vtime
{
  PyObject* vtime::get_time(void)
  {
    SWIG_PYTHON_THREAD_BEGIN_BLOCK;
    PyDateTime_IMPORT;
    SWIG_PYTHON_THREAD_END_BLOCK;
    PyObject* v;

    v = PyDateTime_FromDateAndTime(self->year, self->month, self->day, 
    self->hour, self->minute, self->second, self->usecond);
    return (v);
  }
};

namespace std
{
  %template(MapString)    map<string, string>;
  %template(MapVtime)     map<string,   vtime* >;
  %template(MapInt)       map<string, unsigned int>;
};

%traits_swigtype(vtime);
%fragment(SWIG_Traits_frag(vtime));
