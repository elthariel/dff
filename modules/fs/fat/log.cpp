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

#include "log.hpp"

Log::Log()
{
  Log(1);
}

Log::Log(char a)
{
  active = a;
  printf("Logging enable\n");
  vfile = NULL;
  lfile = "";
}

Log::Log(string output_file, char filetype)
{
  if (filetype == VIRTUAL)
    {
      lfile = "";
    }
  else if (filetype == LOCAL)
    {
      lfile = output_file;
      vfile = NULL;
    }
  else
    printf("Undefined output file type\n");
}

Log::~Log()
{
}

int	Log::log(char *fmt, ...)
{
  va_list args;
  int size;
  char	buff[1024];

  va_start(args, fmt);
  size = vsnprintf(buff, 1024, fmt, args);
  if (size >= 1024)
    printf("output truncated :(\n");
  if ((vfile == NULL) && (lfile == "") && (active == 1))
    printf("%s\n", buff);
  else if (vfile != NULL)
    ;
  else if (lfile != "")
    ;
  else
    ;
  va_end(args);
  return size;
}
