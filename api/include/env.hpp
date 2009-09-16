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
 *  Frederic B. <fba@digital-forensic.org>
 *
 */

#ifndef __ENV_HPP__
#define __ENV_HPP__ 

#include <string>
#include <list>
#include <map>
#include "vars.hpp"
#include "exceptions.hpp"

using namespace std;

/**
 * @file   env.hpp
 * @author  <sja@digital-forensic.org>
 * @date   Mon Aug 17 18:04:22 2009
 * 
 * @brief  This class define a key. It hold description and value of the argument in a list
 * 
 * 
 */
class v_key
{
public:
  EXPORT v_key();		/**<  */
  EXPORT ~v_key();		/**<  */
  list<class v_descr*> descr_l;	/**<  */
  list<class v_val*> val_l;	/**<  */

  /** 
   * 
   * 
   * @param v 
   */
  EXPORT void add_var_descr(v_descr *v);

  /** 
   * 
   * 
   * @param v 
   */
  EXPORT void add_var_val(v_val *v);
};

typedef map< string, v_key * > mapdb_t;


/**
 * @file   env.hpp
 * @author  <solal.jacob@arxsys.fr>
 * @date   Mon Aug 17 18:04:50 2009
 * 
 * @brief  This singleton class contain a map of all key by name 
 * 
 * 
 */
class env
{
private:
  /** 
   * 
   * 
   */
  env() {};

  /** 
   * 
   * 
   */
  ~env() {};

  /** 
   * 
   * 
   */
  void operator=(env&);

  /** 
   * 
   * 
   */
  env(const env&);
public:
  mapdb_t vars_db;		/**<  */

  /** 
   * 
   * 
   * 
   * @return permit to get the object env 
   */
  static env* Get() 
  {
    static env single;
    return &single;
  };

  /** 
   * 
   * 
   * @param v 
   */
  EXPORT void add_var_descr(class v_descr *v);

  /** 
   * 
   * 
   * @param v 
   */
  EXPORT void add_var_val(class v_val *v);
};

#endif
