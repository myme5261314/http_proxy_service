#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 Peng Liu <liupeng@imscv.com>
#
# Distributed under terms of the GNU GPL3 license.

"""
This is the generator for website http://www.kuaidaili.com/proxylist/[1-10]
"""

import time
import requests as rs
from bs4 import BeautifulSoup as bs
from multiprocessing.pool import ThreadPool
from BaseProxyGenerator import BaseProxyGenerator
from BaseProxy import BaseProxy
import random


def wrapper(infos):
    return BaseProxy(infos)


class KuaidailiProxyGenerator(BaseProxyGenerator):

    """Docstring for KuaidailiProxyGenerator. """

    def __init__(self):
        """TODO: to be defined1. """
        template = 'http://www.kuaidaili.com/proxylist/%d'
        super(KuaidailiProxyGenerator, self).__init__(
            [template % i for i in xrange(1, 11)])

    @staticmethod
    def extract(url):
        """TODO: Docstring for extract.
        :returns: TODO

        """
        try:
            sleep_time = random.uniform(0, 3)
            print sleep_time
            time.sleep(sleep_time)
            r = rs.get(url)
            soup = bs(r.text, 'html.parser')
            tr_list = soup.tbody.find_all('tr')
        except AttributeError:
            print r
            return None
        info_list = []
        for tr in tr_list:
            td_list = tr.find_all('td')
            if td_list[2].text.strip() == u'高匿名' and\
                    'HTTP' in td_list[3].text.strip(' ').split(',') and\
                    'GET' in td_list[4].text.strip(' ').split(','):
                infos = list()
                infos.append(td_list[0].text.strip())
                infos.append(td_list[1].text.strip())
                infos.append(td_list[6].text.strip()[:-1])
                if td_list[7].text.find(u'小时') != -1:
                    infos.append(float(td_list[7].text[:-3]) * 3600)
                else:
                    infos.append(float(td_list[7].text[:-3]) * 60)
                info_list.append(infos)
        p = ThreadPool(len(info_list))
        start = time.time()
        proxy_list = p.map(wrapper, info_list)
        p.close()
        print time.time() - start
        return proxy_list


def main():
    """TODO: Docstring for main.

    :arg1: TODO
    :returns: TODO

    """
    k = KuaidailiProxyGenerator()
    print k.gather()


if __name__ == "__main__":
    main()
