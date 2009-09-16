#add_subdirectory (cls)

set(builtins_srcs
  cd.py
  fg.py
  history.py
  info.py
  jobs.py
  load.py
  ls.py
#  rm.py
  show_cwd.py
  show_db.py
)

install_file(builtins ${builtins_srcs})
