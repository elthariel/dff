add_subdirectory (local)
add_subdirectory (shm)
add_subdirectory (fat)
if(HAVE_FUSE)
  add_subdirectory (fuse)
endif(HAVE_FUSE)
add_subdirectory (partition)

set(fs_srcs
  __init__.py
  mzipfile.py
  streamstrings.py
  unzip.py
)

install_file(fs ${fs_srcs})
