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


class MainHandler(tornado.web.RequestHandler):

    def get(self):
        # self.write("Hello, world")
        b = requests.get('http://www.baidu.com')
        self.write(b.text.encode('utf-8'))


class BookHandler(tornado.web.RequestHandler):

    """handle book page."""

    def get(self):
        """TODO: to be defined1. """
        tornado.web.R.__init__(self)


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
