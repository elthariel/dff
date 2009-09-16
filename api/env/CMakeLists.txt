FIND_PACKAGE(SWIG REQUIRED)
INCLUDE(${SWIG_USE_FILE})

#FIND_PACKAGE(PythonLibs)

INCLUDE_DIRECTORIES(${PYTHON_INCLUDE_PATH})
INCLUDE_DIRECTORIES(${CMAKE_CURRENT_SOURCE_DIR})
INCLUDE_DIRECTORIES(../include)

SET_SOURCE_FILES_PROPERTIES(libenv.i PROPERTIES CPLUSPLUS ON)
SWIG_ADD_MODULE(libenv python libenv.i env.cpp conf.cpp argument.cpp results.cpp vars.cpp)
SWIG_LINK_LIBRARIES(libenv ${PYTHON_LIBRARIES} _libexceptions)

if ( CMAKE_GENERATOR MATCHES "Visual Studio")
set_target_properties (${SWIG_MODULE_libenv_REAL_NAME} PROPERTIES
  PREFIX "../"
  SUFFIX ".pyd"
)
endif ( CMAKE_GENERATOR MATCHES "Visual Studio")

set(env_srcs
  __init__.py
  env.py
  libenv.py
)
install_lib(${SWIG_MODULE_libenv_REAL_NAME})
install_file(env ${env_srcs})
