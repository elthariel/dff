# compiled
add_subdirectory (exceptions)
add_subdirectory (env)
add_subdirectory (loader)
add_subdirectory (module)
add_subdirectory (type)
add_subdirectory (vfs)
# python only
add_subdirectory (taskmanager)
add_subdirectory (magic)

#### Deploying python __init__ script
set(api_srcs
  __init__.py
)

install_file(api ${api_srcs})
