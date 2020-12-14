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
		self.menus = Menu(self.master)
		self.master.bind_all('<Control_L><a>',self.add_contact_event)
	def add_contact_event(self,event):
		self.menus.add_contact()
	def __update(self):
		'''update gui content'''
		#self.master.update_idletasks()
		#self.master.update()
		pass

class Menu:
	def __init__(self,master=None):
		assert master!=None
		self.master = master
		self.menu = tkinter.Menu(self.master)
		
		# contacts
		self.contacts = tkinter.Menu(self.menu,tearoff=0)
		self.contacts.add_command(label='Add',command=self.add_contact)
		self.contacts.add_command(label='Del',command=self.del_contact)
		self.menu.add_cascade(label='Contacts',menu=self.contacts)
		#
		self.master.config(menu=self.menu)
	def add_contact(self):
		popup = Popup(self.master,'add contact')
		name = AskQuest(popup.frame,'name:')
		name.pack(expand=1,fill='x')
		number = AskQuest(popup.frame,'number:')
		number.pack(expand=1,fill='x')
		email = AskQuest(popup.frame,'email:')
		email.pack(expand=1,fill='x')
		bts = tkinter.Frame(popup.frame)
		bts.pack(expand=1,fill='x')
		save = tkinter.Button(bts,text='save')
		save['command']=lambda :self.save_contact(popup)
		save.pack(side='left',fill='x',expand=1)
		
		cancel = tkinter.Button(bts,text='cancel')
		cancel['command']=popup.close
		cancel.pack(side='left',fill='x',expand=1)


		name.res.focus_force()
		popup.mainloop()
	def save_contact(self,popup):
		popup.close()
	def del_contact(self):
		pass

class Popup:
	def __init__(self,master,title:str):
		self.master  = master
		self.top = tkinter.Toplevel()
		self.top.geometry(self.master.geometry())
		self.top.grab_set()
		self.top.title(title)
		self.top.protocol("WM_DELETE_WINDOW",self.close)
		self.frame = tkinter.Frame(self.top)
		self.frame.pack(expand=1,fill='both')
	def close(self):
		self.top.grab_release()
		self.top.destroy()
	def mainloop(self):
		self.master.wait_window(self.top)

class AskQuest(tkinter.Frame):
	def __init__(self,master,req:str,*w,**kw):
		super().__init__(master)
		self.req = tkinter.Label(self,text=req)
		self.req.pack(side='left',fill='x')
		self.res = tkinter.Entry(self)
		self.res.pack(side='left',expand=1,fill='x')

