# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 19:13:59 2019

@author: natur
"""

import hashlib
import time

hash = hashlib.sha1()
hash.update(str(time.time()).encode('utf-8'))
print(hash.hexdigest())
print(hash.hexdigest()[:10])