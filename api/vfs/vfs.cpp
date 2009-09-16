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

#include "vfs.hpp"

VFS::VFS()
{
  root = new Node;
  root->name = "";
  root->path = "";
  root->is_root = 1; 
  root->is_file = 0;
  root->attr = new attrib();
  root->parent = root;
  cwd = root;
  Tree.insert(root);
  //vp->attr->size = 0;

//cb_refresh_tree = 0 
}

VFS::~VFS()
{
  DeleteNode(root);
}

void	VFS::DeleteNodeList(list<class Node *> nl)
{
   list<Node*>::iterator i = nl.begin();
  
   for (; i != nl.end(); i++)
   { 
     if ((*i)->next.size())
       DeleteNodeList((*i)->next);
     if ((*i) == cwd)
       cwd = root;
     Tree.erase(*i);
   }
}

int VFS::DeleteNode(Node *node)
{
  list<Node*>::iterator i = node->next.begin();
 
  DeleteNodeList(node->next);
  i = node->parent->next.begin();
  for (; i != node->parent->next.end(); ++i)
  {
    if (*i == node)
    {
      Tree.erase(*i);
      node->parent->next.erase(i);
      break;
    }
  }
  return (1);
}

void VFS::cd(Node *path)
{
  cwd = path;
}

Node* VFS::GetCWD(void)
{
  return (cwd);
}

set<Node *>* VFS::GetTree(void)
{
  return (&Tree);
}

Node* VFS::GetNode(string path, Node* where)
{
  list<Node *>::iterator i = where->next.begin();

  if (path == "..")
    return (where->parent);	
  for (; i != where->next.end(); i++)
  {
     if ((*i)->name == path)
        return (*i); 
  }
  return (0);
}

Node* VFS::GetNode(string path)
{
  if (path == "/")
    return root;	
  path = path.substr(path.find('/') + 1);
  string lpath;
  string rpath = path;
  Node* tmp = root;
  do
  {
     if (rpath.find('/') != -1)	
     {
       lpath = rpath.substr(0, rpath.find('/'));
       rpath = rpath.substr(rpath.find('/') + 1); 
     }
     else
     { 
       lpath = rpath;
       rpath = "";	
     }
     tmp = GetNode(lpath, tmp);
  }  while (tmp && rpath.size());
  return (tmp);
}

unsigned int VFS::AddNodes(list<Node*>  nl)
{
  unsigned int num = 0;
  list<Node* >::iterator n = nl.begin();

  if (!nl.size())
    return 0;
  for(;n  != nl.end(); n++)
  {
    (*n)->parent->addchild((*n));
    Tree.insert((*n));
    num++;
    list<CallBack* >::iterator cb_pp = cbl_pp.begin();
    for (; cb_pp != cbl_pp.end(); cb_pp++)
    {
      (*cb_pp)->cbfunc((*cb_pp)->cbdata, *n);
    }
  }
  list<CallBack* >::iterator cb = cbl.begin();
  for (; cb != cbl.end(); cb++)
  {
    (*cb)->cbfunc((*cb)->cbdata, (*nl.begin()));
  }
  return (num);
  
}

string  VFS::sanitaze(string name, Node* parent)
{
   string tmp;
   string::iterator i = name.begin();

   for (; i != name.end(); ++i)
   {
      if (*i >= ' ' && *i <= '~')
        tmp += *i;
      else
        tmp += '\?';
   }
   name = tmp;
   list<Node*>::iterator n = parent->next.begin();
   for (; n != parent->next.end(); ++n)
   {
     if (name == (*n)->name)
     {
       (*n)->same++;
       char num[11] = {0}; 
       sprintf(num, "%d", (*n)->same);
       name += "." + string(num);
     }
   }
  return (name);
}

Node* VFS::CreateNodeDir(fso *fsobj, Node* parent, string name, attrib *attr)
{
  Node *vp = new Node;

  if (parent->name.size() == 0)
    vp->path = "";
  else
    vp->path += parent->path + "/" + parent->name;
  vp->fsobj = fsobj; 
  vp->name = sanitaze(name, parent);
  vp->attr = attr;
  vp->parent = parent;
  vp->is_file = 0;
  vp->attr->size = 0;

  return (vp);
}

Node* VFS::CreateNodeFile(fso *fsobj, Node* parent, string name, attrib *attr)
{
  Node *vp = new Node;

  if (parent->name.size() == 0)
    vp->path = "";
  else
    vp->path += parent->path + "/" + parent->name;
  vp->fsobj = fsobj;
  vp->name = sanitaze(name, parent);
  vp->attr = attr;
  vp->parent = parent;
  vp->is_file = 1;

  return (vp);
}

void	VFS::SetCallBack(CBFUNC func, void* data, string type)
{
  if (type == "refresh_tree")
    cbl.push_back(new CallBack(func, data));
  else if (type == "post_process")
    cbl_pp.push_back(new CallBack(func, data));
}

