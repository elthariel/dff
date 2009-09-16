add_subdirectory(hexedit)

set(viewer_srcs
  cat.py
#  player.py
  viewerimage.py
)

install_file(viewer ${viewer_srcs})
