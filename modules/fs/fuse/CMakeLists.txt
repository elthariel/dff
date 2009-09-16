include_directories(${CMAKE_CURRENT_SOURCE_DIR})
include_directories(${CMAKE_HOME_DIRECTORY}/api/include)
include_directories(/usr/include/fuse)

set(fusemod_srcs
  fuse.cpp
  ../local/utype.cpp
)

add_library(fusemod SHARED ${fusemod_srcs})

if (UNIX)
  target_link_libraries(fusemod _libloader pthread fuse rt dl)
else (UNIX)
  target_link_libraries(fusemod _libloader _libcmodule _libenv _libexceptions _libtype _libvfs)
endif(UNIX)

set_target_properties(fusemod PROPERTIES
  LIBRARY_OUTPUT_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/
  SUFFIX ".mod"
  #OUTPUT_NAME fuse.mod
)
if ( CMAKE_GENERATOR MATCHES "Visual Studio")
set_target_properties (fusemod PROPERTIES
  PREFIX "../" 
)
endif ( CMAKE_GENERATOR MATCHES "Visual Studio")

install_lib(fusemod)
