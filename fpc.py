
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
    def __init__(self, proxy, max_len):
        super(CheckProxyThread, self).__init__()
        self.proxy = proxy
        self.max_len = max_len

    def run(self):
        try:
            start = time.time()
            response = requests.get(url, proxies={"http": proxy, "https": self.proxy}, timeout=10)
            resp_code = response.status_code
            del response

            if resp_code < 400:
                end = time.time()
                req_time = round(end - start, 1)
                successful_proxies.update({self.proxy: str(req_time)})
                print(f"- Time of {add_indentation(self.proxy, self.max_len)} is\t{req_time}s AND Response Code is: {resp_code}")
            else:
                print(f"- {add_indentation(self.proxy, self.max_len)} is FAILED with response code: {resp_code}")

        except Exception as uee:
            print(f"- FAILED to connect to {add_indentation(self.proxy, self.max_len)}")
            pass

thread_limit = 10 if len(proxies) > 10 else len(proxies)


def add_indentation(proxy, max_len):
    ip_addr, port = proxy.split(":")
    padding = max_len - len(ip_addr)
    return " " * padding + proxy


def format_proxy_list(proxies):
    formatted_list = list()
    max_len = max(len(proxy.split(":")[0]) for proxy in proxies)

    for proxy in proxies:
        formatted_list.append(add_indentation(proxy, max_len))

    return formatted_list, max_len


if __name__ == "__main__":

    print(f">>> [ {str(len(proxies))} proxies found ]\n")
    formatted_list, max_len = format_proxy_list(proxies)
    for _, item in enumerate(formatted_list, 1):
        counter = f"{_}) "
        if len(str(_)) < 2:
            counter = f" {_}) "
        print(f"{counter} {item}")

    thread_list = list()
    thread_available = True

    while proxies:
        print(f"\n>>> [ Starting to check response time of proxies ]\n")
        while threading.active_count() <= thread_limit and proxies:
            proxy = proxies.pop()
            sub_thread = CheckProxyThread(proxy, max_len)
            sub_thread.daemon = True
            thread_list.append(sub_thread)
            sub_thread.start()

        for sub_thread in thread_list:
            sub_thread.join()

    sorted_successful_proxies = OrderedDict(
        sorted(
            successful_proxies.items(), key=lambda item: item[1]
        )
    )
    count = 0
    print("\n>>> [ ---- TOP 3 Proxies ---- ]\n")
    for key, val in sorted_successful_proxies.items():
        count += 1
        print(f"Address: {str(key)} \t-\t Time: {str(val)}s")
        if count == 3:
            break

