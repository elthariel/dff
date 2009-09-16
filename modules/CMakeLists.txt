add_subdirectory (builtins)
add_subdirectory (fs) 
add_subdirectory (info)
add_subdirectory (parser)
add_subdirectory (process)
add_subdirectory (search)
add_subdirectory (viewer)
add_subdirectory (help)
add_subdirectory (test)

set(module_srcs
  __init__.py
)

install_file(module2 ${module_srcs})
