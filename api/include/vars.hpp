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

#ifndef __VARS_HPP__
#define __VARS_HPP__

#include "export.hpp"
#include "type.hpp"
#include <string>
#include <iostream>


using namespace std;

/**
 * @file   vars.hpp
 * @author  <sja@digital-forensic.org>
 * @date   Mon Aug 17 18:00:01 2009
 * 
 * @brief  This class describe a variable used as argument
 * 
 * 
 */

class vars
{
public:
 string name;			/**<  */
 string description;		/**<  */
 string type;			/**<  */
 string from;			/**<  */
 bool	optional;		/**<  */
};


/**
 * @file   vars.hpp
 * @author  <solal.jacob@arxsys.fr>
 * @date   Mon Aug 17 18:00:20 2009
 * 
 * @brief  
 * 
 * 
 */
class v_descr : public vars
{
};


/**
 * @file   vars.hpp
 * @author  <solal.jacob@arxsys.fr>
 * @date   Mon Aug 17 18:00:24 2009
 * 
 * @brief  
 * 
 * 
 */
class v_descr_int : public v_descr
{
public:
  int max;			/**<  */
  int min;			/**<  */
  string descr;			/**<  */

  /** 
   * 
   * 
   * @param f 
   * @param n 
   * @param opt 
   * @param description 
   * 
   * @return 
   */
  EXPORT v_descr_int(string f, string n, bool opt, string description);

  /** 
   * 
   * 
   * @param f 
   * @param n 
   * @param x 
   * @param y 
   * @param opt 
   * @param description 
   * 
   * @return 
   */
  EXPORT v_descr_int(string f, string n, int x, int y, bool opt, string description);

  /** 
   * 
   * 
   * @param v 
   * 
   * @return 
   */
  EXPORT int  check_val(int v);
};


/**
 * @file   vars.hpp
 * @author  <solal.jacob@arxsys.fr>
 * @date   Mon Aug 17 18:00:50 2009
 * 
 * @brief  
 * 
 * 
 */
class v_descr_string : public v_descr
{
public:
  /** 
   * 
   * 
   * @param f 
   * @param n 
   * @param opt 
   * @param description 
   * 
   * @return 
   */
  EXPORT v_descr_string(string f, string n, bool opt, string description);
};


/**
 * @file   vars.hpp
 * @author  <solal.jacob@arxsys.fr>
 * @date   Mon Aug 17 18:01:00 2009
 * 
 * @brief  
 * 
 * 
 */
class v_descr_bool : public v_descr
{
public:
  /** 
   * 
   * 
   * @param f 
   * @param n 
   * @param opt 
   * @param description 
   * 
   * @return 
   */
  EXPORT v_descr_bool(string f, string n, bool opt, string description);
};


/**
 * @file   vars.hpp
 * @author  <solal.jacob@arxsys.fr>
 * @date   Mon Aug 17 18:01:07 2009
 * 
 * @brief  
 * 
 * 
 */
class v_descr_path : public v_descr
{
public:
  /** 
   * 
   * 
   * @param f 
   * @param n 
   * @param opt 
   * @param description 
   * 
   * @return 
   */
  EXPORT v_descr_path(string f, string n, bool opt, string description);
};

/**
 * @file   vars.hpp
 * @author  <solal.jacob@arxsys.fr>
 * @date   Mon Aug 17 18:01:16 2009
 * 
 * @brief  
 * 
 * 
 */
class v_descr_node : public v_descr
{
public:
  /** 
   * 
   * 
   * @param f 
   * @param n 
   * @param opt 
   * @param description 
   * 
   * @return 
   */
  EXPORT v_descr_node(string f, string n, bool opt, string description);
};


/**
 * @file   vars.hpp
 * @author  <solal.jacob@arxsys.fr>
 * @date   Mon Aug 17 18:01:25 2009
 * 
 * @brief  
 * 
 * 
 */
class v_val : public vars
{
public:
  /** 
   * 
   * 
   * 
   * @return 
   */
 EXPORT int get_int(void);

  /** 
   * 
   * 
   * 
   * @return 
   */
 EXPORT string get_string(void);

  /** 
   * 
   * 
   * 
   * @return 
   */
 EXPORT class Node* get_node(void);

  /** 
   * 
   * 
   * 
   * @return 
   */
 EXPORT class Path* get_path(void);

  /** 
   * 
   * 
   * 
   * @return 
   */
 EXPORT bool get_bool(void);
};


/**
 * @file   vars.hpp
 * @author  <udgover@madchat>
 * @date   Mon Aug 17 18:01:43 2009
 * 
 * @brief  
 * 
 * 
 */
class v_val_int : public v_val
{
public:
  int	value;			/**<  */

  /** 
   * 
   * 
   * @param f 
   * @param n 
   * @param v 
   * 
   * @return 
   */
  EXPORT v_val_int(string f, string n, int v);
};


/**
 * @file   vars.hpp
 * @author  <solal.jacob@arxsys.fr>
 * @date   Mon Aug 17 18:01:56 2009
 * 
 * @brief  
 * 
 * 
 */
class v_val_string : public v_val
{
public:
  string value;			/**<  */
  /** 
   * 
   * 
   * @param f 
   * @param n 
   * @param v 
   * 
   * @return 
   */
  EXPORT v_val_string(string f, string n, string v);
};


/**
 * @file   vars.hpp
 * @author  <solal.jacob@arxsys.fr>
 * @date   Mon Aug 17 18:02:20 2009
 * 
 * @brief  
 * 
 * 
 */
class v_val_bool : public v_val
{
public:
  bool value;			/**<  */

  /** 
   * 
   * 
   * @param f 
   * @param n 
   * @param v 
   * 
   * @return 
   */
  EXPORT v_val_bool(string f, string n, bool v);
};


/**
 * @file   vars.hpp
 * @author  <solal.jacob@arxsys.fr>
 * @date   Mon Aug 17 18:02:35 2009
 * 
 * @brief  
 * 
 * 
 */
class v_val_node : public v_val
{
public:
  class Node* value;		/**<  */

  /** 
   * 
   * 
   * @param f 
   * @param n 
   * @param v 
   * 
   * @return 
   */
  EXPORT v_val_node(string f, string n, Node* v);
};


/**
 * @file   vars.hpp
 * @author  <solal.jacob@arxsys.fr>
 * @date   Mon Aug 17 18:02:53 2009
 * 
 * @brief  
 * 
 * 
 */
class v_val_path : public v_val
{
public:
  class Path*	value;		/**<  */

  /** 
   * 
   * 
   * @param f 
   * @param n 
   * @param v 
   * 
   * @return 
   */
  EXPORT v_val_path(string f, string n, Path* v);
};

#endif
