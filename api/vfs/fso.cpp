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

#include "fso.hpp"

fso::fso()
{
}

fso::~fso()
{

}

unsigned int	fso::AddNodes(void)
{
  return VFS::Get().AddNodes(nl);
}

Node 	*fso::CreateNodeFile(Node *parent, string name, attrib* attr)
{
  Node* n;

  n = VFS::Get().CreateNodeFile((fso*)this, parent, name, attr);
  nl.push_back(n);

 // return (VFS::Get().CreateNodeFile((fso*)this,  parent, name, attr));
  return (n);
}

Node	*fso::CreateNodeDir(Node *parent, string name, attrib* attr)
{
  Node* n;

  n = VFS::Get().CreateNodeFile((fso*)this, parent, name, attr);
  nl.push_back(n);

  return (n);
}
