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

#ifndef __ATTRIB_HPP__
#define __ATTRIB_HPP__

#include <string>
#include <map>
#include "type.hpp"

using namespace std;


/**
 * @file   attrib.hpp
 * @author  <sja@digital-forensic.org>
 * @date   Mon Aug 17 17:45:34 2009
 * 
 * @brief  This class permit to stock Handle of type string or dff_ui64
 * 
 * 
 */

class Handle
{
 public:
  /** 
   * 
   * 
   */
  Handle();

  /** 
   * 
   * 
   * @param dff_ui64 handle  
   * 
   * @return 
   */
  EXPORT	Handle(dff_ui64);

  /** 
   * 
   * 
   * @param string handle
   * 
   * @return 
   */
  EXPORT	Handle(string);

  /** 
   * 
   * 
   * @param dff_ui64 handle
   * @param string handle
   * 
   * @return 
   */
  EXPORT	Handle(dff_ui64, string);

  dff_ui64	id;		/**<  */
  string	name;		/**<  */
};


/**
 * @file   attrib.hpp
 * @author  <jacob.solal@arxsys.fr>
 * @date   Mon Aug 17 17:45:38 2009
 * 
 * @brief  This class stock the differente attribute of a Node
 * 
 * 
 */

class attrib
{
//differencier attrib dff vfs / attrib driver / attrib user
//string 'from' ou creer auto avec le nom du driver ou fsobj ou ...
public:

  /** 
   * 
   * 
   * 
   * @return 
   */
  EXPORT						attrib();

  /** 
   * 
   * 
   * 
   * @return 
   */
  EXPORT virtual					~attrib();

  map<string, string >   				smap; /**<  */
  map<string, vtime* > 					time; /**<  */
  map<string, unsigned int >  				imap; /**<  */
  dff_ui64	 					size; /**<  */
  Handle*						handle;	/**<  */
};

#endif

