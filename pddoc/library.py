#!/usr/bin/env python
# coding=utf-8
from lxml import etree
import logging
from pddoc.parser import get_parser
import os
#   Copyright (C) 2016 by Serge Poltavski                                 #
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


class LibraryMaker(object):
    NSMAP = {'xi': "http://www.w3.org/2001/XInclude"}

    def __init__(self, name):
        etree.register_namespace("xi", "http://www.w3.org/2001/XInclude")
        self._name = name
        self._lib = etree.Element("library", version="1.0", name=name, nsmap=self.NSMAP)
        self._cats = {}
        self._cat_entries = {}

    def process_files(self, files):
        for f in files:
            try:
                xml = etree.parse(f, get_parser())
            except etree.XMLSyntaxError as e:
                logging.error("XML syntax error:\n \"%s\"\n\twhile parsing file: \"%s\"", e, f)
                continue

            pddoc = xml.getroot()
            objects = filter(lambda x: x.tag == 'object', pddoc)
            for obj in objects:
                name = obj.get('name')
                descr = obj.find('meta/description').text
                # logging.info("[%s] doc found: %s", name, descr.text)
                categ = obj.find('meta/category')
                if categ is None:
                    self.add_to_others(f, name=name, descr=descr)
                else:
                    self.add_to_cat(categ.text, f, name=name, descr=descr)

                lib = obj.find('meta/library').text
                if lib != self._name:
                    logging.warning("library differs in file: '%s': %s != %s", f, self._name, lib)

            del xml

    def __str__(self):
        xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
        return xml + etree.tostring(self._lib, pretty_print=True)

    def add_to_others(self, fname, **kwargs):
        self.add_to_cat('others', fname, **kwargs)

    def add_to_cat(self, cat_name, fname, **kwargs):
        # first time add new category
        if cat_name not in self._cats:
            c = etree.Element('category', name=cat_name)
            cat_info_path = "{0}.xml".format(cat_name)
            if os.path.exists(cat_info_path):
                c.append(self.xi_include(os.path.basename(cat_info_path)))

            self._cats[cat_name] = c
            self._lib.append(c)
            self._cat_entries[cat_name] = {}

        # check for already added object
        if kwargs['name'] in self._cat_entries[cat_name]:
            logging.warning('object %s already in library', kwargs['name'])
            return

        self._cat_entries[cat_name][kwargs['name']] = True

        entry = etree.Element('entry', **kwargs)
        entry.append(self.xi_include(os.path.basename(fname)))
        self._cats[cat_name].append(entry)

    def xi_include(self, fname):
        return etree.Element('{http://www.w3.org/2001/XInclude}include', href=fname, parse="xml")

    def sort_cat(self, cat):
        entries = cat.findall('entry')
        sorted_entries = sorted(entries, key=lambda x: x.get('name'))

        for child in entries:
            cat.remove(child)

        for child in reversed(sorted_entries):
            cat.insert(0, child)

    def sort(self):
        cats = self._lib.findall('category')
        sorted_cats = sorted(cats, key=lambda x: x.get('name'))

        for child in cats:
            self._lib.remove(child)

        for child in reversed(sorted_cats):
            self.sort_cat(child)
            self._lib.insert(0, child)



