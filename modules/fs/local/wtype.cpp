/*
 * DFF -- An Open Source Digital Forensics Framework
 * Copyright (C) 2009-2010 ArxSys
 * This program is free software, distributed under the terms of
 * the GNU General Public License Version 2. See the LICENSE file
 * at the top of the source tree.
 *  
 * See http: *www.digital-forensic.org for more information about this
 * project. Please do not directly contact any of the maintainers of
 * DFF for assistance; the project provides a web site, mailing lists
 * and IRC channels for your use.
 * 
 * Author(s):
 *  Solal Jacob <sja@digital-forensic.org>
 */

#include "wtype.hpp"
#include <string.h>
using namespace std;

w_vtime::w_vtime(FILETIME* t)
{
   LPSYSTEMTIME tm;
   
   FileTimeToSystemTime(t, tm);
   year = tm->wYear;
   month = tm->wMonth;
   day = tm->wDay;
   hour = tm->wHour;
   minute = tm->wMinute; 
   second = tm->wSecond;
   dst = 0;
   wday = tm->wDayOfWeek;
   yday = 0; 
   usecond = 0;	
}

w_attrib::w_attrib(WIN32_FILE_ATTRIBUTE_DATA info)
{
  if (!(info.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY))
  {
    s_ull  conv;
	conv.Low = info.nFileSizeLow;
	conv.High = info.nFileSizeHigh;
    size  = conv.ull;
  }
  time["accessed"] = new w_vtime(&(info.ftLastAccessTime));
  time["modified"] = new w_vtime(&(info.ftLastWriteTime));
  time["changed"] = new w_vtime(&(info.ftCreationTime));
}

w_attrib::w_attrib(WIN32_FIND_DATAA info)
{
  if (!(info.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY))
  {
    s_ull  conv;
	conv.Low = info.nFileSizeLow;
	conv.High = info.nFileSizeHigh;
    size  = conv.ull;
  }
  time["accessed"] = new w_vtime(&(info.ftLastAccessTime));
  time["modified"] = new w_vtime(&(info.ftLastWriteTime));
  time["changed"] = new w_vtime(&(info.ftCreationTime));
}
