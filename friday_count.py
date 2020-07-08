#!/usr/bin/python3
# -*- coding: utf-8 -*-


import datetime as dt

NEXT_YEAR = dt.datetime.now().year + 1
FRIDAY_INDEX = dt.datetime.now().weekday()

current_date = dt.datetime.now()
timedelta = dt.timedelta(days=1)
friday_count = 0

while current_date.year != NEXT_YEAR:
    if current_date.weekday() == FRIDAY_INDEX:
        friday_count += 1
    current_date += timedelta

print(friday_count)
