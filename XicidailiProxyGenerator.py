#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 Peng Liu <liupeng@imscv.com>
#
# Distributed under terms of the GNU GPL3 license.

"""
This is the generator for website http://www.xicidaili.com/nn/[1-10]
"""

import time
import requests as rs
from bs4 import BeautifulSoup as bs
from multiprocessing.pool import ThreadPool as Pool
from BaseProxyGenerator import BaseProxyGenerator
from BaseProxy import BaseProxy


header = {
    # 'Host': 'www.xicidaili.com',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,' +
    'image/webp,*/*;q=0.8',
    # 'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36' +
    '(KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36',
    # 'Referer': 'http://www.xicidaili.com/nn/',
    # 'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Encoding': '',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6'
}


def wrapper(infos):
    return BaseProxy(infos)


class XicidailiProxyGenerator(BaseProxyGenerator):

    """Docstring for XicidailiProxyGenerator. """

    def __init__(self):
        """TODO: to be defined1. """
        super(XicidailiProxyGenerator, self).__init__()
        template = 'http://www.xicidaili.com/nn/%d'
        self.base_url = [template % i for i in xrange(1, 11)]

    @staticmethod
    def extract(url):
        """TODO: Docstring for extract.
        :returns: TODO

        """
        try:
            r = rs.get(url, headers=header)
            soup = bs(r.text, 'html.parser')
            tr_list = soup.table.find_all('tr')[1:]
        except AttributeError:
            print r
            return None
        info_list = []
        for tr in tr_list:
            td_list = tr.find_all('td')
            if td_list[5].text.strip() == u'高匿' and\
                    'HTTP' in td_list[6].text.strip(' ').split(','):
                infos = list()
                infos.append(td_list[2].text.strip())
                infos.append(td_list[3].text.strip())
                infos.append(
                    float(td_list[7].div['title'][:-1]) +
                    float(td_list[8].div['title'][:-1])
                )
                infos.append(
                    time.time() - time.mktime(
                        time.strptime(td_list[-1].text, '%y-%m-%d %H:%M')
                    )
                )
                info_list.append(infos)
        p = Pool(len(info_list))
        proxy_list = p.map(wrapper, info_list)
        p.close()
        return proxy_list


def main():
    """TODO: Docstring for main.

    :arg1: TODO
    :returns: TODO

    """
    k = XicidailiProxyGenerator()
    k.gather()
    print k.get()


if __name__ == "__main__":
    main()
