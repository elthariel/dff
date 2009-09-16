set(hexedit_srcs
  __init__.py
  GView.py
  Heditor.py
  Navigation.py
  NavigationValues.py
  find_not_aligned_thread.py
  hexeditor.py
  itemText.py
  nceditor.py
  test.py
)

install_file(hexedit ${hexedit_srcs})
