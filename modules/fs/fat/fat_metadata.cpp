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
 *  Frederic Baguelin <fba@digital-forensic.org>
 *
 */

#include "fat.hpp"

void	Fat::SetAttr(RootDir rd, attrib *attr)
{
  attr->time["changed"] = date_dos2vtime(rd.CreatedTime, rd.CreatedDate);
  attr->time["accessed"] = date_dos2vtime(0, rd.LastAccessedDate);
  attr->time["modified"] = date_dos2vtime(rd.LastModifiedTime, rd.LastModifiedDate);
}

vtime	*Fat::date_dos2vtime(unsigned short dos_time, unsigned short dos_date)
{
  int	day;
  int	month;
  int	year;
  int	sec;
  int	min;
  int	hour;

  day = dos_date & 31;
  month = (dos_date >> 5) & 15;
  year = (dos_date >> 9) + 1980;

  sec = dos_time & 31;
  min = (dos_time >> 5) & 63;
  hour = dos_time >> 11;

  return new vtime(year, month, day, hour, min, sec, 0);
}
