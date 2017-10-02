# encoding=utf8 
import os,time
import tkinter
from PIL import Image,ImageTk
from pylab import *
import threading
import random
class TomatoClock:
	def __init__(self):
		self.createwidgets()
		self.renderstyle()
		self.daemon = threading.Thread(target=self.updatetime)
		self.daemon.setDaemon(True)
		self.daemon.start()
		self.run()

	def updatetime(self):
		#t = time.time()
		while True:
			tstr = time.strftime('%H:%M:%S',time.localtime())
			self.timer['text'] = tstr
			time.sleep(1)
	def run(self):
		self.frame.mainloop()
	def start(self):
		hour,minute,second = self.hour.get(),self.minute.get(),self.second.get()
		error = False
		if not hour.isdigit():
			self.hour.set('0')
			error = True
		if not minute.isdigit():
			self.minute.set('0')
			error = True
		if not second.isdigit():
			self.second.set('0')
			error = True
		if error:
			return False
		t = int(hour)*3600 + int(minute)*60 + int(second)
		if t <= 0:
			return False
		self.active = True
		self.counterth = threading.Thread(target=self.countdown,args=(t,))
		self.counterth.setDaemon(True)
		self.counterth.start()
		print('start....{}:{}:{}'.format(hour,minute,second))
	def countdown(self,t):
		while t>=0 and self.active:
			counterstr = '%d:%d:%d'%(int(t/3600),int((t%3600)/60),t%60)
			self.counter['text'] = counterstr
			t -= 1
			time.sleep(1)

		while self.active:
			self.shake()
			#time.sleep(0.1)
	def shake(self):
		screen_width,screen_height = self.frame.winfo_screenwidth(),self.frame.winfo_screenheight()
		self.frame.geometry('%dx%d+%d+%d'%(540,440,(screen_width-540)/2+random.randint(1,3),(screen_height-440)/2+random.randint(1,3)))
		self.frame.update()
		self.frame.deiconify()
	def reset(self):
		self.hour.set('0')
		self.minute.set('0')
		self.second.set('0')
		self.counter['text'] = ''
		self.active = False
		print('reset done!')
	def renderstyle(self):
		self.frame.geometry('540x440')
		self.frame.resizable(False,False)
		self.frame.iconbitmap('clock.ico')
		self.frame.title("Tomato Clock")
		background = Image.open('background.png')
		self.im = ImageTk.PhotoImage(background)
		self.canvas.create_image(0,0,anchor=tkinter.NW,image=self.im)
		self.canvas.place(x=0,y=0)
		self.timer.place(x=100,y=160,width=320,height=50)
		self.counter.place(x=100,y=220,width=320,height=50)
		self.timelabel.place(x=100,y=315,width=80,height=35)
		self.hinput.place(x=190,y=315,width=70,height=35)
		self.minput.place(x=270,y=315,width=70,height=35)
		self.sinput.place(x=350,y=315,width=70,height=35)
		self.setlabel.place(x=100,y=365,width=80,height=35)
		self.startbtn.place(x=190,y=365,width=70,height=35)
		self.resetbtn.place(x=270,y=365,width=70,height=35)
	def createwidgets(self):
		self.frame = tkinter.Tk()
		self.canvas = tkinter.Canvas(self.frame,width=540,height=440,bg='white')
		self.timer = tkinter.Label(self.frame,text="15:44:04",font='Helvetica -35 bold')
		self.counter = tkinter.Label(self.frame,text="",font='Helvetica -35 bold',fg='red')
		self.timelabel = tkinter.Label(self.frame,text='时间')
		self.setlabel = tkinter.Label(self.frame,text='设置')
		self.hour,self.minute,self.second = tkinter.StringVar(),tkinter.StringVar(),tkinter.StringVar()
		self.minute.set('0')
		self.hour.set('0')
		self.second.set('0')
		self.hinput = tkinter.Entry(self.frame,bd=2,relief = 'ridge',textvariable=self.hour)
		self.minput = tkinter.Entry(self.frame,bd=2,relief = 'ridge',textvariable=self.minute)
		self.sinput = tkinter.Entry(self.frame,bd=2,relief = 'ridge',textvariable=self.second) 
		self.startbtn = tkinter.Button(self.frame,text='开始',command=self.start)
		self.resetbtn = tkinter.Button(self.frame,text='重置',command=self.reset)

if __name__ == '__main__':
	tc = TomatoClock()
