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
#  Solal Jacob <sja@digital-forensic.org>


#### Deploying python __init__ script
set(itemview_srcs
__init__.py
listmodel.py
listthread.py
listview.py
nodeitem.py
rootitemmodel.py
selectnodeslistview.py
selectnodesmodel.py
thumbsitemmodel.py
thumbsthread.py
thumbsview.py
treeitemmodel.py
treeview.py
)

install_file(itemview ${itemview_srcs})
