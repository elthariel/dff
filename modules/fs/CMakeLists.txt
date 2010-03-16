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
#  Frederic Baguelin <fba@digital-forensic.org>
#  Solal Jacob <sja@digital-forensic.org>


add_subdirectory (local)
add_subdirectory (fat)
add_subdirectory (carver)
add_subdirectory (shm)
#if(HAVE_FUSE)
#  add_subdirectory (fuse)
#endif(HAVE_FUSE)
add_subdirectory (partition)

set(fs_srcs
  __init__.py
  mzipfile.py
  streamstrings.py
  unzip.py
)

install_file(fs ${fs_srcs})
