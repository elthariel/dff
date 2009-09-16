#if (UNIX)
#add_subdirectory(cextract)
#endif(UNIX)

set(process_srcs
  batch.py
  evalexp.py
  extract.py
#  pipe_exec.py
  post_process.py
)

install_file(process ${process_srcs})
