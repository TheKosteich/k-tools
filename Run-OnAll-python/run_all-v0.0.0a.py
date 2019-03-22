# -*- coding: utf-8 -*-


__doc__ = 'This script for run someone on all computer from IP range'
__version__ = 'v0.0.0b'
__author__ = 'Konstantin Tornovskiy'
__email__ = 'coolship@yandex.ru'
__date__ = 'Dec 2016'

import os
import argparse

#################################################
parser = argparse.ArgumentParser(description='Run some command on some ')
parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)
args = parser.parse_args()
###############################################

SUBNET_RANGE1 = '10.61.44.90-200'
SUBNET_RANGE2 = '10.61.45.90-200'
SUBNET_RANGE3 = '10.61.46.90-200'
SUBNET_RANGE4 = '10.61.47.90-200'

COMMAND_PART1 = r'psexec \\'
COMMAND_PART2 = r' "C:\Program Files (x86)\Crypto Pro\CSP\cpverify.exe" -rm system'


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


computer_list = parse_range(SUBNET_RANGE1) + parse_range(SUBNET_RANGE2) + parse_range(SUBNET_RANGE3) + parse_range(
    SUBNET_RANGE4)

for ip in computer_list:
    if True if os.system("ping -n 1 " + ip) is 0 else False:
        os.system(COMMAND_PART1 + ip + COMMAND_PART2)
    else:
        print('Computer with IP - %s is down!' % ip)