#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
#
#
# com.py
#
# Copyright (C) 2011 Lorenzo Carbonell
# lorenzo.carbonell.cerezo@gmail.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
#
__author__ = 'Lorenzo Carbonell <lorenzo.carbonell.cerezo@gmail.com>'
__date__ ='$03/03/2012'
__copyright__ = 'Copyright (c) 2012 Lorenzo Carbonell'
__license__ = 'GPLV3'
__url__ = 'http://www.atareao.es'
__version__ = '0.0.3.2'

import os

######################################

def is_package():
    return __file__.find('src') < 0

######################################


VERSION = __version__
APP = 'google-tasks-indicator'
APPCONF = APP + '.conf'
APPNAME = 'Google-Tasks-Indicator'

# check if running from source
if is_package():
    ROOTDIR = '/usr/share/'
    LANGDIR = os.path.join(ROOTDIR, 'locale-langpack')
    APPDIR = os.path.join(ROOTDIR, APP)
    ICONDIR = os.path.join(APPDIR, 'icons')
    ICON = '/usr/share/pixmaps/google-tasks-indicator.svg'    
else:
    VERSION = VERSION + '-src'
    ROOTDIR = os.path.split(os.path.dirname(__file__))[0]
    LANGDIR = os.path.join(ROOTDIR, 'template1')
    APPDIR = os.path.join(ROOTDIR, APP)
    ICONDIR = os.path.join(ROOTDIR, 'data/icons')
    ICON = os.path.join(ICONDIR,'google-tasks-indicator.svg')
CONFIG_DIR = os.path.join(os.path.expanduser('~'),'.config')
CONFIG_APP_DIR = os.path.join(CONFIG_DIR, APP)
CONFIG_FILE = os.path.join(CONFIG_APP_DIR, APPCONF)
COOKIE_FILE = os.path.join(CONFIG_APP_DIR, 'oauth2.dat')
