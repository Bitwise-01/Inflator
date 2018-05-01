# Date: 04/13/2018
# Author: Pure-L0G1C
# Description: Queue

class Queue(object):
 def __init__(self, size=30):
  self.queue = []
  self.size = size

 def put(self, item):
  if not item in self.queue:
   if self.qsize == self.size:
    self.queue.pop(0)
   self.queue.append(item)

 def get(self):
  if self.qsize:
   return self.queue.pop(0)

 def inQueue(self, item):
  return item in self.queue 

 @property 
 def qsize(self):
  return len(self.queue)