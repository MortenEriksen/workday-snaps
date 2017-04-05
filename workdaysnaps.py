#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import random
import hashlib
import argparse # since Python 3.2
import datetime

class PeriodArgument(argparse.Action):
    """helper class to parse --period input argument, from HH:MM format
       to datetime.timedelta."""

    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        super(PeriodArgument, self).__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        try:
            hhmm = [int(t) for t in values.split(":")]
            setattr(namespace, self.dest, datetime.timedelta(hours=hhmm[0], minutes=hhmm[1] if len(hhmm)>1 else 0))
        except:
            raise argparse.ArgumentError(self, "wrong format, must be HH:MM")


if __name__ == "__main__":

    argp = argparse.ArgumentParser(description="Take screenshots in regular intervals.")
    argp.add_argument("--period", help="time to run, in HH:MM format", nargs="?", default=datetime.timedelta(hours=8), action=PeriodArgument)
    argp.add_argument("--interval", help="seconds between each screenshot", type=int, nargs="?", default=30)
    argp.add_argument("--randomize", help="slightly randomize exact time of each screenshot", action="store_true")
    args = argp.parse_args()

    until = datetime.datetime.now() + args.period
    print("Will be taking screenshots at %d second intervals, up until %s." \
          % (args.interval, until.strftime("%H:%M:%S")))

    os.environ["DISPLAY"] = ":0.0"
    rootdir = os.path.join(os.path.dirname(__file__), "snaps", "%s" % time.strftime("%Y%m%d"))
    if not os.path.exists(rootdir): os.makedirs(rootdir)

    while datetime.datetime.now() < until:
        # +/- 15% if randomize
        waitsecs = args.interval if not args.randomize else random.randint(int(0.85*args.interval), int(1.15*args.interval))
        time.sleep(waitsecs)

        filename = os.path.join(rootdir, "%s.png" % time.strftime("%H%M%S"))

        os.system("/usr/bin/import -window root '%s'" % filename)
        sys.stdout.write('.'); sys.stdout.flush()

        # rm the snapshot file if identical with previous
        earlier = os.listdir(rootdir)
        earlier.sort()
        last = None if (len(earlier) == 0) else earlier[-1]
        # disabled the check-vs-last for now, don't want this as i want to try to make a movie
        if last and False:
            lastmd5 = hashlib.md5()
            f = open(os.path.join(rootdir, last), "rb")
            lastmd5.update(f.read())
            f.close()
            lastmd5 = lastmd5.hexdigest()

            newmd5 = hashlib.md5()
            f = open(filename, "rb")
            newmd5.update(f.read())
            f.close()
            newmd5 = newmd5.hexdigest()

            if lastmd5 == newmd5:
                os.remove(filename)


    # FIXME: for amalgamating them into a movie, something like this, from https://wiki.libav.org/Snippets/avconv
    #
    # Create video from image sequence
    # $ avconv -framerate 25 -f image2 -i image-%03d.jpeg -b 65536k out.mov
    #
    # Create video from image sequence (really good quality)
    # $ avconv -framerate 25 -f image2 -i %04d.png -c:v h264 -crf 1 out.mov

    sys.exit(0)
