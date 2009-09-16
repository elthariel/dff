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

#include "node.hpp"

VFile* Node::open(void)
{
  int fd;
  VFile *temp;
  try 
  {
    if ((is_file) && ((fd = fsobj->vopen(attr->handle)) > 0))
    {
      temp = new VFile;
      temp->fd = fd;
      temp->node = this;
      
      return (temp);	
    }
    throw vfsError("Can't Open file"); 
  }
  catch (vfsError e)
  {
    throw vfsError("Node::open(void) throw\n" + e.error);
  }
}

void Node::addchild(Node* path)
{
  next.push_back(path);
}
