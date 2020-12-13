import tkinter

class Window:
	def __init__(self,title:str,width:int=640,height:int=480):
		self.master = tkinter.Tk()
		self.master.protocol('WM_DELETE_WINDOW',self.close)
		self.master.title(title)
		self.master.geometry(f'{width}x{height}+0+0')
		self.__start()
		self.master.mainloop()
	def close(self):
		self.master.destroy()
	def __start(self):
		'''start build gui'''
		pass
	def __update(self):
		'''update gui content'''
		#self.master.update_idletasks()
		#self.master.update()
		pass
