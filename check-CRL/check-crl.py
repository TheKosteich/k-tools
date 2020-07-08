#!/usr/bin/python3
# -*- coding: utf-8 -*-


__doc__ = 'This script for check CRL expiration date'
__version__ = 'v0.0.1'
__author__ = 'Konstantin Tornovskiy'
__email__ = 'coolship@yandex.ru'
__date__ = 'Jul 2020'

import argparse
import datetime as dt
import logging
import os

import requests
from cryptography.hazmat.backends import default_backend
from cryptography.x509 import load_der_x509_crl, load_pem_x509_crl
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(name)s: %(message)s',
    datefmt='%d-%b-%y %H:%M:%S',
    filename='check-crl.log',
    level=logging.INFO
)

CRL_URLS = os.getenv('CRL_URLS').split(' ')
CRL_OVERLAP_MINUTES = int(os.getenv('CRL_OVERLAP_MINUTES'))

parser = argparse.ArgumentParser(
    description='This script for check published on caweb.gazprom.ru'
                ' or on ocsp.shelf-neft.gazprom.ru CRL expiration date'
)
parser.add_argument('-c', '--crl-num', help="Check CRL by number")
parser.add_argument('-v', '--version', action='version',
                    version=f'crl-check {__version__}')
args = parser.parse_args()


def check_crl(urls, overlap_minutes):
    result = {}

    for url in urls:
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.exceptions.RequestException as error:
            logging.error(f'Error in request process - {error}')
            continue
        try:
            crl = load_pem_x509_crl(response.content, default_backend())
        except ValueError:
            crl = load_der_x509_crl(response.content, default_backend())
        time_delta = dt.timedelta(minutes=overlap_minutes)
        time_to_update = crl.next_update - dt.datetime.now()
        crl_filename = url.split('/')[-1]
        if 0 < time_to_update < time_delta:
            result[crl_filename] = 'Out of overlap period'
        elif time_to_update < 0:
            result[crl_filename] = 'EXPIRED'
        else:
            result[crl_filename] = 'UPDATED'

    return result


def main():
    print(check_crl(CRL_URLS, CRL_OVERLAP_MINUTES))


if __name__ == '__main__':
    main()
