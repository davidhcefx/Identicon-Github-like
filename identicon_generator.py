import hashlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.colors as mcolors
from matplotlib.collections import PatchCollection

#   Identicon Generator
#   Generate Github-like, horizontally symmetric Identicons.
#   Written by davidhcefx, 2019.4.11

s = input('Icon size: [5-10, default=5] ')
size = int(s) if s != '' else 5
if size not in range(5, 11): size = 5
hash = hashlib.sha1(input('ID code: ').encode('utf8')).hexdigest()
hashbin = bin(int(hash, 16))[2:]
table = [[0] * size for i in range(size)]

# Encoding:
#   every 3rd bit: dots starting from upper-left to lower-right
#   bit 136-143: hue
#   bit 144-151: sat
#   bit 152-159: val (bright)

idx = 0
for i in range(size):
    for j in range(int(size / 2) + size % 2):
        table[i][j] = table[i][size-1 - j] = hashbin[idx]
        idx += 3

hue = int(hash[34:35], 16) / 256
# acceptable sat: 45-100
sat = int(hash[36:37], 16) / 256 * 55 + 45
# acceptable val: 45-80, depending on sat
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

val = int(hash[38:39], 16) / 256 * vrange + vbase
color = mcolors.hsv_to_rgb((hue, sat / 100, val / 100))

# draw Identicon
patches = []
colors = []
for i in range(size):
    for j in range(size):
        print(' O ' if table[i][j] == '1' else '   ', end='')
        patches.append(mpatches.Rectangle((j, size - i - 1), 1, 1))
        colors.append(color if table[i][j] == '1' else (1, 1, 1))
    print('')

fig, ax = plt.subplots()
collection = PatchCollection(patches, cmap=plt.cm.hsv)
collection.set_facecolor(colors)
ax.add_collection(collection)
plt.axis('equal')
plt.axis('off')
plt.tight_layout()
plt.show()
