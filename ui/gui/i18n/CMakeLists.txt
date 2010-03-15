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
#  Solal Jacob <sja@digital-forensic.org>


set(i18n_srcs
  Browsers_en.ts
  Browsers_fr.ts
  Dff_en.qm
  Dff_en.ts
  Dff_fr.qm
  Dff_fr.ts
  Project_en.ts
  Project_fr.ts
  Tools_en.ts
  Tools_fr.ts
  UI_en.ts
  UI_fr.ts
  Viewers_en.ts
  Viewers_fr.ts
)

install_file(i18n ${i18n_srcs})
