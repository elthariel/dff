set(widget_srcs
  __init__.py
  info.py
  interpreter.py
  shell.py
  stdio.py
)

install_file(widget ${widget_srcs})
