FIND_PACKAGE(SWIG REQUIRED)
INCLUDE(${SWIG_USE_FILE})

#FIND_PACKAGE(PythonLibs)

INCLUDE_DIRECTORIES(${PYTHON_INCLUDE_PATH})
INCLUDE_DIRECTORIES(${CMAKE_CURRENT_SOURCE_DIR})
INCLUDE_DIRECTORIES(../include)

SET_SOURCE_FILES_PROPERTIES(libtype.i PROPERTIES CPLUSPLUS ON)
SWIG_ADD_MODULE(libtype python libtype.i type.cpp vtime.cpp attrib.cpp)
SWIG_LINK_LIBRARIES(libtype ${PYTHON_LIBRARIES})
if ( CMAKE_GENERATOR MATCHES "Visual Studio")
set_target_properties (${SWIG_MODULE_libtype_REAL_NAME} PROPERTIES
  PREFIX "../"
  SUFFIX ".pyd"
)
endif ( CMAKE_GENERATOR MATCHES "Visual Studio")
set(type_srcs
  __init__.py
  libtype.py
)

install_file(type ${type_srcs})
install_lib(${SWIG_MODULE_libtype_REAL_NAME})
