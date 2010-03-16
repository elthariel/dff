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
 *  Frederic Baguelin <fba@digital-forensic.org>
 */

#include "fat.hpp"

int			Fat::GetSlack(FileInfo *owner)
{
  unsigned long long	handle;
  FileInfo		*fi;
  Info			*info;
  attrib		*attr;
  unsigned int		slack_size;
  unsigned int		cluster;
  int			index;

  info = info_stack.top();
  slack_size = (((owner->size / ClusterSize) + 1) * ClusterSize) - owner->size;
  index = owner->clusters->size() - 1;
  if ((slack_size > 0) && (index >= 0))
    {
      fi = new FileInfo;
      fi->type = SLACK;
      fi->clusters = new vector<unsigned int>;
      fi->size = slack_size;
      if (owner->type == DELETED)
	{
	  cluster = (*(owner->clusters))[index];
	  cluster += (owner->size / ClusterSize);
	  fi->clusters->push_back(cluster);
	}
      else
	{
	  cluster = (*(owner->clusters))[index];
	  fi->clusters->push_back(cluster);
	}
      handle = filehandler->add(fi);
      if (handle != (unsigned long long) -1)
	{
	  attr = new attrib;
	  attr->handle = new Handle(handle);
	  attr->size = slack_size;
	  if (owner->type == DELETED)
	    CreateNodeFile(DeletedItems, info->filename + ".slack", attr);
	  else
	    CreateNodeFile(info->parent, info->filename + ".slack", attr);
	  return (0);
	}
      else
	{
	  throw vfsError("Fat: cannot register slack of file\n");
	}
    }
}
