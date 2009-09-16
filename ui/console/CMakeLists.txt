set(console_srcs
  __init__.py
  complete_raw_input.py
  completion.py
  console.py
  line_to_arguments.py
  utils.py
)

install_file(console ${console_srcs})
