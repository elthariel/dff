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


FIND_PACKAGE(SWIG REQUIRED)
INCLUDE(${SWIG_USE_FILE})

include_directories(${PYTHON_INCLUDE_PATH})

include_directories(${CMAKE_CURRENT_SOURCE_DIR})
include_directories(${CMAKE_HOME_DIRECTORY}/api/include)


set(fat_srcs
  fat.cpp
  misc.cpp
  fat_metadata.cpp
  fat_forensics.cpp
  fat_entries.cpp
  fat_io.cpp
  log.cpp
  filehandler.cpp
  fdmanager.cpp
)


SET_SOURCE_FILES_PROPERTIES(fat.i PROPERTIES CPLUSPLUS ON)
SWIG_ADD_MODULE(FAT python fat.i ${fat_srcs})
SWIG_LINK_LIBRARIES(FAT ${PYTHON_LIBRARIES} _libexceptions _libtype _libvfs _libenv)

if ( CMAKE_GENERATOR MATCHES "Visual Studio")
set_target_properties (${SWIG_MODULE_FAT_REAL_NAME} PROPERTIES
  PREFIX "../"
  SUFFIX ".pyd"
)
endif ( CMAKE_GENERATOR MATCHES "Visual Studio")

set(fat_files
  FAT.py
)

install_lib(${SWIG_MODULE_FAT_REAL_NAME})
install_file(fat ${fat_files})
