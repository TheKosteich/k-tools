# -*- coding: utf-8 -*-


__doc__ = 'This script for merge files, for example to create big wordlist'
__name__ = 'Merge-Files'
__version__ = 'v0.0'
__author__ = 'Konstantin Tornovskiy'
__email__ = 'coolship@yandex.ru'
__date__ = 'Feb 2017'


#import argparse


out_file = input("Enter full path for output file: ")
in_file = input("Enter full path for input file: ")

merged = open(out_file, 'r+')
source_file = open(in_file)
for line in source_file.readlines():
    if line not in merged:
        merged.write(line)

merged.close()
source_file.close()