#add_subdirectory(carving)
add_subdirectory(hash)

set(parser_srcs
  smsdecode.py
  unxor.py
)

install_file(parser ${parser_srcs})
