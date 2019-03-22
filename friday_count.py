#!/usr/bin/python3
# -*- coding: utf-8 -*-


import datetime

current_date = datetime.datetime.now()
timedelta = datetime.timedelta(1)
friday_count = 0

while current_date.year != 2019:
    if current_date.weekday() == 4:
        friday_count += 1
    current_date += timedelta

print(friday_count)
