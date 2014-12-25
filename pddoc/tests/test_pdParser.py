#!/usr/bin/env python
# coding=utf-8

# Copyright (C) 2014 by Serge Poltavski                                 #
#   serge.poltavski@gmail.com                                             #
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

from unittest import TestCase

__author__ = 'Serge Poltavski'

from pddoc.pdparser import *


class TestPdParser(TestCase):
    def test_init(self):
        p = PdParser()
        self.assertFalse(p.parse(""))

    # def test_parse_canvas(self):
    #     self.fail()
    #
    # def test_current_canvas(self):
    #     self.fail()
    #
    # def test_parse_frameset(self):
    #     self.fail()
    #
    # def test_parse_messages(self):
    #     self.fail()
    #
    # def test_parse_comments(self):
    #     self.fail()
    #
    # def test_parse_restore(self):
    #     self.fail()
    #
    # def test_parse_obj(self):
    #     self.fail()
    #
    # def test_parse_connect(self):
    #     self.fail()
    #
    # def test_parse_objects(self):
    #     self.fail()
    #
    # def test_parse_atoms(self):
    #     self.fail()

    def test_parse_objects(self):
        p = PdParser()
        self.assertTrue(p.parse("objects.pd"))
        cnv = p.canvas
        self.assertEqual(len(cnv.objects), 23)


    def test_parse_comments(self):
        p = PdParser()
        self.assertTrue(p.parse("comments.pd"))
        cnv = p.canvas
        self.assertEqual(len(cnv.objects), 3)

    def test_parse_connections(self):
        p = PdParser()
        self.assertTrue(p.parse("connections.pd"))
        cnv = p.canvas
        self.assertEqual(len(cnv.objects), 12)
        self.assertEqual(len(cnv.connections), 12)

    def test_parse_core_gui(self):
        p = PdParser()
        self.assertTrue(p.parse("core_gui.pd"))
        cnv = p.canvas
        self.assertEqual(len(cnv.objects), 3)
        self.assertEqual(len(cnv.connections), 2)