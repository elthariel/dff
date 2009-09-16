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

#ifndef __VPATH_HH__
#define __VPATH_HH__

#include <stdlib.h> 
#include <string>
#include <string.h>
#include "node.hpp"
#include "type.hpp"
#include "export.hpp"

using namespace std;

class Node;


typedef struct _pdata
{
  void *buff;
  dff_ui64 len;
} pdata;


/**
 * @file   vfile.hpp
 * @author  <sja@digital-forensic.org>
 * @date   Mon Aug 17 18:09:57 2009
 * 
 * @brief  
 * 
 * 
 */
class VFile
{
  public:
  int		fd;		/**<  */
  class 	Node*  		node; /**<  */

  /** 
   * 
   * 
   * 
   * @return 
   */
  EXPORT	int 		close(void);

  /** 
   * 
   * 
   * 
   * @return 
   */
  pdata*		read(void);

  /** 
   * 
   * 
   * @param size 
   * 
   * @return 
   */
  pdata*		read(unsigned int size);

  /** 
   * 
   * 
   * @param buff 
   * @param size 
   * 
   * @return 
   */
  EXPORT	int 		read(void *buff, unsigned int size);

  /** 
   * 
   * 
   * @param offset 
   * @param whence 
   * 
   * @return 
   */
  EXPORT	dff_ui64 	seek(dff_ui64 offset, char *whence);

  /** 
   * 
   * 
   * @param offset 
   * @param whence 
   * 
   * @return 
   */
  EXPORT	dff_ui64 	seek(dff_ui64 offset, int whence);

  /** 
   * 
   * 
   * @param offset 
   * 
   * @return 
   */
  EXPORT    	dff_ui64 	seek(dff_ui64 offset);

  /** 
   * 
   * 
   * @param offset 
   * @param whence 
   * 
   * @return 
   */
  EXPORT	long long	seek(int offset, int whence);

  /** 
   * 
   * 
   * @param buff 
   * 
   * @return 
   */
  EXPORT	int		write(string buff);

  /** 
   * 
   * 
   * @param buff 
   * @param size 
   * 
   * @return 
   */
  EXPORT    	int		write(char *buff, unsigned int size);

  /** 
   * 
   * 
   * 
   * @return 
   */
  int		fileno();

  /** 
   * 
   * 
   * 
   * @return 
   */
  dff_ui64 	tell();
};

#endif
