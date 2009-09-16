if (UNIX)
set(magic_srcs
  __init__.py
  filetype.py
  magic
  magic.mime
  magic.so
  magic_64b.so
)
else(UNIX)
set(magic_srcs
  __init__.py
  filetype.py
  magic
  magic.mime
  magic1.dll
  magic.pyd
  zlib1.dll
  regex2.dll
)  
endif(UNIX)

install_file(magic ${magic_srcs})
