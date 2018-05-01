# Date: 04/13/2018
# Author: Pure-L0G1C
# Description: Get clean proxies without getting a 429 error

import socks
import socket
import lib.proxyScraper
from requests import get
from lib.queue import Queue
from const import MAX_REQUESTS, PROXY_TIME_OUT

class CleanProxies(object):
 def __init__(self):
  self.proxy = None
  self.IDs = Queue()
  self.isAlive = True
  self.requestsMade = 0
  self.msgDisplay = False

 def isClean(self, ip, fails=3):
  if any([self.requestsMade == MAX_REQUESTS, not self.proxy]):self.changeID()
  try:
   if not self.isAlive:return
   self.requestsMade += 1
   stat = get(self.ip_checker + ip, proxies=self.proxy).json()['suspicious_factors']
   return not all([stat['is_proxy'], stat['is_suspicious'], stat['is_tor_node'], stat['is_spam']]) 
  except:
   if fails:self.isClean(ip, fails-1)
   else:self.changeID()

 def changeID(self):
  # bypass 429 error 
  if not self.isAlive:return 
  self.requestsMade = 0
  if not self.msgDisplay:
   print '[!] Searching for secure proxies ...' 
   self.msgDisplay = True

  if not self.IDs.qsize:self.scrapeProxies()

  proxy = self.IDs.get()
  try:self.proxy = {'https': 'http://{}:{}'.format(proxy['ip'], proxy['port'])} 
  except:pass   

 def scrapeProxies(self):
  scraper = lib.proxyScraper.Scrape(maxSize=10, protocol='SSL')
  scraper.scrape()
  while all([self.isAlive, scraper.proxies.qsize]):
   self.IDs.put(scraper.proxies.get())