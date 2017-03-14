from collections import namedtuple
import numpy as np
import matplotlib.pyplot as plt
from random import randrange, choice
import sys


Corner = namedtuple('Corner', ['left', 'right'])
Edge = namedtuple('Edge', 'color')
orange = '#ff8300'
blue = '#07347c'
red = '#a31010'
green = '#76ff00'
yellow = '#ffff00'


plt.rcParams['keymap.fullscreen'] = []
plt.rcParams['keymap.save'] = []


PLLS = [
    ('Aa', [0,3,1,2], [0,1,2,3], 4),
    ('Ab', [1,2,0,3], [0,1,2,3], 4),
    ('E',  [1,0,3,2], [0,1,2,3], 2),
    ('F',  [0,1,3,2], [0,3,2,1], 4),
    ('Ga', [3,0,2,1], [2,1,3,0], 4),
    ('Gb', [1,3,2,0], [3,1,0,2], 4),
    ('Gc', [1,2,0,3], [2,0,1,3], 4),
    ('Gd', [2,0,1,3], [1,2,0,3], 4),
    ('H',  [0,1,2,3], [2,3,0,1], 1),
    ('Ja', [3,1,2,0], [3,1,2,0], 4),
    ('Jb', [0,2,1,3], [1,0,2,3], 4),
    ('Na', [2,1,0,3], [0,3,2,1], 1),
    ('Nb', [0,3,2,1], [0,3,2,1], 1),
    ('Ra', [1,0,2,3], [0,2,1,3], 4),
    ('Rb', [0,1,3,2], [1,0,2,3], 4),
    ('S',  [0,1,2,3], [0,1,2,3], 1),
    ('T',  [0,2,1,3], [0,3,2,1], 4),
    ('Ua', [0,1,2,3], [0,2,3,1], 4),
    ('Ub', [0,1,2,3], [0,3,1,2], 4),
    ('V',  [0,3,2,1], [0,2,1,3], 4),
    ('Y',  [0,3,2,1], [0,1,3,2], 4),
    ('Z',  [0,1,2,3], [1,0,3,2], 2),
]

AUFS = [
    ([0,1,2,3], [0,1,2,3]),
    ([1,2,3,0], [1,2,3,0]),
    ([2,3,0,1], [2,3,0,1]),
    ([3,0,1,2], [3,0,1,2]),
]

ALIASES = {
    'Ga': 'Ga',
    'Gb': 'Gb',
    'Gc': 'Ga',
    'Gd': 'Gb',
}


def parity(perm):
    perm = list(perm)
    even = True
    for i in range(len(perm)):
        if perm[i] != i:
            c = perm.index(i)
            perm[i], perm[c] = perm[c], perm[i]
            even = not even
    return even


class PLL:

    def __init__(self, angle=20.0):
        angle *= np.pi / 180
        self.cx = np.cos(angle)
        self.cy = np.sin(angle)

    def perm(self):
        corners = [Corner(orange, blue), Corner(blue, red),
                        Corner(red, green), Corner(green, orange)]
        edges = [Edge(blue), Edge(red), Edge(green), Edge(orange)]

        total = sum(p for _, _, _, p in PLLS)
        r = randrange(total)
        for name, cp, ep, p in PLLS:
            if r < p:
                break
            r -= p

        corners = [corners[i] for i in cp]
        edges = [edges[i] for i in ep]

        cp, ep = choice(AUFS)
        return name, [corners[i] for i in cp], [edges[i] for i in ep]

    def square(self, dist, lefty, color):
        cx, cy = self.cx, self.cy
        if lefty:
            plt.fill(
                [-dist*cx, -(dist+1)*cx, -(dist+1)*cx, -dist*cx],
                [dist*cy, (dist+1)*cy, (dist+1)*cy + 1, dist*cy + 1],
                color=color,
            )
        else:
            plt.fill(
                [dist*cx, (dist+1)*cx, (dist+1)*cx, dist*cx],
                [dist*cy, (dist+1)*cy, (dist+1)*cy + 1, dist*cy + 1],
                color=color,
            )

    def fronts(self, left, right):
        cx, cy = self.cx, self.cy
        plt.fill([0, -3*cx, -3*cx, 0], [0, 3*cy, 3*cy - 2, -2], color=left)
        plt.fill([0, 3*cx, 3*cx, 0], [0, 3*cy, 3*cy - 2, -2], color=right)

    def finalize(self):
        cx, cy = self.cx, self.cy
        plt.fill(
            [0, 3*cx, 0, -3*cx],
            [1, 3*cy + 1, 6*cy + 1, 3*cy + 1],
            color=yellow
        )

        kw = {
            'linewidth': 6,
            'color': 'black',
            'solid_capstyle': 'round',
        }
        for i in range(4):
            plt.plot([-i*cx, -i*cx, (3-i)*cx], [i*cy - 2, i*cy + 1, (3+i)*cy + 1], **kw)
            plt.plot([i*cx, i*cx, (i-3)*cx], [i*cy - 2, i*cy + 1, (3+i)*cy + 1], **kw)
        for i in range(3):
            plt.plot([-3*cx, 0, 3*cx], [3*cy - i, -i, 3*cy - i], **kw)

        plt.xlim(-4*cx, 4*cx)
        plt.ylim(-3, 2 + 6*cy)
        plt.axes().set_aspect(1)
        plt.axis('off')

    def show(self):
        plt.clf()
        name, c, e = self.perm()
        if name in ALIASES:
            self.name = ALIASES[name].lower()
        else:
            self.name = name[0].lower()
        self.square(2, True, c[0].right)
        self.square(1, True, e[0].color)
        self.square(0, True, c[1].left)
        self.square(0, False, c[1].right)
        self.square(1, False, e[1].color)
        self.square(2, False, c[2].left)
        self.fronts(*choice([
            (blue, red), (red, green),
            (green, orange), (orange, blue)
        ]))
        self.finalize()
        plt.connect('key_press_event', self.press)
        plt.draw()

    def press(self, event):
        if event.key == self.name[0]:
            self.name = self.name[1:]
        if not self.name or event.key == ' ':
            self.show()
        if event.key == 'q':
            sys.exit(0)


if __name__ == '__main__':
    pll = PLL()
    pll.show()
    plt.show()
