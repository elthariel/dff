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


#include "utype.hpp"

u_vtime::u_vtime(struct tm* t)
{
   year = t->tm_year + 1900; 
   month = t->tm_mon + 1; 
   day = t->tm_mday; 
   hour = t->tm_hour;
   minute = t->tm_min; 
   second = t->tm_sec; 
   dst = t->tm_isdst; 
   wday = t->tm_wday;
   yday = t->tm_yday; 
   usecond = 0;	
}

tm* u_vtime::get_tm(void)
{
  tm* t  = (tm *)malloc(sizeof(tm));
  t->tm_year = year - 1900;
  t->tm_mon = month - 1;
  t->tm_mday = day;
  t->tm_hour = hour;
  t->tm_min = minute;
  t->tm_sec = second;
  t->tm_isdst = dst;
  t->tm_wday = wday;
  t->tm_yday = yday;
  return (t);
}

u_attrib::u_attrib(struct stat  *st)
{
  if (((st->st_mode & S_IFMT) == S_IFDIR))
    size = 0;
  else
    size  = (dff_ui64)st->st_size;
  time["accessed"] = new u_vtime(gmtime(&st->st_atime));
  time["modified"] = new u_vtime(gmtime(&st->st_mtime));
  time["changed"] = new u_vtime(gmtime(&st->st_ctime));
  imap["block-size"] = st->st_blksize; 
  imap["blocks"] = st->st_blocks;
}

u_attrib::u_attrib(struct stat  *st, char *path)
{
  int	fd;
  unsigned long	numsectors;

  if (S_ISBLK(st->st_mode))
    {
      if ((fd = open(path, O_RDONLY | O_LARGEFILE)) == -1)
	;
      else
	{
	  if (ioctl(fd, BLKGETSIZE, &numsectors) < 0)
	    ;
	  else
	      size = (dff_ui64)numsectors * 512;
	  close(fd);
	}
    }
  else
  { 
    if (((st->st_mode & S_IFMT) == S_IFDIR))
      size = 0;
    else
      size  = (dff_ui64)st->st_size;
  }
  time["accessed"] = new u_vtime(gmtime(&st->st_atime));
  time["modified"] = new u_vtime(gmtime(&st->st_mtime));
  time["changed"] = new u_vtime(gmtime(&st->st_ctime));
  imap["block-size"] = st->st_blksize; 
  imap["blocks"] = st->st_blocks;
}

void u_attrib::get_stat(struct stat* st)
{
   map<string, vtime *>::iterator i = time.begin();
  
   for (; i != time.end(); ++i)
   {
     u_vtime* cur_time = static_cast<u_vtime *>(i->second);  	

     if (i->first == string("accessed"))
        st->st_atime = mktime(cur_time->get_tm());
     else if (i->first == string("modified"))
        st->st_mtime = mktime(cur_time->get_tm());
     else if (i->first == string("changed"))
        st->st_ctime = mktime(cur_time->get_tm());
   }
}

