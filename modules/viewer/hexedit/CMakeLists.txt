# DFF -- An Open Source Digital Forensics Framework
# Copyright (C) 2009-2010 ArxSys
# This program is free software, distributed under the terms of
# the GNU General Public License Version 2. See the LICENSE file
# at the top of the source tree.
#  
# See http://www.digital-forensic.org for more information about this
# project. Please do not directly contact any of the maintainers of
# DFF for assistance; the project provides a web site, mailing lists
# and IRC channels for your use.
# 
# Author(s):
#  Jeremy Mounier <jmo@digital-forensic.org>


set(hexedit_srcs
  asciiItem.py
  bookmark.py
  cursors.py
  decodeValues.py
  footer.py
  goto.py
  Heditor.py
  hexeditor.py
  hexItem.py
  hexView.py
  informations.py
  __init__.py
  navigation.py
  nceditor.py
  offsetItem.py
  options.py
  right.py
  scrollbar.py
  search.py
  selection.py
  textItem.py
  utils.py
)

install_file(hexedit ${hexedit_srcs})
