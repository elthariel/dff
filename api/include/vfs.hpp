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

// \brief This class implements the virtual file system of the framework.

// The Virtual File System (VFS) is a central point of the framework.
// It permits to register nodes and browse them.

#ifndef __VFS_HH__
#define __VFS_HH__

#include "export.hpp"
#include "exceptions.hpp"
#include "type.hpp"
#include "vfile.hpp"
#include "node.hpp"
#include "fso.hpp"

#include <deque>
#include <list>
#include <set>

typedef void (*CBFUNC) (void *, class Node* pnode);

class CallBack
{
  public:
    CallBack(CBFUNC func, void *data) { cbfunc = func; cbdata = data; };
    void*	cbdata;	
    CBFUNC	cbfunc;	
};

class VFS 
{  
private:
  EXPORT 	        VFS();
  EXPORT                ~VFS();
  VFS&          operator=(VFS&);
                VFS(const VFS&);
  string	sanitaze(string, Node* parent);

public:
  class Node*           cwd;	
  Node*		        root;
  set<Node*>            Tree;
  list<CallBack*>       cbl;  
  list<CallBack*>       cbl_pp; 


  static VFS&   Get() 
  { 
    static VFS single; 
    return single; 
  }

  EXPORT set<Node*>*    GetTree(void);
  EXPORT void 	        cd(Node *);
  EXPORT Node* 	        GetCWD(void);
  EXPORT Node*	        GetNode(string path);
  EXPORT Node*	        GetNode(string path, Node* where);
  EXPORT Node*	        CreateNodeDir(class fso* fsobj ,  Node* parent, string name, class attrib* attr, bool refresh = false); 
  EXPORT Node*	        CreateNodeFile(fso* fsobj,  Node* parent, string name, attrib* attr, bool refresh = false); 
  EXPORT void	        SetCallBack(CBFUNC func, void* cbdata, string type);
  EXPORT unsigned int	AddNodes(list<Node*> nl);
  EXPORT void 		addNode(Node *n);
};
#endif

