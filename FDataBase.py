import os


class FDataBase:
	def __init__(self, db):
		self.__db = db
		self.__cur = db.cursor()

	def getMenu(self):
		sql = '''SELECT * FROM mainmenu'''
		try:
			self.__cur.execute(sql)
			res = self.__cur.fetchall()
			if res: return res
		except:
			print('Error read from BD(menu)')
		return []
	#SQL запрос на регистрацию пользователя
	def setLoginPassword(self, user, password, email):
		auth = 'True'
		sql = "INSERT INTO user (user_name,pass,email,auth) VALUES (?,?,?,?);"
		try:
			self.__cur.execute(sql,(user,password,email,auth))
			self.__db.commit()
			print('read from BD OK')							
		except self.__db.Error as error:
			print('Error read from BD(setlogin) :',error)
			
	#получение логина и пароля.
	def getLoginPassword(self, user,passw):
		try:
			self.__cur.execute('SELECT pass FROM user WHERE user_name=:user', {'user':user})
			rows = self.__cur.fetchone()
			if rows:
				for row in rows:
					if passw == row:
						return True
			print('read from BD OK')
		except self.__db.Error as error:
			print('Error read form BD(getlogin):', error)
		return False


	def getEmail(self, username):
		try:
			self.__cur.execute('SELECT email FROM user WHERE user_name=:user', {'user':username})
			row = self.__cur.fetchone()
			if row==True and list(row)[0] != '':
				print('read from BD OK(email)')
				return row
			else:
				return list(row)[0]
		except self.__db.Error as error:
			print('Error read form BD(getlogin):', error)


	#Загрузка файлов в БД

	def insert_blob(self, username, filename):
		sql = 'INSERT INTO document (user_name, file, file_name) VALUES (?, ?, ?)'
		with open(os.path.abspath(filename), 'rb') as file:
			blob_data = file.read()
		try:
			file = blob_data
			data_tuple = (username, file, filename)

			self.__cur.execute(sql, data_tuple)
			self.__db.commit()
			print('file insert success')
	
		except self.__db.Error as error:
			print('Error read from BD(insert):',error)

# имя документа
	def downfile(self):
		sql = 'SELECT (*) FROM document WHERE file_name;'
		try:
			self.__cur.execute(sql)
			print("Подключен к SQLite")
			rows = self.__cur.fetchall()
			print('read from BD OK')
			return rows
		except self.__db.Error as error:
			print('Error read form BD(getlogin):', error)
	





	#Выгрузка файлов из БД

	def read_blob_data(self, file_upload_name):
		sql = "SELECT * FROM document WHERE user_name = ?"
		sql_id = "SELECT * FROM document WHERE id = ?"
		try:
			self.__cur.execute(sql,(self.__cur.execute(sql_id)))
			print("Подключен к SQLite")
			record = self.__cur.fetchall()

			for row in record:
				print("Id = ", row[0], "Name = ", row[1])
				name  = row[1]
				file = row[2]

				print("Сохранение файла на диске \n")
				
				file_path = os.path.join(file_upload_name)
				
				with open(file_path, 'wb') as file:
					file.write(file)
				print("Данныe из blob сохранены в: ", file_path, "\n")

		except self.__db.Error as error:
			print('Error read from BD(read) :',error)
		
	def countUsers(self):
		
		sql_id = "SELECT user_name, pass FROM user"
		try:
			
			self.__cur.execute(sql_id)
			rows = self.__cur.fetchall()
			print('read from BD OK')
			return rows
		except self.__db.Error as error:
			print('Error read form BD(getlogin):', error)
	

	def delete(self):
		sql = 'DELETE FROM user;'
		try:
			self.__cur.execute(sql)
			self.__db.commit()
			print('read from BD OK')
		except self.__db.Error as error:
			print('Error read form BD(getlogin):', error)

	def countfiles(self):
		sql = 'SELECT id, user_name FROM document;'
		try:
			self.__cur.execute(sql)
			rows = self.__cur.fetchall()
			print('read from BD OK')
			return rows
		except self.__db.Error as error:
			print('Error read form BD(getlogin):', error)