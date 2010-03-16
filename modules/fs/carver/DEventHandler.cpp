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

#include "DEventHandler.hpp"

DEventHandler::DEventHandler()
{
}

bool    DEventHandler::connection(class DEventHandler *obs)
{
  vector<class DEventHandler *>::iterator        it;

  for (it = this->watchers.begin(); it != this->watchers.end(); it++)
    if (*it == obs)
      {
        cout << "already registered" << endl;
        return false;
      }
  this->watchers.push_back(obs);
  return true;
}

bool    DEventHandler::deconnection(class DEventHandler *obs)
{
  vector<class DEventHandler *>::iterator        it;

  for (it = this->watchers.begin(); it != this->watchers.end(), *it != obs; it++)
    ;
  if (it != this->watchers.end())
    {
      this->watchers.erase(it);
      return true;
    }
  else
    return false;
}

bool    DEventHandler::notify(DEvent *e)
{
  vector<class DEventHandler *>::iterator        it;

  for (it = this->watchers.begin(); it != this->watchers.end(); it++)
    (*it)->Event(e);
  return true;
  delete e;
}
