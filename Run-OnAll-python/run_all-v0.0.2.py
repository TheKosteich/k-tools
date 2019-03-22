# -*- coding: utf-8 -*-


__doc__ = 'This script for run someone on all computer from IP range'
__version__ = 'v0.0.2a'
__author__ = 'Konstantin Tornovskiy'
__email__ = 'coolship@yandex.ru'
__date__ = 'Jun 2017'

import os
import argparse

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


computer_list = parse_range(SUBNET_RANGE1)\
                + parse_range(SUBNET_RANGE2)\
                + parse_range(SUBNET_RANGE3)\
                + parse_range(SUBNET_RANGE4)

try:
    if args.renew_hash:
        for ip in computer_list:
            if True if os.system("ping -n 1 " + ip) is 0 else False:
                os.system('psexec \\\\{} "C:\\Program Files (x86)\\Crypto Pro\\CSP\\cpverify.exe" -rm system'.format(ip))
            else:
                print('Computer with IP - %s is down!' % ip)
    elif args.sc_delete:
        for ip in computer_list:
            if True if os.system("ping -n 1 " + ip) is 0 else False:
                os.system("sc \\\\{} stop dwmrcs".format(ip))
                os.system("sc \\\\{} delete dwmrcs".format(ip))
            else:
                print('Computer with IP - %s is down!' % ip)
    else:
        print('\nThe required action is not specified!')
except KeyboardInterrupt:
    print('\n\nHave a nice day! Goodbye!')
    exit(0)