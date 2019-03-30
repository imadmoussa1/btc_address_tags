import requests
from bs4 import BeautifulSoup


class WebRequest:
  # web request with headers that browser send to a webpage
  @staticmethod
  def get_html(url, proxy):
    headers = {
      'Accept-Encoding': 'gzip, deflate, br',
      'Accept-Language': 'en-US,en;q=0.8',
      'Upgrade-Insecure-Requests': '1',
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
      'Cache-Control': 'max-age=0',
      'Connection': 'keep-alive'
    }
    # parse html using BeautifulSoup
    page = requests.get(url, headers=headers, proxies={"http": proxy, "https": proxy})
    html_result = BeautifulSoup(page.content, 'html.parser')

    return html_result
