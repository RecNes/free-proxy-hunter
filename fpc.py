#!/usr/bin/env python
# coding: utf-8

import threading
import time
from collections import OrderedDict

import requests
from lxml.html import fromstring


def get_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)

    parser = fromstring(response.text)
    proxies = set()
    yes_counter = 0
    for i in parser.xpath('//tbody/tr')[:100]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
            yes_counter += 1
        if yes_counter == 10:
            break
    return proxies

proxies = list(get_proxies())
url = 'https://httpbin.org/ip'
successful_proxies = dict()


class CheckProxyThread(threading.Thread):
    def __init__(self, proxy):
        super(CheckProxyThread, self).__init__()
        self.proxy = proxy

    def run(self):
        print(f"Starting to check response time of proxies")
        try:
            start = time.time()
            response = requests.get(url, proxies={"http": proxy, "https": self.proxy}, timeout=10)
            del response
            end = time.time()
            successful_proxies.update({end - start: self.proxy})
            print(f"Time of {self.proxy} is:\t{end-start}")
        except Exception as uee:
            pass

thread_limit = 10 if len(proxies) > 10 else len(proxies)

if __name__ == "__main__":
    print("{} proxies found".format(str(len(proxies))))
    for item in proxies:
        print(item)
    thread_list = list()
    thread_available = True

    while proxies:
        while threading.active_count() <= thread_limit and proxies:
            proxy = proxies.pop()
            sub_thread = CheckProxyThread(proxy)
            sub_thread.daemon = True
            thread_list.append(sub_thread)
            sub_thread.start()

        for sub_thread in thread_list:
            sub_thread.join()

    sorted_successful_proxies = OrderedDict(sorted(successful_proxies.items()))
    count = 0
    print("---- TOP 3 Proxies ----")
    for key, val in sorted_successful_proxies.items():
        count += 1
        print("Address: {} - Time: {}".format(str(val), str(key)))
        if count == 3:
            break

