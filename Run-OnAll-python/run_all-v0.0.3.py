# -*- coding: utf-8 -*-


__doc__ = 'This script for run someone on all computer from IP range'
__version__ = 'v0.0.3a'
__author__ = 'Konstantin Tornovskiy'
__email__ = 'coolship@yandex.ru'
__date__ = 'Oct 2017'

import os
import argparse
import shutil
from multiprocessing import Pool
import time

#################################################
parser = argparse.ArgumentParser(description='Run command on some hosts')
parser.add_argument('-rh', '--renew-hash', help='Renew system files hash after updates', action='store_true')
parser.add_argument('-sd', '--sc-delete', help='Stop and delete service', action='store_true')
parser.add_argument('-u', '--upgrade-csp', help='Upgrade CryptoPRO CSP to version 4.0', action='store_true')
parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)
args = parser.parse_args()
################################################

SUBNET_RANGE1 = '10.61.44.90-200'
SUBNET_RANGE2 = '10.61.45.90-200'
SUBNET_RANGE3 = '10.61.46.90-200'
SUBNET_RANGE4 = '10.61.47.90-200'


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


def is_online(host):
    if os.system('ping -n 1 ' + host) is 0:
        return True
    else:
        return False


def get_online(hosts):
    online_hosts = []
    for host in hosts:
        if is_online(host):
            online_hosts.append(host)
    return online_hosts


def upgrade_csp(host):
    # remove CryptoPRO 3.9
    # os.system(('psexec.exe \\\\%s MsiExec.exe /x{39D25A86-A5E6-42FC-9C8F-EFA4C138B08C} /quiet /norestart') % host)
    os.system(f'psexec.exe \\\\{host} MsiExec.exe /x{39D25A86-A5E6-42FC-9C8F-EFA4C138B08C} /quiet')
    destination = (f'\\\\{host}\C$\\tmp')
    rm_destination = (f'\\\\{host}\\C$\\tmp')
    source_msi = 'C:\\tmp\\csp-x64-kc1-rus.msi'
    source_bat = 'C:\\tmp\\install.bat'
    if os.path.isfile(rm_destination):
        os.remove(rm_destination)
    # shutil.rmtree(rm_destination)
    if not os.path.exists(destination):
        os.makedirs(destination)
    shutil.copy(source_msi, destination)
    shutil.copy(source_bat, destination)
     # устанавливаем КриптоПРО 4.0
    os.system(('psexec.exe \\\\{} C:\\tmp\\install.bat').format(host))
    shutil.rmtree(rm_destination)


computer_list = parse_range(SUBNET_RANGE1)\
                + parse_range(SUBNET_RANGE2)\
                + parse_range(SUBNET_RANGE3)\
                + parse_range(SUBNET_RANGE4)

if __name__ == '__main__':
    try:
        if args.renew_hash:
            for ip in computer_list:
                if True if os.system("ping -n 1 " + ip) is 0 else False:
                    os.system(f'psexec \\\\{ip} "C:\\Program Files (x86)\\Crypto Pro\\CSP\\cpverify.exe" -rm system')
                else:
                    print(f'Computer with IP - {ip} is down!')
        elif args.sc_delete:
            for ip in computer_list:
                if True if os.system("ping -n 1 " + ip) is 0 else False:
                    os.system(f'sc \\\\{ip} stop dwmrcs')
                    os.system(f'sc \\\\{ip} delete dwmrcs')
                else:
                    print(f'Computer with IP - {ip} is down!')
        elif args.upgrade_csp:
            pool = Pool(processes=4)
            pool.map(upgrade_csp, computer_list)
            pool.close()
            pool.join()
        else:
            print('\nThe required action is not specified!')
    except KeyboardInterrupt:
        print('\n\nHave a nice day! Goodbye!')
        exit(0)