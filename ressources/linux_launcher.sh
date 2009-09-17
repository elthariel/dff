#!/bin/sh
#
# DFF -- An Open Source Digital Forensics Framework
# Copyright (C) 2009 ArxSys
# 
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
#
#
# This script starts DFF. Its right place is in /usr/bin or
# /usr/local/bin (installer does it).
# It sets library path in order libraries from the DFF API be
# well resolved.
# 

LD_LIBRARY_PATH=${PYTHON_SITE_PACKAGES_PATH}/api/exceptions:${PYTHON_SITE_PACKAGES_PATH}/api/env:${PYTHON_SITE_PACKAGES_PATH}/api/loader:${PYTHON_SITE_PACKAGES_PATH}/api/module:${PYTHON_SITE_PACKAGES_PATH}/api/vfs:${PYTHON_SITE_PACKAGES_PATH}/api/type:${PYTHON_SITE_PACKAGES_PATH}/api/magic python ${PYTHON_SITE_PACKAGES_PATH}/dff/dff.py $*
