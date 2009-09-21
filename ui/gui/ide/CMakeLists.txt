set(ide_srcs
  DFF_Editor.py
  DFF_Ide.py
  Ide.py
  __init__.py
  generateCode.py
  messageBox.py
  toolBar.py
  ideWizard.py
  ideWizardPages.py
)

install_file(ide ${ide_srcs})
