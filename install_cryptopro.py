__author__ = 'Konstantin Tornovskiy'
# -*- coding: utf-8 -*-


import winreg
import time
import wmi
import os
#import shutil
#shutil.copy('C:/temp/csp_install/cspsetup.exe', '\\\\' + ip + '\\C$\\temp\\')
#os.remove(r'\\' + ip + r'\C$\Temp\cspsetup.exe')


def parse_range(ip_range):
    dash_index = ip_range.index('-')
    net_index = ''
    ip_list = []
    i = dash_index
    while i:
        if ip_range[i] == '.':
            net_index = i
            i = False
        else:
            i -= 1
    net = ip_range[:net_index + 1]
    first_ip = int(ip_range[net_index + 1:dash_index])
    last_ip = int(ip_range[dash_index + 1:])
    ip = first_ip
    while ip <= last_ip:
        ip_list.append(str(net + str(ip)))
        ip += 1
    return ip_list


def install_csp(ip):
    print('Job has been started on ' + ip + '\n' + 30*'*')
    try:
        c = wmi.WMI(ip)
        print('Computer name is - ' + c.Win32_OperatingSystem()[0].CSName)
        if c.Win32_Service(Name='RemoteRegistry')[0].State == 'Running':
            try:
                connect_reg = winreg.ConnectRegistry('\\\\' + ip, winreg.HKEY_LOCAL_MACHINE)
                open_key = winreg.OpenKey(connect_reg, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Installer\UserData\S-1-5-18\Products\05480A45343B0B0429E4860F13549069\InstallProperties')
                reg_value, req_state = winreg.QueryValueEx(open_key, r'DisplayVersion')
                if reg_value != '3.6.7777':
                    os.system(r'M:\tools\PsExec.exe \\' + ip + r' -c C:\Temp\cspsetup.exe -silent -args /norestart')
                    print('CryptoPro installed')
                    winreg.DeleteKey(connect_reg, r'SOFTWARE\Microsoft\Cryptography\Calais\SmartCards\eToken_PRO_M420b_Default')
                    winreg.DeleteKey(connect_reg, r'SOFTWARE\Microsoft\Cryptography\Calais\SmartCards\eToken_JAVA_10_Default')
                    if c.Win32_OperatingSystem()[0].osarchitecture == '64-bit':
                        print(c.Win32_OperatingSystem()[0].osarchitecture)
                        winreg.DeleteKey(connect_reg, r'SOFTWARE\Wow6432Node\Microsoft\Cryptography\Calais\SmartCards\eToken_PRO_M420b_Default')
                        winreg.DeleteKey(connect_reg, r'SOFTWARE\Wow6432Node\Microsoft\Cryptography\Calais\SmartCards\eToken_JAVA_10_Default')
                    print('Keys on ' + ip + ' was be deleted\n')
                    time.sleep(10)
                winreg.CloseKey(open_key)
                winreg.CloseKey(connect_reg)
            except FileNotFoundError:
                print('Can not open path on - ' + ip + '. May be CryptoPro not installed!\n')
        elif c.Win32_Service(Name='RemoteRegistry')[0].State == 'Stopped':
            c.Win32_Service(Name='RemoteRegistry')[0].StartService()
            time.sleep(10)
            try:
                connect_reg = winreg.ConnectRegistry('\\\\' + ip, winreg.HKEY_LOCAL_MACHINE)
                open_key = winreg.OpenKey(connect_reg, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Installer\UserData\S-1-5-18\Products\05480A45343B0B0429E4860F13549069\InstallProperties')
                reg_value, req_state = winreg.QueryValueEx(open_key, r'DisplayVersion')
                if reg_value != '3.6.7777':
                    os.system(r'M:\tools\PsExec.exe \\' + ip + r' -c C:\Temp\cspsetup.exe -silent -args /norestart')
                    print('CryptoPro installed')
                    winreg.DeleteKey(connect_reg, r'SOFTWARE\Microsoft\Cryptography\Calais\SmartCards\eToken_PRO_M420b_Default')
                    winreg.DeleteKey(connect_reg, r'SOFTWARE\Microsoft\Cryptography\Calais\SmartCards\eToken_JAVA_10_Default')
                    if c.Win32_OperatingSystem()[0].osarchitecture == '64-bit':
                        print(c.Win32_OperatingSystem()[0].osarchitecture)
                        winreg.DeleteKey(connect_reg, r'SOFTWARE\Wow6432Node\Microsoft\Cryptography\Calais\SmartCards\eToken_PRO_M420b_Default')
                        winreg.DeleteKey(connect_reg, r'SOFTWARE\Wow6432Node\Microsoft\Cryptography\Calais\SmartCards\eToken_JAVA_10_Default')
                    print('Keys on ' + ip + ' was be deleted\n')
                    time.sleep(10)
                winreg.CloseKey(open_key)
                winreg.CloseKey(connect_reg)
            except FileNotFoundError:
                print('Can not open path on - ' + ip + '. May be CryptoPro not installed!\n')
            c.Win32_Service(Name='RemoteRegistry')[0].StopService()
        else:
            print('Not recognized service state on ' + ip + ' - ' + c.Win32_Service(Name='RemoteRegistry')[0].State + '\n')
    except wmi.x_wmi:
        print('WMI on host ' + ip + ' not allowed.\n')
    return 0


# EXCEPT
#   limonov_nv (10.61.47.163)
#   gustoy  (10.61.46.114)
#   lyubingp (10.61.46.158)

#ip_list = parse_range('10.61.47.135-162')
ip_list = [
    #'10.61.46.135',
    #'10.61.44.194',
    #'10.61.46.128',
    #'10.61.47.127',
    #'10.61.44.153',
    #'10.61.47.132',
    '10.61.46.113',
    ]

for host_ip in ip_list:
    install_csp(host_ip)