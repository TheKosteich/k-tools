__author__ = 'Tornovskiy Konstantin'


import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-cs', '--check-csp', help="Check installed Crypto PRO CSP version", action='store_true')
parser.add_argument('-v', '--get-version', help="Get dictionary with Hostname(IP) and Crypto PRO CSP version", action='store_true')
parser.add_argument('-f', '--write-file', help="Write output to file", action='store_true')
parser.add_argument('-r', '--range', help='Machine IP range')
args = parser.parse_args()

if args.range:
    print('Check CSP on range - ' + args.range)
else:
    print('Enter some range')
if args.check_csp:
    print('Check is enabled')