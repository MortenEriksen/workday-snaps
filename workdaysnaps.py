#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import time
import random
import hashlib

if __name__ == "__main__":
    time.sleep(random.randint(1, 5*60))

    os.environ['DISPLAY'] = ':0.0'

    rootdir = os.path.join(os.path.dirname(__file__), 'snaps', '%s' % time.strftime('%Y%m%d'))
    if not os.path.exists(rootdir): os.makedirs(rootdir)

    earlier = os.listdir(rootdir)
    earlier.sort()
    last = None if (len(earlier) == 0) else earlier[-1]

    filename = os.path.join(rootdir, '%s.png' % time.strftime('%H%M%S'))

    os.system('/usr/bin/import -window root "%s"' % filename)

    if last:
        lastmd5 = hashlib.md5()
        f = open(os.path.join(rootdir, last), 'rb')
        lastmd5.update(f.read())
        f.close()
        lastmd5 = lastmd5.hexdigest()

        newmd5 = hashlib.md5()
        f = open(filename, 'rb')
        newmd5.update(f.read())
        f.close()
        newmd5 = newmd5.hexdigest()

        if lastmd5 == newmd5:
            os.remove(filename)
    

    sys.exit(0)
