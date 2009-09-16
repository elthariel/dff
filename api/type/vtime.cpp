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

#include "vtime.hpp"

vtime::vtime()
{
}

vtime::~vtime()
{
}

vtime::vtime(int y, int mo, int d, int h, int mi, int s, int us)
{
   year = y; month = mo; day = d; hour = h; minute = mi; second = s; 
   usecond = us; 
}
