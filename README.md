# workday-snaps

Python command line tool using ImageMagick's "import" for X11 to grab
a screenshot at regular intervals for a pre-defined period. Usage:

`
$ workdaysnaps.py [-h] [--period PERIOD] [--interval [INTERVAL]]
                       [--randomize]

Take screenshots in regular intervals.

optional arguments:
  -h, --help            show this help message and exit
  --period PERIOD       time to run, in HH:MM format
  --interval [INTERVAL]
                        seconds between each screenshot
  --randomize           slightly randomize exact time of each screenshot
`
