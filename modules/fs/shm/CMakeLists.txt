include_directories(${CMAKE_CURRENT_SOURCE_DIR})
include_directories(${CMAKE_HOME_DIRECTORY}/api/include)

set(shm_srcs
  shm.cpp
)

add_library(shm SHARED ${shm_srcs})

if (UNIX)
  target_link_libraries(shm _libloader)
else (UNIX)
  target_link_libraries(shm _libloader _libcmodule _libenv _libexceptions _libtype _libvfs)
endif(UNIX)

set_target_properties(shm PROPERTIES
  LIBRARY_OUTPUT_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/
  SUFFIX ".mod"
)
if ( CMAKE_GENERATOR MATCHES "Visual Studio")
set_target_properties (shm PROPERTIES
  PREFIX "../" 
)
endif ( CMAKE_GENERATOR MATCHES "Visual Studio")
set(shm_srcs
  __init__.py
  touch.py
)

install_file(shm ${shm_srcs})
install_lib(shm)
