set(taskmanager_srcs
  __init__.py
  processus.py
  scheduler.py
  taskmanager.py
)

install_file(taskmanager ${taskmanager_srcs})
