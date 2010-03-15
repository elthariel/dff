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
#  Christophe Malinge <cma@digital-forensic.org>


# We create ADD_PYTHON_DOCTEST because we have to set PYTHONPATH environement
#  variable, because CTest/CMake don't care about env var using standard
#  ADD_TEST.
MACRO(ADD_PYTHON_DOCTEST TESTNAME FILENAME)
  GET_SOURCE_FILE_PROPERTY(loc ${FILENAME} LOCATION)
  STRING(REGEX REPLACE ";" " " wo_semicolumn "${ARGN}")
  FILE(WRITE ${CMAKE_CURRENT_BINARY_DIR}/${TESTNAME}.cmake
"
  SET(ENV{PYTHONPATH} ${PROJECT_SOURCE_DIR})
  EXECUTE_PROCESS(
  	COMMAND python -m doctest ${loc} ${wo_semicolumn}
  	#WORKING_DIRECTORY @LIBRARY_OUTPUT_PATH@
  	RESULT_VARIABLE import_res
  	OUTPUT_VARIABLE import_output
  	ERROR_VARIABLE  import_output
  )
  
  # Pass the output back to ctest
  MESSAGE(STATUS "\${import_output}")
  IF(import_res)
    MESSAGE(SEND_ERROR "\${import_res}")
  ENDIF(import_res)
"
)
  ADD_TEST(${TESTNAME} cmake -P ${CMAKE_CURRENT_BINARY_DIR}/${TESTNAME}.cmake)
ENDMACRO(ADD_PYTHON_DOCTEST)


# doctest
ADD_PYTHON_DOCTEST(modules.viewer.plot.DffDatetime dffdatetime.txt)


# unittest
ADD_TEST(modules.fs.local python local.py)
ADD_TEST(modules.parser.hash python hashtest.py)
ADD_TEST(modules.fs.fat python fattest.py)
ADD_TEST(modules.api.env.error python enverrortest.py)
ADD_TEST(modules.api.vfs.error python vfserrortest.py)
