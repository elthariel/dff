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

#ifndef __NODE_HH__
#define __NODE_HH__

#include <string>
#include <map>
#include <iostream>
#include <sys/types.h>
#include <sys/stat.h>
//#include <unistd.h>
#include "type.hpp"
#include "attrib.hpp"
#include "export.hpp"
#include "vfile.hpp"
#include "fso.hpp"

using namespace std;

class Node 
{
  public:
  list<class Node*>     next;
  Node*			parent;	
  attrib*		attr;	
  class fso*		fsobj;	
  unsigned int		same;
  string		name;
  string 		path;
  bool			is_file; 
  bool			is_root; 
  string		absolute(void);	
  bool                  has_child();  
  bool                  empty_child();
  EXPORT class VFile*	open(void);
  Node();
  ~Node();
  void  		addchild(Node* path);
};

class Link : public Node
{
public:
  Link(Node *, Node *);
  Link(Node *, string, Node *);
  Node*			node;
  string 		name;
  list<class Node*>     next;
  ~Link();
};


#endif
