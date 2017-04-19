#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time
from page_parsing import collection

while True:
    print collection.find().count()
    time.sleep(10)