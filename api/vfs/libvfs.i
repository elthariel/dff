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

%module(package="api.vfs",docstring="libvfs: c++ generated inteface", directors="1") libvfs 
%feature("autodoc", 1); //1 = generate type for func proto, no work for typemap
%feature("docstring");

%feature("director") fso;

%feature("director:except") fso 
{
    if ($error != NULL) 
    {
      throw Swig::DirectorMethodException();
    }
}

%include "std_string.i"
%include "std_list.i"
%include "std_set.i"
%include "std_map.i"
%include "std_except.i"
%include "windows.i"

%import "../exceptions/libexceptions.i"
%catches(vfsError) Node::open(void);
%catches(vfsError) VFile::read(void);
%catches(vfsError) VFile::read(unsigned int size);
%catches(vfsError) VFile::read(void *buff, unsigned int size);
%catches(vfsError) VFile::write(char *, unsigned int);
%catches(vfsError) VFile::write(string buff);
%catches(vfsError) VFile::close(void);
%catches(vfsError) VFile::seek(dff_ui64 offset,char *chwence);
%catches(vfsError) VFile::seek(dff_ui64 offset);
%catches(vfsError) VFile::tell(void);
%catches(envError) fso::start(argument* args); fso::vopen(Handle *handle); Node::open(void);
%catches(vfsError) fso::start(argument* args); fso::vopen(Handle *handle); Node::open(void);
%catches(vfsError) fso::vopen(Handle *handle);

%feature("director") fso::__getstate__;

%exception start
{
   try
   {
       SWIG_PYTHON_THREAD_BEGIN_ALLOW;
       $action 
       SWIG_PYTHON_THREAD_END_ALLOW;
   }
   catch (Swig::DirectorException e) 
   {
     SWIG_PYTHON_THREAD_BEGIN_BLOCK;
     SWIG_fail; 
     SWIG_PYTHON_THREAD_END_BLOCK;
   }
}

%exception open 
{
    try 
    { 
  //    SWIG_PYTHON_THREAD_BEGIN_BLOCK;
   //   SWIG_PYTHON_THREAD_BEGIN_ALLOW;
      $action 
       //SWIG_PYTHON_THREAD_END_ALLOW;
    //  SWIG_PYTHON_THREAD_END_BLOCK;
    }
    catch (Swig::DirectorException e) 
    {
        SWIG_fail;
    }
    catch (vfsError &e)
    {
      SWIG_PYTHON_THREAD_BEGIN_BLOCK;
      SWIG_Python_Raise(SWIG_NewPointerObj((new vfsError(static_cast< const vfsError& >(e))),SWIGTYPE_p_vfsError, SWIG_POINTER_OWN), "vfsError", SWIGTYPE_p_vfsError); 
      SWIG_PYTHON_THREAD_END_BLOCK;
      SWIG_fail;
    }
    catch (const std::exception &e)
    {
     SWIG_exception(SWIG_RuntimeError, e.what());
    }
}


typedef unsigned long long dff_ui64; 

%typemap(directorargout) (void *buff , unsigned int size)   
{
   memcpy((char *)buff, PyString_AsString($input) , PyString_Size($input));
}

%typemap(out) pdata*  
{
  Py_XDECREF($result);
  $result = PyString_FromStringAndSize((const char *)$1->buff, $1->len);
  free($1->buff);
}

%typemap(in) PyObject* pyfunc
{
  if (!PyCallable_Check($input))
  {
    PyErr_SetString(PyExc_TypeError, "Need a callable object!");
    return NULL;
  }
  $1 = $input;
}

%{
  #include "export.hpp"
  #include "vfs.hpp"
  #include "node.hpp"
  #include "fso.hpp"
  #include "vfile.hpp"

  static void PythonCallBack(void *data, Node* pnode)
  {
    PyObject *func, *arglist;
    PyObject *result = NULL;

    SWIG_PYTHON_THREAD_BEGIN_BLOCK;
    func = (PyObject *) data;
    PyObject* obj = SWIG_NewPointerObj((void *)pnode, SWIGTYPE_p_Node, 0);
    arglist = Py_BuildValue("(O)", obj) ;

    result = PyEval_CallObject(func, arglist);
    fflush(stdout); 
//  fflush(stderr);
    Py_DECREF(arglist);
    SWIG_PYTHON_THREAD_END_BLOCK;
    Py_XDECREF(result);

    return ;
  }

 static PyObject* __CBgetstate__(void* data)
 {
    PyObject *func, *result = NULL;

    SWIG_PYTHON_THREAD_BEGIN_BLOCK;
    func = (PyObject *) data;
    result = PyEval_CallObject(func, NULL);
    fflush(stdout); 
    SWIG_PYTHON_THREAD_END_BLOCK;
    if (!result)
      return NULL;   
    return result;
  }
%}

%include "../include/export.hpp"
%include "../include/vfs.hpp"
%include "../include/node.hpp"
%include "../include/fso.hpp"
%include "../include/vfile.hpp"

namespace std
{
  %template(ListNode)     list<Node*>;
  %template(SetNode)      set<Node *>;
  %template(Listui64) list<dff_ui64>;
};
%newobject VFile::read;
%newobject VFile::argument;

%extend VFS
{
  void set_callback(string type, PyObject* pyfunc)
  {
    self->SetCallBack(PythonCallBack, (void* ) pyfunc, type);
    Py_INCREF(pyfunc);
  }
};

%extend fso 
{
 void set_getstate(PyObject *pyfunc)
 {
   self->SetCallBack(__CBgetstate__, (void*)pyfunc);
   Py_INCREF(pyfunc);
 } 
};


%extend Node
{
%pythoncode
%{
def __iter__(self):
  for node in self.next:  
     yield node
%}
};
