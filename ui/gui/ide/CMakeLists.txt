set(ide_srcs
  DFF_Editor.py
  DFF_Ide.py
  Ide.py
  __init__.py
  dialog.py
  generateCode.py
  messageBox.py
  toolBar.py
)

install_file(ide ${ide_srcs})
