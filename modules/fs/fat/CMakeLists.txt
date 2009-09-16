include_directories(${CMAKE_CURRENT_SOURCE_DIR})
include_directories(${CMAKE_HOME_DIRECTORY}/api/include)

set(fat_srcs
  fat.cpp
  misc.cpp
  fat_metadata.cpp
  fat_forensics.cpp
  fat_entries.cpp
  fat_io.cpp
  log.cpp
  filehandler.cpp
)

add_library(fat SHARED ${fat_srcs})

if(UNIX)
  target_link_libraries(fat _libloader)
else(UNIX)
  target_link_libraries(fat _libloader _libcmodule _libenv _libexceptions _libtype _libvfs)
endif(UNIX)


set_target_properties(fat PROPERTIES
  LIBRARY_OUTPUT_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/
  SUFFIX ".mod"
)
if ( CMAKE_GENERATOR MATCHES "Visual Studio")
set_target_properties (fat PROPERTIES
  PREFIX "../" 
)
endif ( CMAKE_GENERATOR MATCHES "Visual Studio")

install_lib(fat)
