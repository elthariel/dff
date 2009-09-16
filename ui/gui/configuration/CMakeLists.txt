set(configuration_srcs
  Config.py
  __init__.py
  configureDFF.py
  Translator.py
  _configureDFF.py
)

install_file(configuration ${configuration_srcs})
