# -*- coding: utf-8 -*-
import copy
import sys
import logging
import re

from bidict import bidict
import diff_match_patch as dmp_module
from lxml.html import fromstring, tostring, fragment_fromstring
from lxml import etree

if sys.version_info < (3,):
    chr = unichr
    unicode_type = unicode
else:
    unicode_type = str

UNICODE_KEY = [chr(item) for item in range(0xE000, 0xFFFF + 1)]
# unicode spec not in use
DMP = dmp_module.diff_match_patch()


TAG_RE = re.compile('</?\w+[^>]*>')


class ContentDiff(object):

    INSERT = 1
    DELETE = -1
    EQUAL = 0

    def __init__(self, new_content, old_content):
        self.new_content = to_unicode(new_content)
        self.old_content = to_unicode(old_content)
        self.tag_map = {}
        self.media_url = bidict()
        self.code_key = copy.deepcopy(UNICODE_KEY)

    def _map_tag(self, content):
        tags = TAG_RE.findall(content)
        for tag in tags:
            if tag[1] == '/':
                if tags not in self.tag_map.values():
                    self.tag_map[self.code_key.pop()] = tag
            else:
                element = fromstring(tag)
                if element.tag in ('img', 'a', 'video', 'audio'):
                    self._map_media_tag(element, tag)
                else:
                    self.tag_map[self.code_key.pop()] = tag

    def _map_media_tag(self, element, raw_tag):
        tag_key = gen_tag_key(element.attrib)
        if tag_key in self.media_url.values():
            code = self.media_url.inv[tag_key]
            self.tag_map[code].append(raw_tag)
            return
        code = self.code_key.pop()
        self.tag_map[code] = [raw_tag]
        self.media_url[code] = tag_key

    def _replace(self, new_content, old_content):
        self._map_tag(new_content)
        for code, tag in self.tag_map.items():
            if not isinstance(tag, list):
                tag = [tag]
            for item in tag:
                new_content = new_content.replace(item, code)
        for code, tag in self.tag_map.items():
            if not isinstance(tag, list):
                tag = [tag]
            for item in tag:
                old_content = old_content.replace(item, code)
        return to_unicode(new_content), to_unicode(old_content)

    def _recover(self, content):
        for code, tag in self.tag_map.items():
            if isinstance(tag, list):
                tag = tag[0]
            content = content.replace(code, tag)
        return ensure_closed_tag(content)

    def diff(self):
        if self.new_content == self.old_content:
            return self.new_content
        new_content, old_content = self._replace(self.new_content, self.old_content)
        content = self._diff(old_content, new_content)
        return content

    def _diff(self, old_content, new_content):
        diffs = DMP.diff_main(to_unicode(old_content), to_unicode(new_content))
        html = []
        for (op, data) in diffs:
            text = self._recover(data)
            if op == self.INSERT:
                html.append("<ins style=\"background:#e6ffe6;\">{}</ins>".format(text))
            elif op == self.DELETE:
                html.append("<del style=\"background:#ffe6e6;\">{}</del>".format(text))
            elif op == self.EQUAL:
                html.append(text)
        return "".join(html)


_TO_UNICODE_TYPES = (unicode_type, type(None))


def to_unicode(value):
    if isinstance(value, _TO_UNICODE_TYPES):
        return value
    if not isinstance(value, bytes):
        raise TypeError(
            "Expected bytes, unicode, or None; got %r" % type(value)
        )
    return value.decode("utf-8")


def ensure_closed_tag(html):
    try:
        element = fromstring(html)
    except etree.ParserError as e:
        logging.warn('fromstring error: {}, use fragment_fromstring'.format(e))
        element = fragment_fromstring(html, create_parent='div')
    return to_unicode(tostring(element, encoding='utf-8'))


def gen_tag_key(query):
    l = ["{}={}".format(to_unicode(k), to_unicode(v)) for k, v in query.items()]
    return '&'.join(l)
