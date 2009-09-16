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
 *  Solal Jacob <sja@digital-forensic.org>
 *
 */

#include "fuse.hpp"

extern "C" 
{
  static int f_getattr(const char *path, struct stat *stbuf)
  {
    Node* node;
    u_attrib	*attr;
    memset(stbuf, 0, sizeof(struct stat));

    node = vfs.GetNode(path);
    if (!node)
      return -ENOENT;
  
    if (node->next.size())
    {
      attr = static_cast<u_attrib *>(node->attr);
      attr->get_stat(stbuf); 
      stbuf->st_mode = S_IFDIR | 0755;
      stbuf->st_nlink = 2 + node->next.size();
    }
    else
    {
      attr = static_cast<u_attrib *>(node->attr);
      attr->get_stat(stbuf); 
      stbuf->st_mode = S_IFREG | 0444;
      stbuf->st_nlink = 1;
      stbuf->st_size = node->attr->size;
    }

      return 0;
  }

  static int f_readdir(const char *path, void *buf, fuse_fill_dir_t filler, off_t offset, struct fuse_file_info *fi)
 {
   Node *node;

   node = vfs.GetNode(path);
   if (!node)
     return -ENOENT;
   if (node->next.size())
   {
     filler(buf, ".", NULL, 0);
     filler(buf, "..", NULL, 0);
     list<Node*>::iterator i = node->next.begin();
     for (; i != node->next.end(); ++i)
     {
	filler(buf, (*i)->name.c_str(), NULL, 0);
     }
   }
   else
    return -ENOENT;

   return 0;
  }

  static int f_open(const char *path, struct fuse_file_info *fi)
  {
    Node *node;

    node = vfs.GetNode(path);
    if (!node)
      return -ENOENT;
    if (!node->is_file)
      return -ENOENT;
    if ((fi->flags & 3) != O_RDONLY)
      return -EACCES;

    return 0;
  }

  static int f_read(const char *path, char *buf, size_t size, off_t offset, struct fuse_file_info *fi)
  {
    Node 	*node;
    VFile 	*file;
    int		n;

    node = vfs.GetNode(path);
    if (!node)
      return 0;
    try
    {
      file = node->open();
      file->seek(offset);
      n = file->read(buf, size);
      file->close();
    }
    catch (vfsError e)
    {
      return 0;
    }
    return n;
  }

  struct f_oper : fuse_operations  
  {
    f_oper() 
    {
      getattr = f_getattr;
      open = f_open;
      readdir = f_readdir;
      read = f_read;
    }
  };
  static struct f_oper f_opers;
}

void fuse::start(argument* arg)
{
  Path		*tpath;
  char		**argv;

  try 
  { 
    arg->get("path", &tpath);
  }
  catch (envError e)
  {
    res->add_const("error", "conf " + e.error);
    return ;
  }
  
  argv = (char **)malloc(sizeof(char*) * 3); 
  *argv = (char *)"dff-fuse";
  *(argv + 1) = (char *)tpath->path.c_str();
  *(argv + 2) = (char *)"-d";
//loop :(
  fuse_main(3, argv, &f_opers, 0); 
  res->add_const("result", std::string("no problem")); 

  return ;
}
extern "C"
{
  fso* create(void)
  {
    return (new fuse(string("fuse")));
  }
  void destroy(fso *p)
  {
    delete p;
  }

  class proxy 
  {
    public :
    proxy()
    {
     CModule* cmod = new CModule("fuse", create);
     cmod->conf->add("path", "path");
     cmod->tags = "fs";
    }
  };
  proxy p;
}
