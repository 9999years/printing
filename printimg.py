#!  /usr/local/bin/python3.7
import sys
import subprocess
from typing import Text, Iterable
import argparse

from PIL import Image

__version__ = '1.0.0'

# mm
WIDTH = 72

# TODO the docs allege there is custom widths / heights available, but ive never been able to get it to work
HEIGHTS = (
        30, 40, 50, 60, 70, 80, 90,
        100, 110, 120, 130, 140, 150, 160, 170, 180, 190,
        200,
        )

def star_size(w: int, h: int) -> Text:
    return f'X{w}MMY{h}MM'

def best_height(ratio: float, width: int = WIDTH, heights: Iterable[int] = HEIGHTS):
    """
    gives the best height out of a selection of heights for an image of given
    ratio and width
    """
    def fitness(height: int) -> float:
        return ratio - width / height

    return min(sorted(filter(lambda h: fitness(h) > 0, heights), key=fitness))

def printimg(img_name: str):
    try:
        with Image.open(img_name) as img:
            # w/h
            ratio = img.width / img.height
    except IOError:
        print('Could not find', repr(img_name))
        return

    height = best_height(ratio)
    print('Printing at', WIDTH, '×', height, 'mm')
    subprocess.run(['lp', '-o', 'PageSize=' + star_size(WIDTH, height), img_name])

def main():
    parser = argparse.ArgumentParser(description='''
        Prints images given as filenames at the best available size via `lp`.
        Sizes are chosen from an internal hard-coded list, although I could
        probably parse lpoptions -l.
        ''')
    parser.add_argument('images', metavar='IMAGE', nargs=argparse.REMAINDER)
    parser.add_argument('-v', '--version', action='version', version=__version__)
    args = parser.parse_args()
    for img in args.images:
        printimg(img)

if __name__ == '__main__':
    main()
