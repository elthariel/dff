# DFF -- An Open Source Digital Forensics Framework
# Copyright (C) 2009-2010 ArxSys
# This program is free software, distributed under the terms of
# the GNU General Public License Version 2. See the LICENSE file
# at the top of the source tree.
#  
# See http://www.digital-forensic.org for more information about this
# project. Please do not directly contact any of the maintainers of
# DFF for assistance; the project provides a web site, mailing lists
# and IRC channels for your use.
# 
# Author(s):
#  Christophe Malinge <cma@digital-forensic.org>
#  Frederic Baguelin <fba@digital-forensic.org>
#  Solal Jacob <sja@digital-forensic.org>


if (UNIX AND NOT WIN32)
  set(magic_srcs
    __init__.py
    filetype.py
    )
endif(UNIX AND NOT WIN32)

if(WIN32 AND NOT UNIX)
  ADD_CUSTOM_TARGET(magicBin ALL
      COMMENT "copying magic binaries for win"
      COMMAND ${CMAKE_COMMAND} -E copy magic.mgc.win magic.mgc
      )
  if( HAVE_64_BIT )
    ADD_CUSTOM_TARGET(magicDll ALL
      COMMENT "copying magic librairies for win64"
      COMMAND ${CMAKE_COMMAND} -E copy magic1.dll.win64 magic1.dll
      COMMAND ${CMAKE_COMMAND} -E copy zlib1.dll.win64 zlib1.dll
      COMMAND ${CMAKE_COMMAND} -E copy regex2.dll.win64 regex2.dll
      )
  else( HAVE_64_BIT )
    ADD_CUSTOM_TARGET(magicDll ALL
      COMMENT "copying magic librairies for win32"
      COMMAND ${CMAKE_COMMAND} -E copy magic1.dll.win32 magic1.dll
      COMMAND ${CMAKE_COMMAND} -E copy zlib1.dll.win32 zlib1.dll
      COMMAND ${CMAKE_COMMAND} -E copy regex2.dll.win32 regex2.dll
      )
  endif( HAVE_64_BIT )

  set(magic_srcs
    __init__.py
    magic.mgc
    filetype.py
    magic1.dll
    magic.pyd
    zlib1.dll
    regex2.dll
    )
endif(WIN32 AND NOT UNIX)

install_file(magic ${magic_srcs})
