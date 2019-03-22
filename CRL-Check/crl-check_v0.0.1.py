# -*- coding: utf-8 -*-


__doc__ = 'This script for check published on caweb.gazprom.ru CRL expiration date'
__version__ = 'v0.0.1'
__author__ = 'Konstantin Tornovskiy'
__email__ = 'coolship@yandex.ru'
__date__ = 'Apr 2017'

import winreg
import os
import argparse
import urllib.request

################################################
parser = argparse.ArgumentParser(description='This script for check published on caweb.gazprom.ru or on ocsp.shelf-neft.gazprom.ru CRL expiration date')
parser.add_argument('-c', '--crl-num', help="Check CRL by number")
parser.add_argument('-v', '--version', action='version', version='%(prog)s' + __version__)
args = parser.parse_args()
###############################################

url = 'http://ocsp/cdp/gazprom_neft_shelf_ca(3).crl'
urllib.request.urlretrieve(url, 'gazprom_neft_shelf_ca(3).crl')
