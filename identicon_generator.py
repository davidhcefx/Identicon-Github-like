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
    @param size Output table size, 5 ~ 20
    @return Table and its color
    """

    h = hashlib.sha512(idcode.encode('utf8')).hexdigest() + \
        hashlib.sha512((idcode + 'SEED:3.1416').encode('utf8')).hexdigest()
    hashbin = '{:0>1024}'.format(bin(int(h, 16))[2:])
    table = [[0] * size for i in range(size)]

    # The Encodings:
    #   bit 0-7       => hue
    #   bit 8-15      => sat
    #   bit 16-23     => val (bright)
    #   every 3rd bit => dots starting from upper-left to lower-right

    idx = 24
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

    hue = int(hashbin[0:8], 2) / 256
    sat = int(hashbin[8:16], 2) / 256 * 55 + 45
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

    val = int(hashbin[16:24], 2) / 256 * vrange + vbase
    color = mcolors.hsv_to_rgb((hue, sat / 100, val / 100))

    return table, color


if __name__ == '__main__':
    s = input('Icon size: [5-20, default=5] ')
    size = int(s) if s != '' else 5
    if size not in range(5, 21):
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