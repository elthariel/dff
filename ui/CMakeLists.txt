add_subdirectory(console)
add_subdirectory(gui)

set(ui_srcs
  __init__.py
  history.py
  redirect.py
)

install_file(ui ${ui_srcs})
