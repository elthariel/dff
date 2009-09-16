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


/**
 * @file   node.hpp
 * @author  <sja@digital-forensic.org>
 * @date   Mon Aug 17 18:08:50 2009
 * 
 * @brief  This class handle nodes of the VFS
 * 
 * 
 */
class Node
{
  public:
  unsigned int		same;	/**<  */
  class fso*		fsobj;	/**<  */

  /** 
   * 
   * 
   * 
   * @return 
   */
  EXPORT class VFile*	open(void);
  attrib*		attr;	/**<  */
  string		name;	/**<  */
  string 		path;	/**<  */
  bool			is_file; /**<  */
  bool			is_root; /**<  */
  Node*			parent;	/**<  */
  list<class Node *>	next;	/**<  */

  /** 
   * 
   * 
   */
  Node() {  is_root = 0; is_file = 0; same = 0;/*nnext = 0; */};

  /** 
   * 
   * 
   */
  ~Node() {  };

  /** 
   * 
   * 
   * @param path, this function add a children to the current node
   */
  void  addchild(Node* path);
};

#endif
