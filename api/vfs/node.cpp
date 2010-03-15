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
 *  Solal J. <sja@digital-forensic.org>
 */

#include "node.hpp"

Node::Node()
{
  is_root = 0;
  is_file = 0;
  same = 0;
}

Node::~Node()
{
}

string Node::absolute(void)
{
  string abs = path + "/" + name;

  return abs;
}


VFile* Node::open(void)
{
  int fd;
  VFile *temp;
  try 
  {
    if ((is_file) && ((fd = fsobj->vopen(attr->handle)) >= 0))
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
bool Node::has_child(void)
{
  return (!next.empty());
}

bool Node::empty_child(void)
{
  return next.empty();
}

void Node::addchild(Node* path)
{
  next.push_back(path);
}

Link::Link(Node *n, Node* p)
{
  node = n;
  name = node->name;
  parent = p;
  p->addchild(n);
}

Link::Link(Node *n, string nname, Node *p)
{
  node = n;
  name = nname;
  parent = p;
  p->addchild(n);
}

Link::~Link()
{
}
