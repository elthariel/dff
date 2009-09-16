include_directories(${CMAKE_CURRENT_SOURCE_DIR})
include_directories(${CMAKE_HOME_DIRECTORY}/api/include)

set(partition_srcs
  partition.cpp
)

add_library(partition SHARED ${partition_srcs})

if (UNIX)
  target_link_libraries(partition _libloader _libtype)
else (UNIX)
  target_link_libraries(partition _libloader _libcmodule _libenv _libexceptions _libtype _libvfs)
endif(UNIX)

set_target_properties(partition PROPERTIES
  LIBRARY_OUTPUT_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/
  SUFFIX ".mod"
)
if ( CMAKE_GENERATOR MATCHES "Visual Studio")
set_target_properties (partition PROPERTIES
  PREFIX "../" 
)
endif ( CMAKE_GENERATOR MATCHES "Visual Studio")

install_lib(partition)
