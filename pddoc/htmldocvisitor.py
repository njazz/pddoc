#!/usr/bin/env python
# coding=utf-8

# Copyright (C) 2014 by Serge Poltavski                                 #
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

import os.path
import os
import cairopainter
from mako.template import Template

import pddrawer
from docobject import *
from pdlayout import *


class HtmlDocVisitor(object):
    image_output_dir = "./out"

    def __init__(self):
        self._title = ""
        self._description = ""
        self._keywords = []
        self._website = ""
        self._library = ""
        self._category = ""
        self._version = ""
        self._license = {}
        self._aliases = []
        self._see_also = []
        self._examples = []
        self._authors = []
        self._contacts = ""
        self._inlets = {}
        self._outlets = {}
        self._arguments = []
        self._inlet_counter = 0
        self._image_counter = 0
        self._css_theme = "../theme.css"
        # template config
        tmpl_path = "{0:s}/share/html_object.tmpl".format(os.path.dirname(__file__))
        # self._tmpl_lookup = TemplateLookup(directories=[os.path.dirname(__file__)])
        self._html_template = Template(filename=tmpl_path)
        self._layout = PdLayout()
        self._canvas_padding = 10

    def title_begin(self, t):
        self._title = t.text()

    def website_begin(self, w):
        self._website = w.text()

    def keywords_begin(self, k):
        self._keywords = k.keywords()

    def description_begin(self, d):
        self._description = d.text()

    def aliases_begin(self, a):
        self._aliases += a.aliases()

    def license_begin(self, l):
        self._license['url'] = l.url()
        self._license['name'] = l.name()

    def library_begin(self, lib):
        self._library = lib.text()

    def category_begin(self, cat):
        self._category = cat.text()

    def version_begin(self, v):
        self._version = v.text()

    def author_begin(self, author):
        self._authors.append(author.text())

    def contacts_begin(self, cnt):
        self._contacts = cnt.text()

    def see_begin(self, see):
        dict = {'name' : see.text()}
        dict['image'] = "object_{0:s}.png".format(see.text())
        dict['link'] = "{0:s}.html".format(see.text())
        self._see_also.append(dict)

    def make_image_id_name(self):
        self._image_counter += 1
        cnt = self._image_counter
        path = os.path.join(HtmlDocVisitor.image_output_dir, "image_{0:02d}.png".format(self._image_counter))
        return cnt, path

    def pdexample_begin(self, tag):
        self._layout.canvas = pd.Canvas(0, 0, 10, 10, name="10")
        self._layout.canvas.type = pd.Canvas.TYPE_WINDOW

    def pdexample_end(self, tag):
        img_id, img_path = self.make_image_id_name()
        # append data to template renderer
        self._pd_append_example(img_id, img_path, None, tag.title())
        # update layout - place all objects
        self._layout.update()
        # draw image
        w, h = self.draw_area_size(tag)
        self._pd_draw(w, h, img_path)

    def pdinclude_begin(self, tag):
        assert isinstance(tag, DocPdinclude)

        if not os.path.exists(tag.file()):
            logging.error("Error in tag <pdinclude>: file not exists: \"{0:s}\"".format(tag.file()))
            return

        parser = pd.PdParser()
        if not parser.parse(tag.file()):
            tag.set_invalid()
            logging.error("Error in tag <pdexample>: can't process file: {0:s}".format(tag.file()))

        self._layout.canvas = parser.canvas
        img_id, img_path = self.make_image_id_name()
        # append data to template renderer
        self._pd_append_example(img_id, img_path, tag.file(), tag.file())

        # TODO auto layout
        w, h = self._layout.canvas_brect()[2:]
        self._pd_draw(w, h, img_path)

    def _pd_append_example(self, img_id, img_path, pd_path="", title=""):
        example_dict = {
            'id': img_id,
            'image': img_path,
            'title': title,
            'file': pd_path
        }

        self._examples.append(example_dict)

    def _pd_draw(self, w, h, fname):
        painter = cairopainter.CairoPainter(w, h, fname,
                                            xoffset=self._canvas_padding,
                                            yoffset=self._canvas_padding)
        self._layout.canvas.draw(painter)
        logging.info("image [{0:d}x{1:d}] saved to: \"{2:s}\"".format(w, h, fname))

    def pdcomment_begin(self, comment):
        self._layout.comment(comment)

    def row_begin(self, row):
        self._layout.row_begin()

    def row_end(self, row):
        self._layout.row_end()

    def col_begin(self, col):
        self._layout.col_begin()

    def col_end(self, col):
        self._layout.col_end()

    def pdmessage_begin(self, msg_obj):
        self._layout.message_begin(msg_obj)

    def pdobject_begin(self, doc_obj):
        self._layout.object_begin(doc_obj)

    def draw_area_size(self, pdxmpl):
        assert isinstance(pdxmpl, DocPdexample)

        w = 0
        h = 0

        if pdxmpl.file() and pdxmpl.size() == "canvas":
            w, h = self._layout.canvas_brect()[2:]
        elif pdxmpl.size() == "auto":
            w, h = self._layout.layout_brect()[2:]
        elif not pdxmpl.size():
            w = pdxmpl.width()
            h = pdxmpl.height()

            if not w:
                w = self._layout.layout_brect()[2]
            if not h:
                h = self._layout.layout_brect()[3]
        else:
            w, h = self._layout.layout_brect()[2:]

        return int(w + 2 * self._canvas_padding), int(h + 2 * self._canvas_padding)

    def pdconnect_begin(self, c):
        self._layout.connect_begin(c)

    def inlets_begin(self, inlets):
        self._inlets = inlets.inlet_dict()

    def outlets_begin(self, outlets):
        self._outlets = outlets.outlet_dict()

    def arguments_begin(self, args):
        self._arguments = args.items()

    def generate_object_image(self, name):
        fname = os.path.join(HtmlDocVisitor.image_output_dir, "object_{0:s}.png".format(name))
        if os.path.exists(fname):
            return

        pdo = pd.make_by_name(name)
        brect = pd.BRectCalculator().object_brect(pdo)
        pad = 1  # pixel
        painter = cairopainter.CairoPainter(int(brect[2]) + pad, int(brect[3]) + pad, fname, "png")
        pdo.draw(painter)

    def generate_images(self):
        try:
            if not os.path.exists(HtmlDocVisitor.image_output_dir):
                os.makedirs(HtmlDocVisitor.image_output_dir)

            if not os.path.isdir(HtmlDocVisitor.image_output_dir):
                raise RuntimeError("not a directory: %s".format(HtmlDocVisitor.image_output_dir))

            if self._aliases:
                for a in [self._title] + self._aliases:
                    self.generate_object_image(a)

            if self._see_also:
                for sa in self._see_also:
                    self.generate_object_image(sa['name'])
        except Exception, e:
            logging.error("Error while generating images: %s", e)

    def render(self):
        return self._html_template.render(
            title=self._title,
            description=self._description,
            keywords=self._keywords,
            image_dir='.',
            css_theme=self._css_theme,
            aliases=[self._title] + self._aliases,
            license=self._license,
            version=self._version,
            examples=self._examples,
            inlets=self._inlets,
            outlets=self._outlets,
            arguments=self._arguments,
            see_also=self._see_also,
            website=self._website,
            authors=self._authors,
            contacts=self._contacts,
            library=self._library,
            category=self._category)