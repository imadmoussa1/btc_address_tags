import time

import requests
from lxml import html
from bs4 import BeautifulSoup
import json
from web_request import WebRequest


class BlockchainInfo:

  def read_links(self):
    _filters = [
      {'id': 4, 'type': 'Bitcoin-OTC Profiles'},
      {'id': 2, 'type': 'BitcoinTalk Profiles'},
      {'id': 8, 'type': 'Submitted Links'},
      {'id': 16, 'type': 'Signed Messages'}
      ]
    source_uri = "https://www.blockchain.com"
    for tag_filter in _filters:
      max_offset_number = self.max_page(source_uri, tag_filter)
      a = 0
      for offset_nub in range(0, max_offset_number, 50):
        html_data = WebRequest.get_html("%s/btc/tags?filter=%s&offset=%s" % (source_uri, tag_filter['id'], offset_nub))
        table = html_data.find('table', class_="table table-striped")
        table_line = table.find_all('tr')
        for wallet_info in table_line:
          cols = wallet_info.find_all('td')
          a += 1
          address = cols[0].find('a').text
          tag = cols[1].find('span').text
          tag_uri = cols[2].find('a').text
          category = tag_filter['type']
          print(address, tag, tag_uri, category)
          # fct to save the data
        
  @staticmethod
  def max_page(source_uri, filter):
    html_data = WebRequest.get_html("%s/btc/tags?filter=%s" % (source_uri, filter))
    return int([href['href'].split('offset=')[1] for href in html_data.find("ul", class_="pagination").find_all('a', href=True) if href.text=="≥"][0])
