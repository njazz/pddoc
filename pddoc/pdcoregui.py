#!/usr/bin/env python
# coding=utf-8

#   Copyright (C) 2014 by Serge Poltavski                                 #
#   serge.poltavski@gmail.com                                            #
#                                                                         #
#   This program is free software; you can redistribute it and/or modify  #
#   it under the terms of the GNU General Public License as published by  #
#   the Free Software Foundation; either version 3 of the License, or     #
#   (at your option) any later version.                                   #
#                                                                         #
#   This program is distributed in the hope that it will be useful,       #
#   but WITHOUT ANY WARRANTY; without even the implied warranty of        #
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         #
#   GNU General Public License for more details.                          #
#                                                                         #
#   You should have received a copy of the GNU General Public License     #
#   along with this program. If not, see <http://www.gnu.org/licenses/>   #

__author__ = 'Serge Poltavski'


import pdobject
from termcolor import colored
import six
import common


class PdColor:
    def __init__(self, r=0, g=0, b=0):
        assert isinstance(r, float) or isinstance(r, int)
        assert isinstance(g, float) or isinstance(g, int)
        assert isinstance(b, float) or isinstance(b, int)
        self._r = r
        self._g = g
        self._b = b

    @staticmethod
    def black():
        return PdColor(0, 0, 0)

    @staticmethod
    def white():
        return PdColor(255, 255, 255)

    def rgb(self):
        return self._r, self._g, self._b

    def set_rgb(self, rgb):
        self._r = rgb[0]
        self._g = rgb[1]
        self._b = rgb[2]

    def from_pd(self, value):
        v = abs(int(value) + 1)
        r = v / 4096
        g = (v % 4096) / 64
        b = (v % 4096) % 64
        self._r = int(round(r / 63.0 * 255)) % 256
        self._g = int(round(g / 63.0 * 255)) % 256
        self._b = int(round(b / 63.0 * 255)) % 256

    @staticmethod
    def from_hex(hex_str):
        c = PdColor()

        if hex_str[0] == '#':
            hex_str = hex_str[1:]

        if len(hex_str) == 6:
            r = int(hex_str[0:2], 16)
            g = int(hex_str[2:4], 16)
            b = int(hex_str[4:6], 16)
            c.set_rgb((r, g, b))
        elif len(hex_str) == 3:
            r = int(hex_str[0], 16) * 0x11
            g = int(hex_str[1], 16) * 0x11
            b = int(hex_str[2], 16) * 0x11
            c.set_rgb((r, g, b))
        else:
            assert False

        return c

    def compare(self, rgb):
        if isinstance(rgb, list) or isinstance(rgb, tuple):
            return self._r == rgb[0] and self._g == rgb[1] and self._b == rgb[2]
        elif isinstance(rgb, self.__class__):
            return self._r == rgb._r and self._g == rgb._g and self._b == rgb._b
        else:
            return False

    def is_black(self):
        return self.compare((0, 0, 0))

    def rgb_float(self):
        return self._r / 255.0, self._g / 255.0, self._b / 255.0

    def to_pd(self):
        return -4096 * int(round(self._r * (63 / 255.0))) \
               - 64 * int(round(self._g * (63 / 255.0))) \
               - 1 * int(round(self._b * (63 / 255.0))) - 1

    def to_hex_str(self):
        return "#{0:02X}{1:02X}{2:02X}".format(self._r, self._g, self._b)

    def __str__(self):
        res = colored("RGB[%i,%i,%i]" % (self._r, self._g, self._b), "green")
        return res

    def __eq__(self, other):
        return self.compare(other)

def color_from_str(value):
    c = PdColor()

    if isinstance(value, int):
        c.from_pd(value)
    elif isinstance(value, six.string_types):
        if value[0] == '#':
            return PdColor.from_hex(value)
        else:
            c.from_pd(value)
    else:
        assert False

    return c


class PdCoreGui(pdobject.PdObject):
    tgl_defaults = ['15', '0', 'empty', 'empty', 'empty', '17', '7', '0', '10', '-262144', '-1', '-1', '0', '1']

    POS_LEFT, POS_RIGHT, POS_TOP, POS_BOTTOM = (0, 1, 2, 3)

    def __init__(self, name, x, y, args, **kwargs):
        pdobject.PdObject.__init__(self, name, x, y, 0, 0, args)
        self._send = kwargs.get("send", "empty")
        self._receive = kwargs.get("send", "empty")
        self._label = kwargs.get("label", "empty")
        self._label_xoff = int(kwargs.get("label_xoff", 17))
        self._label_yoff = int(kwargs.get("label_yoff", 7))
        self._font_type = int(kwargs.get("font_type", 0))
        self._font_size = int(kwargs.get("font_size", 10))
        self._bg_color = color_from_str(kwargs.get("bg_color", -262144))
        self._fg_color = color_from_str(kwargs.get("fg_color", -1))
        self._label_color = color_from_str(kwargs.get("label_color", -1))

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, v):
        self._label = v

    @property
    def send(self):
        return self._send

    @send.setter
    def send(self, v):
        self._send = v

    def no_send(self):
        return not self._send or self.send == "empty"

    def no_label(self):
        return not self._label or self.label == "empty"

    @property
    def receive(self):
        return self._receive

    @receive.setter
    def receive(self, v):
        self._receive = v

    def no_receive(self):
        return not self._send or self.receive == "empty"

    def __str__(self):
        return "[GUI:%-36s {x:%i,y:%i,id:%i}" % (self.name + "]", self._x, self._y, self._id)

    def draw(self, painter):
        painter.draw_core_gui(self)

    def bgcolor(self):
        return self._bg_color.rgb_float()

    def fgcolor(self):
        return self._fg_color.rgb_float()

    def lbcolor(self):
        return self._label_color.rgb_float()

    def inlets(self):
        if self.no_receive():
            return [self.XLET_GUI]
        else:
            return []

    def outlets(self):
        if self.no_send():
            return [self.XLET_GUI]
        else:
            return []

    def traverse(self, visitor):
        visitor.visit_core_gui(self)

    def draw_xlets(self, painter):
        painter.draw_inlets(self.inlets(), self.x, self.y, self.width)
        painter.draw_outlets(self.outlets(), self.x, self.bottom, self.width)

    def _get_label_xy(self):
        return self.x + self._label_xoff, self.y + self._label_yoff  # font height correction

    def _get_label_pos(self, pos):
        if isinstance(pos, int):
            if pos not in (self.POS_LEFT, self.POS_TOP, self.POS_BOTTOM, self.POS_RIGHT):
                common.warning("invalid label position: {0:d}".format(pos))
                return None

            return pos
        elif isinstance(pos, six.string_types):
            lmap = { "left": self.POS_LEFT,
                    "right": self.POS_RIGHT,
                    "top": self.POS_TOP,
                    "bottom": self.POS_BOTTOM}

            if pos.lower() in lmap:
                return lmap[pos.lower()]
            else:
                common.warning("invalid label position: {0:s}".format(pos))
                return None
        else:
            common.warning("invalid label position: {0:s}".format(str(pos)))
            return None