add_subdirectory(gif)
add_subdirectory(jpeg)
add_subdirectory(pdf)

set(carving_srcs
  __init__.py
  carver.py
)

install_file(carving ${carving_srcs})
