add_subdirectory(listFolder)
add_subdirectory(treeDir)

set(vfsGui_srcs
  __init__.py
  _propertyDialog.py
  propertyDialog.py
)

install_file(vfsGui ${vfsGui_srcs})
