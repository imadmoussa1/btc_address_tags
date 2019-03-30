import _thread
import time

from lxml.html import fromstring
import requests
from itertools import cycle
import traceback
import json
from web_request import WebRequest


class WalletExplorer:

  # use proxy to fetch data
  def get_proxies(self):
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//tbody/tr')[:300]:
      if i.xpath('.//td[7][contains(text(),"yes")]'):
        proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
        proxies.add(proxy)
    return proxies

  # read link of tag category from json file
  def read_links(self, json_tag):
    proxies = self.get_proxies()
    print(proxies)
    proxy_pool = cycle(proxies)
    try:
      tag_type = json_tag["type"]
      for tag_list in json_tag["list"]:
        _thread.start_new_thread(self.parse_tag, (tag_list, tag_type, next(proxy_pool)))
    except Exception as e:
      print("Error: unable to start thread", e)
    while 1:
      pass

  def parse_tag(self, tag_list, tag_type, proxy):
    print(tag_list['link'])
    max_page_number = self.max_page(tag_list, proxy)
    a = 0
    for page_nub in range(1, max_page_number+1):
      while True:
        try:
          html_data = WebRequest.get_html("%s/addresses?page=%s" % (tag_list['link'], page_nub), proxy)
          table = html_data.find('table')
          wallet_links = table.find_all('a')
          for wallet_link in wallet_links:
            a += 1
            # own function to save tags
            print(wallet_link.text, tag_list['link'].split('wallet/', 2)[1], tag_list['link'], tag_type)
        except Exception as e:
          print("error ", e)
          continue
        break

  @staticmethod
  def max_page(tag_list, proxy):
    while True:
      try:
        html_data = WebRequest.get_html("%s/addresses" % tag_list['link'], proxy)
        list_href = html_data.find("div", class_="paging").find_all('a', href=True)
        return 1 if len(list_href) < 2 else int(list_href[1]['href'].split('=', 2)[1])
      except Exception as e:
        continue
