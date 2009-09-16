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
 *  Frederic B. <fba@digital-forensic.org>
 *
 */

#ifndef __FDMANAGER_HH__
#define __FDMANAGER_HH__
#include <vector>
#include "export.hpp"
#include "type.hpp"

using namespace std;

/*FD Structure*/

/**
 * @file   fdmanager.hpp
 * @author  <fba@digital-forensic.org>
 * @date   Mon Aug 17 17:56:46 2009
 * 
 * @brief  
 * 
 * 
 */
class FDInfo
{
  public:
  /** 
   * 
   * 
   */
  FDInfo() {};
  dff_ui64	current;	/**<  */
  void*		fdata;		/**<  */
};


/**
 * @file   fdmanager.hpp
 * @author  <udgover@madchat>
 * @date   Mon Aug 17 17:57:02 2009
 * 
 * @brief  
 * 
 * 
 */
class fdmanager
{
  private:
  vector<FDInfo*>	fdm; //files descriptors map /**<  */
  public: 
  unsigned int		fdallocated; /**<  */
  /*FD Manager*/

/** 
 * 
 * 
 * 
 * @return 
 */
  EXPORT bool		InitFDM();

  /** 
   * 
   * 
   * 
   * @return 
   */
  EXPORT bool		DeleteFDM();

  /** 
   * 
   * 
   * @param fd 
   * 
   * @return 
   */
  EXPORT bool		ClearFD(int fd);

  /** 
   * 
   * 
   * @param fd 
   * @param offset 
   * 
   * @return 
   */
  EXPORT dff_ui64	UpdateFD(int fd, dff_ui64 offset); 

  /** 
   * 
   * 
   * @param fdinfo 
   * 
   * @return 
   */
  EXPORT unsigned int	AllocFD(FDInfo* fdinfo);

  /** 
   * 
   * 
   * @param fd 
   * 
   * @return 
   */
  EXPORT FDInfo		*GetFDInfo(int fd);
};

#endif
