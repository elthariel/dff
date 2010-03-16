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


#ifndef __CARVER_HPP__
#define __CARVER_HPP__

#include "common.hpp"
#include "filehandler.hpp"
#include "fdmanager.hpp"
#include "DEventHandler.hpp"

//Let the possibility to modify the matching footer or to dynamically set the window
//representing the carved file.

class Carver: public fso, public DEventHandler
{
private:
  Node			*inode;
  Node			*root;
  VFile			*ifile;
  FileHandler		*filehandler;
  fdmanager		*fdm;
  BoyerMoore		*bm;
  vector<context*>	ctx;
  unsigned int		maxNeedle;
  bool			aligned;
  bool			stop;
  string		Results;

  bool			createFile();
  void			registerNode(Node *parent, dff_ui64 start, dff_ui64 end);
  unsigned int		createWithoutFooter(Node *parent, vector<dff_ui64> *headers, unsigned int max);
  unsigned int		createWithFooter(Node *parent, vector<dff_ui64> *headers, vector<dff_ui64> *footers, unsigned int max);
  int			createNodes();
  void			mapper();

public:
  Carver();
  ~Carver();
  dff_ui64		tell();
  EXPORT string		process(list<description *> *d, dff_ui64 start, bool aligned);
  virtual void          start(argument *arg);
  virtual int		vopen(Handle *handle);
  virtual int		vread(int fd, void *buff, unsigned int size);
  virtual int		vclose(int fd);
  virtual dff_ui64	vseek(int fd, dff_ui64 offset, int whence);
  virtual int		vwrite(int fd, void *buff, unsigned int size){return 0;};
  virtual unsigned int	status();
  virtual void		Event(DEvent *e);
  int			Read(char *buffer, unsigned int size);
};

#endif
