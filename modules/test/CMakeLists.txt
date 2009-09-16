if (UNIX)
  add_subdirectory(loadtest)
endif(UNIX)

set(test_srcs
  statest.py
)

install_file(test ${test_srcs})
