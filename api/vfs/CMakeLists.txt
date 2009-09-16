FIND_PACKAGE(SWIG REQUIRED)
INCLUDE(${SWIG_USE_FILE})

#FIND_PACKAGE(PythonLibs)

INCLUDE_DIRECTORIES(${PYTHON_INCLUDE_PATH})
INCLUDE_DIRECTORIES(${CMAKE_CURRENT_SOURCE_DIR})
INCLUDE_DIRECTORIES(../include)

SET_SOURCE_FILES_PROPERTIES(libvfs.i PROPERTIES CPLUSPLUS ON)
SWIG_ADD_MODULE(libvfs python libvfs.i fso.cpp node.cpp vfile.cpp vfs.cpp)
SWIG_LINK_LIBRARIES(libvfs ${PYTHON_LIBRARIES} _libexceptions _libtype)
if ( CMAKE_GENERATOR MATCHES "Visual Studio")
set_target_properties (${SWIG_MODULE_libvfs_REAL_NAME} PROPERTIES
  PREFIX "../"
  SUFFIX ".pyd"
)
endif ( CMAKE_GENERATOR MATCHES "Visual Studio")
set(vfs_srcs
  vfs.py
  __init__.py
  libvfs.py
)

install_lib(${SWIG_MODULE_libvfs_REAL_NAME})
install_file(vfs ${vfs_srcs})
