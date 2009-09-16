FIND_PACKAGE(SWIG REQUIRED)
INCLUDE(${SWIG_USE_FILE})

#FIND_PACKAGE(PythonLibs)

INCLUDE_DIRECTORIES(${PYTHON_INCLUDE_PATH})
INCLUDE_DIRECTORIES(${CMAKE_CURRENT_SOURCE_DIR})
INCLUDE_DIRECTORIES(../include)

SET_SOURCE_FILES_PROPERTIES(libloader.i PROPERTIES CPLUSPLUS ON)
SWIG_ADD_MODULE(libloader python libloader.i loader.cpp)
SWIG_LINK_LIBRARIES(libloader ${PYTHON_LIBRARIES})
if ( CMAKE_GENERATOR MATCHES "Visual Studio")
set_target_properties (${SWIG_MODULE_libloader_REAL_NAME} PROPERTIES
  PREFIX "../"
  SUFFIX ".pyd"
)
endif ( CMAKE_GENERATOR MATCHES "Visual Studio")
set(loader_srcs
  __init__.py
  loader.py
  libloader.py
)

install_lib(${SWIG_MODULE_libloader_REAL_NAME})
install_file(loader ${loader_srcs})

