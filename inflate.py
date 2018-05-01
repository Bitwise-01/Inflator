# Date: 04/13/2018
# Author: Pure-L0G1C
# Description: UI 

import sys
from Tkinter import *
from time import sleep
from threading import Thread 
from lib.browser import Viewer

class Window(Frame):
 def __init__(self, gui):
  Frame.__init__(self, gui)

  self.gui = gui
  self.lastUrl = None 
  self.isAlive = True
  self.lastVisit = None 
  gui.protocol("WM_DELETE_WINDOW", self.close)

  self.viewBot = None
  self.isStarted = False   
  Label(text='Version: 0.1\nAuthor: Pure-L0G1C\n', font=('Courier', 8, 'italic')).pack()

  Label(text='URL', fg='blue', font=('Courier', 16)).pack()
  self.link = Entry(font=('Helvetica', 16), justify='center')
  self.link['width'] = 42
  self.link.pack()
         
  Label(text='\nViews', fg='blue', font=('Courier', 16)).pack()
  self.maxVisits = Entry(justify='center', font=('Helvetica', 16))
  self.maxVisits['width'] = 10
  self.maxVisits.pack()
  Label().pack()
               
  self.startBtn = Button(bg='blue',
                         fg='white',
                         text='Start',
                         font=('Courier', 12),
                         command=self.onEnter)
  self.startBtn.pack()  

  self.output = Text(self, width=100, height=9, bg='lightgray', fg='black')
  self.output.bind('<Key>', lambda _: 'break')
  self.output.pack()

  sys.stdout = self
  self.pack()

 def switchMonitor(self):
  while self.viewBot.isAlive:sleep(1)
  if self.isStarted:self.switchRole() 

 def viewBotKill(self):
  if self.viewBot:
   self.viewBot.kill()

 def switchRole(self):
  if self.isStarted:
   self.viewBotKill()
   self.isStarted = False
   print '\n[!] Stopping ...\n'

   sleep(1.5)
   self.startBtn.config(text='Start', bg='blue')

  else:
   self.isAlive = True
   self.isStarted = True
   print '[+] Starting ...'
   self.startBtn.config(text='Stop', bg='red')
  
 def close(self):
  self.isAlive = False
  self.viewBotKill()
  self.gui.destroy()     
  self.gui.quit()
  sys.exit()

 def watch(self, link, amt, lastVisits=0):
  self.viewBotKill()
  self.viewBot = Viewer(link, amt, lastVisits)
  Thread(target=self.viewBot.start).start()
  Thread(target=self.switchMonitor).start()

 def onEnter(self):
  if any([not self.link.get(), not self.maxVisits.get().isdigit()]):return 
  if int(self.maxVisits.get()) < 1:return

  self.switchRole()
  if self.isStarted:
   if all([self.lastVisit == int(self.maxVisits.get()), self.lastUrl == self.link.get()]):
    crntVisits = self.viewBot.visits 
    self.watch(self.link.get(), int(self.maxVisits.get()), crntVisits)
   else:
    self.watch(self.link.get(), int(self.maxVisits.get()))
    self.lastVisit = int(self.maxVisits.get())
    self.lastUrl = self.link.get()

 def write(self, txt):
  try:
   self.output.insert(END, str(txt))
   self.update_idletasks()
   self.output.see('end')
  except:self.close()

if __name__ == '__main__':
 app = Window(Tk())
 app.master.geometry('730x330+340+180')
 app.master.title('Inflator')
 app.mainloop()