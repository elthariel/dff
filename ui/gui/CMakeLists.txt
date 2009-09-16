add_subdirectory(configuration)
add_subdirectory(i18n)
#add_subdirectory(icons)
add_subdirectory(ide)
add_subdirectory(scheduler)
add_subdirectory(utils)
add_subdirectory(vfs)
add_subdirectory(widget)
add_subdirectory(wrapper)

set(gui_srcs
  __init__.py
  _mainWindow.py
  gui.py
  gui_rc.py
  mainWindow.py
)

install_file(gui ${gui_srcs})
