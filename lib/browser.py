# Date: 04/13/2018
# Author: Pure-L0G1C
# Description: Browser

from random import choice
from lib.queue import Queue 
from os import remove, path
from threading import Thread 
from time import sleep, time  
from selenium import webdriver
from lib.const import DEBUG_LOG
from lib.const import USER_AGENTS
from lib.const import DRIVER_PATH
from lib.proxyScraper import Scrape 
from lib.const import MIN_WATCH_TIME
from lib.const import MAX_WATCH_TIME

class Viewer(object):
 def __init__(self, url, views, visits=0): 
  self.recentProxies = Queue()
  self.proxies = Queue()
  self.renewDriver = True
  self.isActive = True
  self.isAlive = True
  self.views = views
  self.visits = visits
  self.url = url
  self.scraper = Scrape(maxSize=30,
                        protocol='SSL', 
                        cleanProxies=True)

 def proxiesManager(self):
  while self.isAlive:
   while all([self.isAlive, self.proxies.qsize]):
    [sleep(1) for _ in range(10) if self.isAlive if self.proxies.qsize]
    self.collect()
   if self.isAlive:    
    Thread(target=self.scraper.scrape).start()
    while all([self.isAlive, self.scraper.proxies.qsize < 3]):pass    
   self.collect()
  self.scraper.isAlive = False

 def collect(self):
  while all([self.isAlive, self.scraper.proxies.qsize]):
   proxy = self.scraper.proxies.get()
   if not self.recentProxies.inQueue(proxy):
    self.recentProxies.put(proxy)
    self.proxies.put(proxy)

 def kill(self):
  self.isAlive = False
 
 def watch(self, proxy, driver):
  print '\n[!] Proxy-IP: {}\n[-] Country: {}\n[+] Views: {}\n'.format(proxy['ip'], proxy['country'], self.visits+1)
  if not self.isAlive:return

  try:driver.get(self.url + '&t=5')
  except:
   self.renewDriver = True
   driver.quit()
 
  try:
    html = driver.page_source.encode('utf-8')
    if any(['ERR_PROXY_CONNECTION_FAILED' in html, 'ERR_TUNNEL_CONNECTION_FAILED' in html, 'ERR_EMPTY_RESPONSE' in html]):
     self.renewDriver = True
     driver.quit()
  except:
   self.renewDriver = True
   driver.quit()

  sleep(3)
  self.isActive = False 
  if self.renewDriver:driver.quit()
  else:self.visits += 1

 def driver(self, proxy):
  chrome_options = webdriver.ChromeOptions()
  chrome_options.add_argument('--headless')
  chrome_options.add_argument('--mute-audio')
  chrome_options.add_argument('--log-level=3')
  chrome_options.add_argument('--disable-gpu')
  chrome_options.add_argument('user-agent={}'.format(choice(USER_AGENTS)))
  chrome_options.add_argument('--proxy-server=http://{}:{}'.format(proxy['ip'], proxy['port']))
  return webdriver.Chrome(executable_path=DRIVER_PATH, chrome_options=chrome_options)

 def start(self):
  proxy = None
  driver = None
  driverUsage = 0
  renewDriver = True 
  Thread(target=self.proxiesManager).start()

  while all([self.visits < self.views, self.isAlive]):
   try:
    if driverUsage == 10:
     self.renewDriver = True

    if any([not self.isAlive, self.renewDriver]):
     proxy = None
     if driver:driver.quit()
     if self.proxies.qsize:
      driverUsage = 0
      self.renewDriver = False
      proxy = self.proxies.get()
      driver = self.driver(proxy)

    if all([self.proxies.qsize, proxy]):     
     self.isActive = True 
     if not proxy:
      proxy = self.proxies.get()

     Thread(target=self.watch, args=[proxy, driver]).start()
     
     # wait 
     while self.isActive:
      try:
       sleep(0.5)
       self.removeDebug()       
      except KeyboardInterrupt:
       self.isAlive = False 

     driverUsage += 1
     if any([not self.isAlive, self.renewDriver]):
      proxy = None 
      if driver:driver.quit()
      if self.proxies.qsize:
       driverUsage = 0
       self.renewDriver = False
       proxy = self.proxies.get()
       driver = self.driver(proxy)

   except KeyboardInterrupt:
    self.isAlive = False

  if driver:driver.quit()
  self.isAlive = False
  self.removeDebug()
  if self.visits == self.views:
   self.visits = 0

 def removeDebug(self):
  if path.exists(DEBUG_LOG):
   remove(DEBUG_LOG)