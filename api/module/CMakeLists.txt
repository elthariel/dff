FIND_PACKAGE(SWIG REQUIRED)
INCLUDE(${SWIG_USE_FILE})

#FIND_PACKAGE(PythonLibs)

INCLUDE_DIRECTORIES(${PYTHON_INCLUDE_PATH})
INCLUDE_DIRECTORIES(${CMAKE_CURRENT_SOURCE_DIR})
INCLUDE_DIRECTORIES(../include)

SET_SOURCE_FILES_PROPERTIES(libcmodule.i PROPERTIES CPLUSPLUS ON)
SWIG_ADD_MODULE(libcmodule python libcmodule.i cmodule.cpp fdmanager.cpp)
if (UNIX)
SWIG_LINK_LIBRARIES(libcmodule ${PYTHON_LIBRARIES} _libexceptions _libenv _libtype _libvfs _libloader)
else(UNIX)
SWIG_LINK_LIBRARIES(libcmodule ${PYTHON_LIBRARIES} _libenv _libloader)
endif(UNIX)
if ( CMAKE_GENERATOR MATCHES "Visual Studio")
set_target_properties (${SWIG_MODULE_libcmodule_REAL_NAME} PROPERTIES
  PREFIX "../"
  SUFFIX ".pyd"
)
endif ( CMAKE_GENERATOR MATCHES "Visual Studio")
set(module_srcs
  __init__.py
  module.py
  script.py
  libcmodule.py
)

install_lib(${SWIG_MODULE_libcmodule_REAL_NAME})
install_file(module ${module_srcs})
