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

/**
 * @file   vfs.hpp
 * @author  <sja@digital-forensic.org>
 * @date   Mon Aug 17 17:33:30 2009
 * 
 * @brief  
 * 
 * 
 */

class CallBack
{
  public:
  /** 
   * 
   * 
   * @param func 
   * @param data 
   */
    CallBack(CBFUNC func, void *data) { cbfunc = func; cbdata = data; };
    void*	cbdata;		/**<  */
    CBFUNC	cbfunc;		/**<  */
};

class VFS 
{  
private:
  class Node*   cwd;		/**<  */
  set<Node*>    Tree;		/**<  */
  list<CallBack*> cbl;  	/**<  */
  list<CallBack*> cbl_pp;  	/**<  */
  Node*		root;		/**<  */

  /** 
   * 
   * 
   * 
   * @return 
   */
  EXPORT 	VFS();

  /** 
   * 
   * 
   * 
   * @return 
   */
  EXPORT 	~VFS();

  /** 
   * 
   * 
   * 
   * @return 
   */
  VFS& operator=(VFS&);

  /** 
   * 
   * 
   */
  VFS(const VFS&);

  /** 
   * 
   * 
   * @param string 
   * @param parent 
   * 
   * @return 
   */
  string	sanitaze(string, Node* parent);
public:
  /** 
   * 
   * 
   * 
   * @return 
   */
  static VFS&   Get() 
  { 
    static VFS single; 
    return single; 
  }

  /** 
   * 
   * 
   * 
   * @return 
   */
  EXPORT	set<Node*>*  	GetTree(void);

  /** 
   * 
   * 
   */
  void 		cd(Node *);

  /** 
   * 
   * 
   * 
   * @return 
   */
  Node* 	GetCWD(void);

  /** 
   * 
   * 
   * @param path 
   * 
   * @return 
   */
  Node*		GetNode(string path);

  /** 
   * 
   * 
   * @param path 
   * @param where 
   * 
   * @return 
   */
  Node*		GetNode(string path, Node* where);

  /** 
   * 
   * 
   * @param fsobj 
   * @param parent 
   * @param name 
   * @param attr 
   * 
   * @return 
   */
  Node*		CreateNodeDir(class fso *fsobj,  Node* parent, string name, class attrib* attr); 

  /** 
   * 
   * 
   * @param fsobj 
   * @param parent 
   * @param name 
   * @param attr 
   * 
   * @return 
   */
  Node*		CreateNodeFile(fso *fsobj,  Node* parent, string name, attrib* attr); 

  /** 
   * 
   * 
   * 
   * @return 
   */
  EXPORT int	DeleteNode(Node*);

  /** 
   * 
   * 
   * @param nl 
   */
  void		DeleteNodeList(list<class Node* > nl);			

  /** 
   * 
   * 
   * @param func 
   * @param cbdata 
   * @param type 
   */
  void		SetCallBack(CBFUNC func, void* cbdata, string type);

  /** 
   * 
   * 
   * @param nl 
   * 
   * @return 
   */
  unsigned int	AddNodes(list<Node*> nl);
};
#endif

