#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re

HOTFIX_PATTERN = 'KB[\d]{7}'

with open(r'C:\tmp\ca0233_hotfixes.txt', 'r') as etalon_file:
    for line in etalon_file.readlines():
        if 'Security Update' in line:
            kb_id = re.search(HOTFIX_PATTERN, line).group()
            with open(r'C:\tmp\ra_hotfixes.txt', 'r') as ca_server_file:
                for ca_item in ca_server_file.readlines():
                    if kb_id in ca_item:
                        break
                else:
                    print(kb_id)
