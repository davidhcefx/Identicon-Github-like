# /usr/bin/python3
#
# Identicon Generator - Generate Github-like, horizontally symmetric Identicons.
# Written by davidhcefx, 2019.4.11

from math import ceil
import hashlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.colors as mcolors
from matplotlib.collections import PatchCollection


def generate(idcode: str, size: int) -> tuple:
    """
    @param size Output table size, 5 ~ 10
    @return Table and its color
    """
    h = hashlib.sha1(idcode.encode('utf8')).hexdigest()
    hashbin = bin(int(h, 16))[2:]
    table = [[0] * size for i in range(size)]

    # The Encodings:
    #   every 3rd bit => dots starting from upper-left to lower-right
    #   bit 136-143   => hue
    #   bit 144-151   => sat
    #   bit 152-159   => val (bright)

    idx = 0
    for i in range(size):
        for j in range(ceil(size / 2)):
            table[i][j] = table[i][size-1 - j] = int(hashbin[idx])
            idx += 3

    # The following ranges were decided empirically so that the color looks best:
    #   hue: 0 ~ 1
    #   sat: 45 ~ 100
    #   val: 45 ~ 80, depending on sat
    #     vrange: 25 -> 30(sat=60) -> 15
    #     vbase: 45 -> 50(sat=70) -> 60(sat=85) -> 65

    hue = int(hashbin[136:144], 2) / 256
    sat = int(hashbin[144:152], 2) / 256 * 55 + 45
    if sat < 60:
        vrange = (sat - 45) / 15 * 5 + 25
    else:
        vrange = (100 - sat) / 40 * 15 + 15

    if sat < 70:
        vbase = (sat - 45) / 25 * 5 + 45
    elif sat > 85:
        vbase = (sat - 85) / 15 * 5 + 60
    else:
        vbase = (sat - 70) / 15 * 10 + 50

    val = int(hashbin[152:160], 2) / 256 * vrange + vbase
    color = mcolors.hsv_to_rgb((hue, sat / 100, val / 100))

    return table, color


if __name__ == '__main__':
    s = input('Icon size: [5-10, default=5] ')
    size = int(s) if s != '' else 5
    if size not in range(5, 11):
        size = 5

    table, color = generate(input('ID code: '), size)

    # draw Identicon
    patches = []
    colors = []
    for i in range(size):
        for j in range(size):
            print(' O ' if table[i][j] == 1 else '   ', end='')
            patches.append(mpatches.Rectangle((j, size - i - 1), 1, 1))
            colors.append(color if table[i][j] == 1 else (1, 1, 1))
        print('')
    print('(R,G,B) = (%.2f, %.2f, %.2f)' % tuple(color))

    fig, ax = plt.subplots()
    collection = PatchCollection(patches, cmap=plt.cm.hsv)
    collection.set_facecolor(colors)
    ax.add_collection(collection)
    plt.axis('equal')
    plt.axis('off')
    plt.tight_layout()
    plt.show()
