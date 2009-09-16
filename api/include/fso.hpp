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

/**
 * @file   fso.hpp
 * @author  <sja@digital-forensic.org>
 * @date   Mon Aug 17 18:07:06 2009
 * 
 * @brief  This class describe a file system object. It permit to create a driver when it's virtual function are implemented 
 * 
 * 
 */
class fso 
{
private:
//virer sa
  unsigned int		NodeDirNumbers;	/**<  */
  unsigned int		NodeFileNumbers; /**<  */
//bouger ds une classe a part
public:
  argument*		arg;	/**<  */
  results*		res;	/**<  */
  string 		name;	/**<  */
  string		stateinfo; /**<  */

  /** 
   * 
   * 
   * 
   * @return 
   */
  EXPORT 		fso();

  /** 
   * 
   * 
   * 
   * @return 
   */
  EXPORT virtual 	~fso();

  /** 
   * 
   * 
   * @param args, this virtual function is the first called when an fso is initialised
   */
  virtual void		start(argument* args) = 0;

  /** 
   * 
   * 
   * @param handle This function is called when the open function is performed on a fso. The handle permit to distinguish between different opened file.
   * 
   * @return 
   */
  virtual int 		vopen(Handle *handle) = 0;

  /** 
   * 
   * 
   * @param fd is the file descriptor corresponding to the underlaying file where the read function will apply 
   * @param buff is the buffer where data will be copied during the read operations
   * @param size determine the size of the data excpected to be read
   * 
   * @return 
   */
  virtual int 		vread(int fd, void *buff, unsigned int size) = 0;

  /** 
   * 
   * 
   * @param fd 
   * @param buff 
   * @param size 
   * 
   * @return 
   */
  virtual int 		vwrite(int fd, void *buff, unsigned int size) = 0;

  /** 
   * 
   * 
   * @param fd 
   * 
   * @return 
   */
  virtual int 		vclose(int fd) = 0; 

  /** 
   * 
   * 
   * @param fd 
   * @param offset 
   * @param whence , whence can take the value SET, CUR or END. Positioning the file respectively at offset, current location plus offset, end of file plus offset
   * 
   * @return 
   */
  virtual dff_ui64	vseek(int fd, dff_ui64 offset, int whence) = 0;

  /** 
   * 
   * 
   * 
   * @return 
   */
  virtual unsigned int	status(void) = 0;

  /** 
   * 
   * 
   * @param parent, the created node will be linked to this parent Node 
   * @param name, the name of the newly created node 
   * @param attr, the attribute of the node
   * 
   * @return 
   */
  EXPORT  class Node* 	CreateNodeDir(Node* parent, string name, class attrib* attr);

/** 
 * 
 * 
 * @param parent, the created node vill be linked to this parent Node
 * @param name , the name of the newly created node
 * @param attr , the attribute of the node
 * 
 * @return 
 */
  EXPORT  Node* 	CreateNodeFile(Node* parent, string name, attrib* attr);
  list<Node*>		nl;	/**<  */

  /** 
   * 
   * 
   * 
   * @return 
   */
  unsigned int 		AddNodes(void);
};

typedef class fso* create_t(void);
typedef void  destroy_t(void);

#endif
