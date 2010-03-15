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

#ifndef __FSO_HH__
#define __FSO_HH__
#include <iostream>
#include <stdio.h>
#include <list>
#include <map>
#include <vector>

#include "export.hpp"
#include "type.hpp"
#include "vfs.hpp"
#include "argument.hpp"
#include "results.hpp"

using namespace std;

#include <Python.h>
typedef PyObject* (*CBGETFUNC) (void *);
typedef void (*CBSETFUNC) (void *, PyObject*);

class fso 
{
//private:
public:
//virer sa
  unsigned int		NodeDirNumbers;	
  unsigned int		NodeFileNumbers;
//bouger ds une classe a part
  argument*		arg;
  results*		res;
  string 		name;
  string		stateinfo; 
  list<Node*>		nl;

  EXPORT 		fso();
  EXPORT virtual 	~fso();


  PyObject*             __getstate__(void);
  void*                 getpyfunc;
  CBGETFUNC             getcbfunc;


  EXPORT  class Node* 	CreateNodeDir(Node* parent, string name, class attrib* attr, bool refresh = false);
  EXPORT  Node* 	CreateNodeFile(Node* parent, string name, attrib* attr, bool refresh = false);
  unsigned int 		AddNodes(void);
  void                  SetCallBack(CBGETFUNC func, void* data);
  virtual void		start(argument* args) = 0;
  virtual int 		vopen(Handle *handle) = 0;
  virtual int 		vread(int fd, void *buff, unsigned int size) = 0;
  virtual int 		vwrite(int fd, void *buff, unsigned int size) = 0;
  virtual int 		vclose(int fd) = 0; 
  virtual dff_ui64	vseek(int fd, dff_ui64 offset, int whence) = 0;
  virtual unsigned int	status(void) = 0;
};

typedef class fso* create_t(void);
typedef void  destroy_t(void);

#endif
