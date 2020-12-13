import sqlite3

class DataBase:
	'''sql wrapper for python'''
	def __init__(self,filename:str,debug:bool=False,*w,**kw):
		self.__debug=debug
		self.connected = False
		self.connection = sqlite3.connect(filename)
		self.cursor = self.connection.cursor()
		self.connected = True
	def close(self):
		if self.connected:
			self.connected=False
			self.cursor.close()
			self.connection.close()
	def __exit__(self):
		self.close()
	def __del__(self):
		self.close()
	# sql connection functions
	def commit(self):
		'''save database changes to disk'''
		if self.connected:
			self.connection.commit()
		return self.connected
	# sql cursor     functions
	def execute(self,sql:str):
		'''execute sql command'''
		if self.connected:
			try:
				self.cursor.execute(sql)
				return True
			except Exception as e:
				if self.__debug:
					raise e
				else:
					print(e)
		return False
	def fetch(self,row:int=1):
		'''fetch n rows from result'''
		if self.connected:
			return self.cursor.fetchmany(row)
	def fetchall(self):
		'''return all rows from result'''
		if self.connected:
			return self.cursor.fetchall()
	# sql common commands
	def drop(self,name:str):
		sql = f'DROP TABLE {name};'
		return self.execute(sql)
	def create_table(self,name:str,*w,**kw):
		'''create new table'''
		if self.connected:
			sql = f'CREATE TABLE {name}('+','.join(w)+');'
			self.execute(sql)
			return Table(name,self)

class Table:
	def __init__(self,name:str,db=None):
		self.name = name
		assert isinstance(db,DataBase)
		self.db = db
	def __kw_check(self,*w,**kw):
		'''correct strings for insert into database'''
		#print('kw:',kw)
		for k,v in kw.items():
			if type(v)==str:
				kw[k]="'"+v+"'"
			else:
				v= str(v)
				kw[k]=v
		return kw
	def insert(self,*w,**kw):
		'''insert data to table'''
		kw = self.__kw_check(*w,**kw)
		keys = ','.join(kw.keys())
		values = ','.join(kw.values())
		sql = f'INSERT INTO {self.name}({keys}) VALUES({values});'
		return self.db.execute(sql)
	def drop(self):
		'''remove table'''
		sql = f'DROP TABLE {self.name};'
		self.db.execute(sql)
		del self
	def delete(self,where='',*w,**kw):
		'''delete table content or table self'''
		if where!='':
			where = ' WHERE '+where
		sql = f'DELETE FROM {self.name}'+where+';'
		return self.db.execute(sql)
	def select(self,*w,where:str='',**kw):
		'''select items in table'''
		if where!='':
			where = ' WHERE '+where
		sql = 'SELECT '+','.join(w)+' FROM '+self.name+where+';'
		return self.db.execute(sql)
	def update(self,where='',*w,**kw):
		kw = self.__kw_check(kw)
		if where!='':
			where = ' WHERE '+where
		sql = f'UPDATE {self.name} SET '+','.join([f'{k}={v}' for k,v in kw.items()])+where+';'
		return self.db.execute(sql)