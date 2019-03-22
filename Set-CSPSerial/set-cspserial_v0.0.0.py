# -*- coding: utf-8 -*-


__doc__ = 'This script for run someone on all computer from IP range'
__name__ = 'Run-OnAll'
__version__ = 'v0.0.0c'
__author__ = 'Konstantin Tornovskiy'
__email__ = 'coolship@yandex.ru'
__date__ = 'Dec 2016'


import winreg
import os


leave = False
while not leave:
    host = input('Enter Hostname on host IP: ')
    if True if os.system('ping -n 1 ' + host) is 0 else False:
        connect_reg = winreg.ConnectRegistry('\\\\' + host, winreg.HKEY_LOCAL_MACHINE)
        open_key = winreg.OpenKey(connect_reg,
                                  r'SOFTWARE\Microsoft\Windows\CurrentVersion\Installer\UserData\S-1-5-18\Products\68A52D936E5ACF24C9F8FE4A1C830BC8\InstallProperties',
                                  0,
                                  winreg.KEY_ALL_ACCESS)
        csp_version, req_state = winreg.QueryValueEx(open_key, r'DisplayVersion')
        print('\n' + '#' * 30 + '\nCurrent information')
        print('Version - %s' % csp_version)
        csp_owner, req_state = winreg.QueryValueEx(open_key, r'RegOwner')
        print('Registered owner - %s' % csp_owner)
        csp_company, req_state = winreg.QueryValueEx(open_key, r'RegCompany')
        print('Registered company owner - %s' % csp_company)
        csp_serial, req_state = winreg.QueryValueEx(open_key, r'ProductID')
        print('Current serial - %s' % csp_serial)
    else:
        print('Host is down!')

    response = input('\nChange CSP settings? (y/n): ')
    if response.lower() == 'y' or response.lower() == 'yes':
        new_owner = input('Enter new CSP owner (default - %s): ' % csp_owner)
        if new_owner:
            winreg.SetValueEx(open_key, 'RegOwner', 0, winreg.REG_SZ, new_owner)
        else:
            pass

        csp_company = 'ООО "Газпром нефть шельф"'
        new_company = input('Enter new CSP owner (default - %s): ' % csp_company)
        if new_company:
            winreg.SetValueEx(open_key, 'RegCompany', 0, winreg.REG_SZ, new_company)
        else:
            pass

        new_serial = input('Enter new CSP owner (default - %s): ' % csp_serial)
        if new_serial:
            winreg.SetValueEx(open_key, 'ProductID', 0, winreg.REG_SZ, new_serial)
        else:
            pass
    elif response.lower() == 'n' or response.lower() == 'no':
        pass
    else:
        print("Input don't recognized. You will be redirected to the next step!")

    response = input('\nWork with different host? (y/n): ')
    if response.lower() == 'y' or response.lower() == 'yes':
        leave = False
    elif response.lower() == 'n' or response.lower() == 'no':
        leave = True
    else:
        print("Input don't recognized. You will be redirected to the next step!")