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
        # Make sure the 'hash' and 'usable' entries are always the first two
        # entry of the list.
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
        if self.data_dict['response_time'] > 3:
            self.data_dict['usable'] = False
            return False
        else:
            url = 'http://www.baidu.com'
            start = time.time()
            try:
                soup = bs(
                    rs.get(url, timeout=3,
                           proxies={'http': 'http://%s:%d' % (
                               self.data_dict['ip'],
                               self.data_dict['port'])}).text,
                    'html.parser')
            except rs.exceptions.Timeout:
                self.data_dict['usable'] = False
                return False
            except rs.exceptions.ConnectionError:
                self.data_dict['usable'] = False
                return False
            if soup.title.text != u'百度一下，你就知道':
                self.data_dict['usable'] = False
                return False
            else:
                print self.data_dict['ip'] + ':' + str(self.data_dict['port'])
                self.data_dict['usable'] = True
                self.data_dict['response_time'] = time.time() - start
                print self.data_dict['response_time']
                return True

    def get_status(self):
        """TODO: Docstring for get_status.

        :returns: TODO

        """
        return self.data_dict['usable']
