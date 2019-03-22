# -*- coding: utf-8 -*-


__doc__ = 'This script for run someone on all computer from IP range'
__name__ = 'Run-OnAll'
__version__ = 'v0.0.2b'
__author__ = 'Konstantin Tornovskiy'
__email__ = 'coolship@yandex.ru'
__date__ = 'Dec 2016'

import winreg
import os
import argparse


#################################################
parser = argparse.ArgumentParser(description='Script for CryptoPRO CSP 3.9. serial key management.')
parser.add_argument('-cs', '--check-csp', help="Example: Check installed Crypto PRO CSP version", action='store_true')
parser.add_argument('-r', '--range', help='Example: Machine IP range')
parser.add_argument('-v', '--version', action='version', version='%(prog)s v0.0.2b')
args = parser.parse_args()

'''
print(args.range)

if args.check_csp:
    print('Check is enabled')
'''
###############################################

LEAVE = False
APPROVE = ['y', 'yes', 'д', 'да', '1']
DENY = ['n', 'no', 'н', 'нет', '0']

try:
    while not LEAVE:
        host = input('\nEnter Hostname or host IP: ')
        if True if os.system('ping -n 1 ' + host) is 0 else False:
            try:
                connect_reg = winreg.ConnectRegistry('\\\\' + host, winreg.HKEY_LOCAL_MACHINE)
                open_key = winreg.OpenKey(connect_reg,
                                          r'SOFTWARE\Microsoft\Windows\CurrentVersion\Installer\UserData\S-1-5-18\Products\68A52D936E5ACF24C9F8FE4A1C830BC8\InstallProperties',
                                          0,
                                          winreg.KEY_ALL_ACCESS)
            except FileNotFoundError:
                print('\nUnable connect to remote registry on host %s' % host)
                continue
            csp_version, req_state = winreg.QueryValueEx(open_key, r'DisplayVersion')
            print('\n' + '#' * 30 + '\nCurrent information')
            print('CSP Version - %s' % csp_version)

            csp_owner, req_state = winreg.QueryValueEx(open_key, r'RegOwner')
            print('Registered owner - %s' % csp_owner)

            csp_company, req_state = winreg.QueryValueEx(open_key, r'RegCompany')
            print('Registered company owner - %s' % csp_company)

            csp_serial, req_state = winreg.QueryValueEx(open_key, r'ProductID')
            print('Current serial - %s' % csp_serial)

            response = input('\nChange CSP settings? (y/n): ')
            if response.lower() in APPROVE:
                new_owner = input('Enter new CSP owner (default - %s): ' % csp_owner)
                if new_owner:
                    winreg.SetValueEx(open_key, 'RegOwner', 0, winreg.REG_SZ, new_owner)
                else:
                    pass

                csp_company = 'ООО "Газпром нефть шельф"'
                new_company = input('Enter new CSP company (default - %s): ' % csp_company)
                if new_company:
                    winreg.SetValueEx(open_key, 'RegCompany', 0, winreg.REG_SZ, new_company)
                else:
                    winreg.SetValueEx(open_key, 'RegCompany', 0, winreg.REG_SZ, csp_company)

                new_serial = input('Enter new CSP serial (default - %s): ' % csp_serial)
                if new_serial:
                    winreg.SetValueEx(open_key, 'ProductID', 0, winreg.REG_SZ, new_serial.replace('-', ''))
                else:
                    pass
            elif response.lower() in DENY:
                pass
            else:
                print("Input don't recognized. You will be redirected to the next step!")
            winreg.CloseKey(open_key)
            winreg.CloseKey(connect_reg)
        else:
            print('\n' + '#' * 30 + '\nHost is down!')

        response = input('\nWork with different host? (y/n): ')
        if response.lower() in APPROVE:
            LEAVE = False
        elif response.lower() in DENY:
            LEAVE = True
        else:
            print("Input don't recognized. You will be redirected to the next step!")
except KeyboardInterrupt:
    print('\n\nHave a nice day! Goodbye!')
    exit(0)
