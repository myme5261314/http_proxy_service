#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 Peng Liu <liupeng@imscv.com>
#
# Distributed under terms of the GNU GPL3 license.

"""
This is the base class for the proxy server information.
"""

import requests as rs
from bs4 import BeautifulSoup as bs
import time


class BaseProxy(object):

    """Docstring for BaseProxy. """

    def __init__(self, content_list):
        """TODO: to be defined1. """
        self.data_dict = dict()
        self.data_dict['ip'] = content_list[0]
        self.data_dict['port'] = int(content_list[1])
        self.data_dict['response_time'] = float(content_list[2])
        self.data_dict['verify_time'] = time.time() - float(content_list[3])
        self.data_dict['hash'] = self.data_dict[
            'ip'] + ":" + str(self.data_dict['port'])
        self.data_dict['usable'] = False

    def check(self):
        """Check whether proxy server is usable.

        :returns: True for usable and False for unusable.

        """
        url = 'http://www.baidu.com'
        valid_text = u'百度一下，你就知道'
        start = time.time()
        try:
            r = rs.get(url, timeout=5, proxies={'http': self.get_proxy_link()})
        except rs.exceptions.RequestException:
            self.data_dict['usable'] = False
            return False
        response_time = time.time() - start
        if response_time > 3 or r.status_code != 200 or r.reason != 'OK':
            self.data_dict['usable'] = False
            return False
        soup = bs(r.text, 'html.parser')
        if soup.title.text != valid_text:
            self.data_dict['usable'] = False
            return False
        else:
            self.data_dict['usable'] = True
            self.data_dict['response_time'] = response_time
            self.data_dict['verify_time'] = time.time()
            return True

    def get_status(self):
        """TODO: Docstring for get_status.

        :returns: TODO

        """
        return self.data_dict['usable']

    def get_proxy_link(self):
        """return the link string for proxy to use.
        :returns: TODO

        """
        return 'http://%s:%d' % (self.data_dict['ip'], self.data_dict['port'])
