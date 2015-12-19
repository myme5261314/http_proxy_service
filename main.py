#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 Peng Liu <liupeng@imscv.com>
#
# Distributed under terms of the GNU GPL3 license.

"""

"""
import tornado.ioloop
import tornado.web
import requests
import random

from KuaidailiProxyGenerator import KuaidailiProxyGenerator
from XicidailiProxyGenerator import XicidailiProxyGenerator


class MainHandler(tornado.web.RequestHandler):

    def get(self):
        used_proxy = random.choice(k.get().values()).data_dict['hash']
        print 'Used proxy: %s' % used_proxy
        b = requests.get('http://www.baidu.com',
                         proxies={'http': 'http://' + used_proxy})
        self.write(b.text.encode('utf-8'))


class BookHandler(tornado.web.RequestHandler):

    """handle book page."""

    def get(self, bookid):
        """TODO: to be defined1. """
        used_proxy = random.choice(k.get().values())
        print used_proxy
        used_proxy = used_proxy.data_dict['hash']
        print 'Used proxy: %s' % used_proxy
        b = requests.get('http://book.douban.com/subject/%s' % bookid,
                         proxies={'http': 'http://' + used_proxy})
        self.write(b.text.encode('utf-8'))


class LinkHandler(tornado.web.RequestHandler):

    """handle url."""

    def get(self, url):
        """TODO: to be defined1. """
        used_proxy = random.choice(k.get().values())
        used_proxy = used_proxy.data_dict['hash']
        b = requests.get(url, proxies={'http': 'http://' + used_proxy})
        self.write(b.text.encode('utf-8'))


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/book/([0-9]+)", BookHandler),
        (r"/(http://.+)", LinkHandler)
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    k = KuaidailiProxyGenerator()
    x = XicidailiProxyGenerator()
    k.start()
    x.start()
    tornado.ioloop.IOLoop.current().start()
