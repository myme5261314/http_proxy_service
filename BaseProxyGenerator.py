#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 Peng Liu <liupeng@imscv.com>
#
# Distributed under terms of the GNU GPL3 license.

"""
This is the abstract class for the proxy server info gather.
"""

import time
import threading
from multiprocessing.pool import ThreadPool as Pool
import itertools


def proxy_check(proxy):
    return proxy.check()


def url_extract(pair_list):
    p_self = pair_list[0]
    url = pair_list[1]
    p_self.lock.acquire()
    result = [proxy for proxy in p_self.extract(url) if proxy is not None]
    p_self.lock.release()
    return result


class BaseProxyGenerator(threading.Thread):

    """Define Some data variables and common operations for various kinds of
    proxy generators."""

    def __init__(self, url_list=[]):
        """Initialize the common data variables.
        :url: this is the link to gather information of proxies.

        """
        threading.Thread.__init__(self)
        self.lock = threading.Lock()
        self.base_url = url_list
        self.proxy_dict = dict()

    def run(self):
        """TODO: Docstring for run.
        :returns: TODO

        """
        while True:
            try:
                self.gather()
            except Exception as e:
                print e
            print 'proxy dict is %s' % (self.get())
            print 'Start of sleep'
            time.sleep(3)
            print 'End of sleep'

    def gather(self):
        """Convert the gathered data and stored in the instance.
        :returns: dict of (hash, BaseProxy) pair.

        """
        page_num = len(self.base_url)
        assert(page_num > 0)
        p = Pool(len(self.base_url))
        proxy_list_list = p.map(url_extract, zip(
            [self] * page_num, self.base_url))
        proxy_list = list(itertools.chain.from_iterable(proxy_list_list))
        p.close()
        p = Pool(len(proxy_list))
        status_list = p.map(proxy_check, proxy_list)
        p.close()
        for i in xrange(len(status_list)):
            if status_list[i]:
                self.proxy_dict[proxy_list[i].data_dict['hash']] = proxy_list[i]

    def get(self):
        """TODO: Docstring for get.
        :returns: TODO

        """
        return self.proxy_dict

    @staticmethod
    def extract(url):
        """extract each page depends only on url which contains proxy info, so
        it's independent with instance.

        :url: TODO
        :returns: TODO

        """
        pass
