# Date: 04/11/2018
# Author: Pure-L0G1C
# Description: Scrape a proxy site and store the data

from requests import get
from lib.queue import Queue
from bs4 import BeautifulSoup as bs 
from proxyChecker import CleanProxies

class Scrape(CleanProxies):

 def __init__(self, port=None, protocol=None, country=None, maxSize=None, cleanProxies=False):
  self.socks_proxies = 'https://socks-proxy.net'
  self.ssl_proxies = 'https://sslproxies.org'
  self.ip_checker = 'https://ip-api.io/json/'
  self.port = str(port) if port else None 
  self.cleanIP  = cleanProxies
  self.protocol = protocol
  self.maxSize  = maxSize  
  self.country  = country
  self.proxies  = Queue()
  self.isAlive  = True
  
  super(Scrape, self).__init__()

 def parse(self, proxy, ssl=False):
  detail = {'ip': proxy[0].string, 'port': proxy[1].string,
            'protocol': 'SSL' if ssl else proxy[4].string, 
            'anonymity': proxy[4 if ssl else 5].string, 
            'country': proxy[3].string,
            'updated': proxy[7].string,
            'https': proxy[6].string}

  if all([self.protocol, self.country, self.port]):
   if detail['protocol'].lower() == self.protocol.lower():
    if detail['country'].lower() == self.country.lower():
     if detail['port'] == self.port:
      return detail
  elif all([self.protocol, self.country]):
   if detail['protocol'].lower() == self.protocol.lower():
    if detail['country'].lower() == self.country.lower():
     return detail
  elif all([self.protocol, self.port]):
   if detail['protocol'].lower() == self.protocol.lower():
    if detail['port'] == self.port:
     return detail
  elif all([self.country, self.port]):
   if detail['country'].lower() == self.country.lower():
    if detail['port'].lower() == self.port:
     return detail
  elif self.protocol:
   return None if detail['protocol'].lower() != self.protocol.lower() else detail
  elif self.country:
   return None if detail['country'].lower() != self.country.lower() else detail
  elif self.port:
   return None if detail['port'] != self.port else detail
  else:
   return detail

 def fetch(self, url, ssl=False):
  try:proxies = bs(get(url).text, 'html.parser').find('tbody').findAll('tr')
  except:return

  for proxy in proxies:
   if not self.isAlive:break
   data = self.parse(proxy.findAll('td'), ssl)
   if data:
    if self.maxSize:
     if self.proxies.qsize < self.maxSize:
      if self.cleanIP:
       if self.isClean(data['ip']):
        self.proxies.put(data)
      else:self.proxies.put(data)
     else:break
    else:
     if self.cleanIP:
      if self.isClean(data['ip']):
       self.proxies.put(data)
     else:self.proxies.put(data)
 
 def scrape(self, fails=3):
  self.fetch(self.ssl_proxies, True)
  self.fetch(self.socks_proxies)

## Example I 
# n = Scrape()
# n.scrape()
# print n.proxies

## Example II, by port 
# n = Scrape(port=1080)
# n.scrape()
# print n.proxies

## Example III, by size 
# n = Scrape(maxSize=10)
# n.scrape()
# print n.proxies

## Example IV, by port and maxSize
# n = Scrape(port=1080, maxSize=3)
# n.scrape()
# print n.proxies

## Example V, by port, maxSize, clean
# n = Scrape(port=1080, maxSize=3, cleanProxies=True)
# n.scrape()
# print n.proxies