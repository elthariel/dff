include_directories(${CMAKE_CURRENT_SOURCE_DIR})
include_directories(${CMAKE_HOME_DIRECTORY}/api/include)

if (UNIX)
set(local_srcs
  ulocal.cpp
  utype.cpp
)
else (UNIX)
set(local_srcs
  wlocal.cpp
  wtype.cpp
)
else (UNIX)
endif(UNIX)

add_library(local SHARED ${local_srcs})

if (UNIX)
  target_link_libraries(local _libloader _libtype)
else (UNIX)
  target_link_libraries(local _libloader _libcmodule _libenv _libexceptions _libtype _libvfs)
endif(UNIX)

set_target_properties(local PROPERTIES
  LIBRARY_OUTPUT_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/
  SUFFIX ".mod"
)
if ( CMAKE_GENERATOR MATCHES "Visual Studio")
set_target_properties (local PROPERTIES
  PREFIX "../" 
)
endif ( CMAKE_GENERATOR MATCHES "Visual Studio")

install_lib(local)
