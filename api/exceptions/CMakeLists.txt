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


FIND_PACKAGE(SWIG REQUIRED)
INCLUDE(${SWIG_USE_FILE})

#FIND_PACKAGE(PythonLibs)
#FIND_PACKAGE(PythonInterp)
INCLUDE_DIRECTORIES(${PYTHON_INCLUDE_PATH})
INCLUDE_DIRECTORIES(${CMAKE_CURRENT_SOURCE_DIR})
INCLUDE_DIRECTORIES(../include)

SET_SOURCE_FILES_PROPERTIES(libexceptions.i PROPERTIES CPLUSPLUS ON)
SWIG_ADD_MODULE(libexceptions python libexceptions.i exceptions.cpp)
SWIG_LINK_LIBRARIES(libexceptions ${PYTHON_LIBRARIES})
if ( CMAKE_GENERATOR MATCHES "Visual Studio")
set_target_properties (${SWIG_MODULE_libexceptions_REAL_NAME} PROPERTIES
  PREFIX "../"
  SUFFIX ".pyd"
)
endif ( CMAKE_GENERATOR MATCHES "Visual Studio")
if (UNIX)
add_custom_target(patchexceptions ALL
  COMMENT "Patching libexceptions.py"
  COMMAND python ${CMAKE_CURRENT_SOURCE_DIR}/patch.py
    ${CMAKE_CURRENT_BINARY_DIR}/libexceptions.py
)
elseif(UNIX)
add_custom_target(patchexceptions ALL
  COMMENT "Patching libexceptions.py"
  COMMAND ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/patch.py
    ${CMAKE_CURRENT_BINARY_DIR}/libexceptions.py
)
endif(UNIX)
set(exceptions_srcs
  __init__.py
   libexceptions.py
)

install_lib(${SWIG_MODULE_libexceptions_REAL_NAME})
install_file(exceptions ${exceptions_srcs})
