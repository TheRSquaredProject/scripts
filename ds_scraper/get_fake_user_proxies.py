# -*- coding: utf-8 -*-

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import random
from get_fake_user_agent import getRandomUserAgent

ua = getRandomUserAgent()
#ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396 Safari/537.36'
proxies = [] # Will contain proxies [ip, port]


def getProxy():
    proxies_req = Request('https://www.sslproxies.org/')
    proxies_req.add_header('User-Agent', ua)
    proxies_doc = urlopen(proxies_req).read().decode('utf8')

    soup = BeautifulSoup(proxies_doc, 'html.parser')
    proxies_table = soup.find(id='proxylisttable')

    # Save proxies in the array
    for row in proxies_table.tbody.find_all('tr'):
        proxies.append({
                'ip':   row.find_all('td')[0].string,
                'port': row.find_all('td')[1].string
                })

    # Choose a random proxy
    proxy_index = random_proxy()
    proxy = proxies[proxy_index]
    
    spoofedProxyWithPort = proxy['ip']+ ":" + proxy['port'] #need to refactor
    proxy = {"http": f"http://{str(spoofedProxyWithPort)}"}
    
    return proxy

def random_proxy():
  return random.randint(0, len(proxies) - 1)
