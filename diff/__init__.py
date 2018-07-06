# -*- coding: utf-8 -*-
import copy
import re

from bidict import bidict
import diff_match_patch as dmp_module
from lxml.html import fragment_fromstring


UNICODE_KEY = [unichr(item) for item in range(0xE000, 0xFFFF + 1)]
# unicode spec not in use
DMP = dmp_module.diff_match_patch()


TAG_RE = re.compile('</?\w+[^>]*>')


class ContentDiff(object):

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
                element = fragment_fromstring(tag)
                if element.tag in ('img', 'a', 'video', 'audio'):
                    self._map_media_tag(element, tag)
                else:
                    self.tag_map[self.code_key.pop()] = tag

    def _map_media_tag(self, element, raw_tag):
        url = get_url(element)
        if url in self.media_url.values():
            code = self.media_url.inv[url]
            self.tag_map[code].append(raw_tag)
            return
        code = self.code_key.pop()
        self.tag_map[code] = [raw_tag]
        self.media_url[code] = url

    def _replace(self, new_content, old_content):
        self._map_tag(new_content)
        self._map_tag(old_content)
        for code, tag in self.tag_map.iteritems():
            if not isinstance(tag, list):
                tag = [tag]
            for item in tag:
                new_content = new_content.replace(item, code)
        for code, tag in self.tag_map.iteritems():
            if not isinstance(tag, list):
                tag = [tag]
            for item in tag:
                old_content = old_content.replace(item, code)
        return to_unicode(new_content), to_unicode(old_content)

    def _recover(self, content):
        for code, tag in self.tag_map.iteritems():
            if isinstance(tag, list):
                tag = tag[0]
            content = content.replace(code, tag)
        return content

    def diff(self):
        new_content, old_content = self._replace(self.new_content, self.old_content)
        content = diff_text(old_content, new_content)
        return self._recover(content)


def get_url(element):
    if element.tag == 'a':
        return element.attrib.get('href')
    elif element.tag == 'img':
        return element.attrib.get('src')
    elif element.tag in ('video', 'audio'):
        children = element.getchildren()
        if children:
            return children[0].get('src')
    return ''


def diff_text(old_text, text, output_html=True):
    diffs = DMP.diff_main(to_unicode(old_text), to_unicode(text))
    if output_html:
        return pretty_html(diffs)
    return diffs


def pretty_html(diffs):
    html = []
    for (op, data) in diffs:
        text = data
        if op == 1:
            html.append("<ins style=\"background:#e6ffe6;\">%s</ins>" % text)
        elif op == -1:
            html.append("<del style=\"background:#ffe6e6;\">%s</del>" % text)
        elif op == 0:
            html.append("%s" % text)
    return "".join(html)


_TO_UNICODE_TYPES = (unicode, type(None))


def to_unicode(value):
    if isinstance(value, _TO_UNICODE_TYPES):
        return value
    if not isinstance(value, bytes):
        raise TypeError(
            "Expected bytes, unicode, or None; got %r" % type(value)
        )
    return value.decode("utf-8")
