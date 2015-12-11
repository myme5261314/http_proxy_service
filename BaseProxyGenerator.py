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


class BaseProxyGenerator(object):

    """Define Some data variables and common operations for various kinds of
    proxy generators."""

    def __init__(self, url):
        """Initialize the common data variables.
        :url: this is the link to gather information of proxies.

        """
        self.base_url = url

    def gather(self):
        """Convert the gathered data and stored in the instance.
        :returns: dict of (hash, BaseProxy) pair.

        """
        proxy_dict = dict()
        if isinstance(self.base_url, list):
            for url in self.base_url:
                for proxy in self._extract(url):
                    proxy_dict[proxy.data_dict['hash']] = proxy
        elif isinstance(self.base_url, str):
            for proxy in self._extract(url):
                    proxy_dict[proxy.data_dict['hash']] = proxy
        else:
            raise Exception('Invalid url: %s', self.base_url)
        return proxy_dict

    def _extract(self, url):
        """TODO: extract info based on specific website structure and url.

        :returns: List of BaseProxy.

        """
        yield None
