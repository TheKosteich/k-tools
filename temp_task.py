#!/usr/bin/python3
# -*- coding: utf-8 -*-

import codecs
import random

rand_file = codecs.open(r'C:\Users\tornovskiy.kg\Desktop\items.txt', 'r', "utf_8_sig")
text = rand_file.read()
rand_file.close()
print(text)
