#!  /usr/local/bin/python3.7
import sys
import subprocess
from typing import Text, Iterable
import argparse
import io

__version__ = '1.0.0'

# inches
WIDTH_IN = 2.8346457
WIDTH_PX = 576

def printtxt(txt, ratio: float = 0.5,
        width: float = WIDTH_IN,
        width_px: int = WIDTH_PX,
        noop=False):
    line_len = len(max(txt.split('\n'), key=len))
    precision = 3
    # lpi wraps aggresively
    compensate = 1.05
    cpi = round((line_len * compensate) / width, precision)
    lpi = round(cpi * ratio, precision)
    print('Printing at', cpi, 'CPI and', lpi, 'LPI')
    px_per_char = width_px / width / cpi
    print('Characters are', round(px_per_char, 1), '×',
            round(px_per_char * ratio, 1), 'px')
    print('Longest line is', line_len, 'chars long')
    if not noop:
        proc = subprocess.Popen(['lp', '-o', f'cpi={cpi}', '-o', f'lpi={lpi}'], stdin=subprocess.PIPE)
        proc.communicate(input=txt.encode('utf-8'))

def main():
    parser = argparse.ArgumentParser(description='''
        Prints text files given as filenames at the largest possible size via
        `lp`.
        ''')
    parser.add_argument('files', metavar='FILE', nargs=argparse.REMAINDER, type=open)
    parser.add_argument('-r', '--ratio', type=float, default=0.5,
            help='''Width/height ratio for output; default 0.5 = lines are
            twice as tall as characters are wide''')
    parser.add_argument('-w', '--whatif',
            action='store_true',
            help="Don't print anything")
    parser.add_argument('-v', '--version', action='version', version=__version__)
    args = parser.parse_args()
    for file in args.files:
        printtxt(file.read(), ratio=args.ratio,
                noop=args.whatif)
    if not args.files:
        printtxt(sys.stdin.read(), ratio=args.ratio,
                noop=args.whatif)

if __name__ == '__main__':
    main()
