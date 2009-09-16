# DFF -- An Open Source Digital Forensics Framework
# Copyright (C) 2009 ArxSys
# 
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
#  Christophe Malinge <cma@digital-forensic.org>
#  Solal J. <sja@digital-forensic.org>

project (dff)

#### Basic Cmake definitions
cmake_minimum_required (VERSION 2.6)
set(CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/cmake_modules/")


#### Project-wide requirements

option(ENABLE_DEBUG "Compile using -g flag ? Useful for debugging" OFF)
if(UNIX)
  if(ENABLE_DEBUG)
    add_definitions(-D_FILE_OFFSET_BITS=64 -D_LARGEFILE64_SOURCE)
    message(STATUS "Will use -g for debugging -- no")
  else(ENABLE_DEBUG)
    add_definitions(-D_FILE_OFFSET_BITS=64 -D_LARGEFILE64_SOURCE -O2) 
    message(STATUS "Will use -g for debugging -- yes")
  endif(ENABLE_DEBUG)
endif(UNIX)
# $> cmake -DENABLE_DEBUG:BOOLEAN=OFF


## Swig

find_package(SWIG REQUIRED)
include(${SWIG_USE_FILE})
# Project-wide swig options
#SET(CMAKE_SWIG_FLAGS "-py3")

option(DISABLE_SWIG_THREADING "Wrap cpp code to python without -threads" OFF)
if(DISABLE_SWIG_THREADING)
  message(STATUS "Will we use swig -threads -- no")
else()
  message(STATUS "Will we use swig -threads -- yes")
  set(CMAKE_SWIG_FLAGS -threads)
endif(DISABLE_SWIG_THREADING)
# $> cmake -DDISABLE_SWIG_THREADING:BOOLEAN=ON

find_library(HAVE_FUSE NAMES fuse)
if(NOT HAVE_FUSE)
  message(STATUS "fuse library not found; file system module 'fuse' will not be built")
endif(NOT HAVE_FUSE)


## Python


execute_process ( COMMAND python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()" OUTPUT_VARIABLE PYTHON_SITE_PACKAGES_PATH OUTPUT_STRIP_TRAILING_WHITESPACE)
execute_process ( COMMAND python -c "from distutils.sysconfig import get_python_version; print get_python_version()" OUTPUT_VARIABLE PYTHON_VERSION OUTPUT_STRIP_TRAILING_WHITESPACE)
if (UNIX)
execute_process ( COMMAND  python -c "from distutils.sysconfig import get_config_vars; print get_config_vars()[\"LIBDIR\"] + \"/\" + get_config_vars()[\"LDLIBRARY\"]" OUTPUT_VARIABLE PYTHON_LIBRARIES OUTPUT_STRIP_TRAILING_WHITESPACE)
execute_process ( COMMAND  python -c "from distutils.sysconfig import get_python_inc; print get_python_inc()" OUTPUT_VARIABLE PYTHON_INCLUDE_PATH OUTPUT_STRIP_TRAILING_WHITESPACE)
else (UNIX)
find_package(PythonLibs)
find_package(PythonInterp)
endif(UNIX)


SET(CMAKE_INSTALL_PREFIX ${PYTHON_SITE_PACKAGES_PATH}/${CMAKE_PROJECT_NAME}/)

## Macro to copy files at install
macro(install_file target_name)
  foreach(file ${ARGN})
  add_custom_target("${target_name}.${file}" ALL)
  FILE(RELATIVE_PATH rel ${CMAKE_BINARY_DIR} ${CMAKE_CURRENT_BINARY_DIR})
  install(FILES ${file}
 	  DESTINATION ${PYTHON_SITE_PACKAGES_PATH}/${CMAKE_PROJECT_NAME}/${rel}
	)
  endforeach(file ${ARGN}) 
endmacro(install_file target_name)

## Macro to copy lib at install
macro(install_lib target_name)
  FILE(RELATIVE_PATH rel ${CMAKE_BINARY_DIR} ${CMAKE_CURRENT_BINARY_DIR})
  INSTALL (TARGETS ${target_name} DESTINATION ${PYTHON_SITE_PACKAGES_PATH}/${CMAKE_PROJECT_NAME}/${rel})
endmacro(install_lib)

#### Deploying package file and DFF startup files
if (UNIX)
set(dff_scripts
  __init__.py
  dff.py
  dff-gui.py
)
else(UNIX)
set(dff_scripts
  __init__.py
  dff.py
  dff-gui.py
  dff.ico	  
)
else(UNIX)
endif(UNIX)

install_file(dff_launch ${dff_scripts})

# Create launcher. Replace CMake variables in it, used after install.
configure_file(${CMAKE_CURRENT_SOURCE_DIR}/launcher.sh ${CMAKE_CURRENT_BINARY_DIR}/dff)

#### Subdirectories to recurse
add_subdirectory (api)
add_subdirectory (modules)
add_subdirectory (ui)

SET(CPACK_SET_DESTDIR "ON")
#### Project install

SET(CPACK_PACKAGE_DESCRIPTION_SUMMARY "Digital Forensic Framework")
SET(CPACK_PACKAGE_VENDOR "ArxSys")
SET(CPACK_PACKAGE_DESCRIPTION_FILE "${CMAKE_CURRENT_SOURCE_DIR}/ressources/ReadMe.txt")
SET(CPACK_RESOURCE_FILE_LICENSE "${CMAKE_CURRENT_SOURCE_DIR}/ressources/Copyright.txt")
SET(CPACK_PACKAGE_VERSION_MAJOR "0") 
SET(CPACK_PACKAGE_VERSION_MINOR "4")
SET(CPACK_PACKAGE_VERSION_PATCH "2")
SET(CPACK_PACKAGE_INSTALL_DIRECTORY "DFF")
IF(WIN32 AND NOT UNIX)
  SET(CPACK_PACKAGE_ICON "${CMAKE_CURRENT_SOURCE_DIR}\\\\ressources\\\\arxsys.bmp")
  SET(CPACK_BUNDLE_ICON "${CMAKE_CURRENT_SOURCE_DIR}\\\\ressources\\\\arxsys.bmp")
  SET(CPACK_NSIS_MUI_ICON "${CMAKE_CURRENT_SOURCE_DIR}\\\\ressources\\\\dff.ico")
  SET(CPACK_NSIS_MUI_NUIICON "${CMAKE_CURRENT_SOURCE_DIR}\\\\ressources\\\\dff.ico")
  SET(CPACK_NSIS_DISPLAY_NAME "Digital Forensic Framework")
  SET(CPACK_NSIS_HELP_LINK "http:\\\\\\\\www.digital-forensic.org")
  SET(CPACK_NSIS_URL_INFO_ABOUT "http:\\\\\\\\www.arxsys.fr")
  SET(CPACK_NSIS_CONTACT "contact@arxsys.fr")
  SET(CPACK_NSIS_MODIFY_PATH OFF)
  SET(CPACK_NSIS_COMPRESSOR "/SOLID lzma")
  SET(CPACK_GENERATOR "NSIS")
  SET(CPACK_NSIS_EXTRA_INSTALL_COMMANDS
 "
 SetOutPath \\\"$INSTDIR\\\\dff\\\"
 CreateShortCut \\\"$DESKTOP\\\\dff (shell).lnk\\\" \\\"$INSTDIR\\\\dff\\\\dff.py\\\" \\\"\\\" \\\"$INSTDIR\\\\dff\\\\ressources\\\\dff.ico\\\" 
 CreateShortCut \\\"$DESKTOP\\\\dff (gui).lnk\\\" \\\"$INSTDIR\\\\dff\\\\dff-gui.py\\\" \\\"\\\" \\\"$INSTDIR\\\\dff\\\\ressources\\\\dff.ico\\\"  
 CreateShortCut \\\"$SMPROGRAMS\\\\DFF\\\\dff (shell).lnk\\\" \\\"$INSTDIR\\\\dff\\\\dff.py\\\" \\\"\\\" \\\"$INSTDIR\\\\dff\\\\ressources\\\\dff.ico\\\"  
 CreateShortCut \\\"$SMPROGRAMS\\\\DFF\\\\dff (gui).lnk\\\" \\\"$INSTDIR\\\\dff\\\\dff-gui.py\\\" \\\"\\\" \\\"$INSTDIR\\\\dff\\\\ressources\\\\dff.ico\\\"  
 ")
  SET(CPACK_SOURCE_GENERATOR "ZIP")
ELSE(WIN32 AND NOT UNIX)
  SET(CPACK_SOURCE_GENERATOR "TGZ")
#  SET(CPACK_SOURCE_IGNORE_FILES "") 
  SET(CPACK_GENERATOR "DEB" "RPM")
ENDIF(WIN32 AND NOT UNIX)

#debian specific
SET(CPACK_DEBIAN_PACKAGE_MAINTAINER "Malinge Christophe packaging@digital-forensic.org")
execute_process ( COMMAND uname -m  OUTPUT_VARIABLE CURRENT_ARCH OUTPUT_STRIP_TRAILING_WHITESPACE)
#SET(CPACK_DEBIAN_PACKAGE_ARCHITECTURE "${CURRENT_ARCH}")
SET(CPACK_DEBIAN_PACKAGE_ARCHITECTURE "i386")
SET(CPACK_DEBIAN_PACKAGE_DEPENDS "python${PYTHON_VERSION} (>= ${PYTHON_VERSION}.0), python-qt4 (>= 4.4.0), python-qscintilla2 (>= 2.0), libfuse2 (>= 2.7.0)")
SET(CPACK_DEBIAN_PACKAGE_SECTION "utils")

#rpm specific
SET(CPACK_RPM_PACKAGE_ARCHITECTURE "${CURRENT_ARCH}")
SET(CPACK_RPM_PACKAGE_GROUP "Applications/System")
SET(CPACK_RPM_PACKAGE_LICENSE "GPLV2")
SET(CPACK_RPM_PACKAGE_REQUIRES "python${PYTHON_VERSION} >= ${PYTHON_VERSION}.0 , python-qt4 >= 4.4.0 , python-qscintilla2 >= 2.0 , libfuse2 >= 2.7.0")
include(CPack)

install(FILES ${CMAKE_CURRENT_BINARY_DIR}/dff.py
  DESTINATION ${PYTHON_SITE_PACKAGES_PATH}/${CMAKE_PROJECT_NAME}
  PERMISSIONS OWNER_READ OWNER_WRITE OWNER_EXECUTE GROUP_READ GROUP_EXECUTE WORLD_READ WORLD_EXECUTE)

if (UNIX)
  install(FILES ${CMAKE_CURRENT_BINARY_DIR}/dff
  DESTINATION /usr/bin
  PERMISSIONS OWNER_READ OWNER_WRITE OWNER_EXECUTE GROUP_READ GROUP_EXECUTE WORLD_READ WORLD_EXECUTE)
  install(FILES ${CMAKE_CURRENT_BINARY_DIR}/ressources/dff.png ${CMAKE_CURRENT_BINARY_DIR}/ressources/dff.xpm
  DESTINATION /usr/share/pixmaps
  PERMISSIONS OWNER_READ OWNER_WRITE GROUP_READ WORLD_READ)
  install(FILES ${CMAKE_CURRENT_BINARY_DIR}/ressources/dff.desktop
  DESTINATION /usr/share/applications
  PERMISSIONS OWNER_READ OWNER_WRITE GROUP_READ WORLD_READ)
endif(UNIX)
