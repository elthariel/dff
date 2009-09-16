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
add_custom_target(patchexceptions ALL
  COMMENT "Patching libexceptions.py"
  COMMAND python patch.py 
)
set(exceptions_srcs
  __init__.py
   libexceptions.py
)

install_lib(${SWIG_MODULE_libexceptions_REAL_NAME})
install_file(exceptions ${exceptions_srcs})
