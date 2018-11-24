import sqlite3

class DB():
	conectado = False
	resultado = None
	contador = None
	id_inserido = None
	linhas_atualizadas = None
	linhas_deletadas = None

	def __init__(self, banco='db/dados.db'):
		self.conectar(banco)


	def conectar(self, banco):
		def dict_factory(cursor, row):
			d = {}
			for idx, col in enumerate(cursor.description):
				d[col[0]] = row[idx]
			return d

		try:
			self.con = sqlite3.connect(banco)
			self.con.row_factory = dict_factory
			self.cur = self.con.cursor()
			self.conectado = True
		except Exception as e:
			print(e)
			self.conectado = False

	def gerar_espaco_reservado(self, quantidade):
		lista = []
		for i in range(quantidade):
			lista.append('?')
		return lista

	def checar_tabela(self, tabela):
		sql = "SELECT COUNT(*) as count FROM sqlite_master WHERE type='table' AND name=?"
		self.cur.execute(sql, (tabela,))
		resultado = self.cur.fetchall()[0]
		
		if (resultado['count'] < 1):
			return False
		else:
			return True

	def checar_id(self, tabela, id):
		if (self.checar_tabela(tabela) != True):
			return False
		else:
			sql = "SELECT COUNT(*) as count FROM {} WHERE id=?".format(tabela)
			self.cur.execute(sql, (id,))
			resultado = self.cur.fetchall()[0]
			
			if (resultado['count'] < 1):
				return False
			else:
				return True

	def checar(self, tabela, where='', select='*', valores=[]):
		if (self.checar_tabela(tabela) != True):
			return False
		else:
			sql = "SELECT {} FROM {} {}".format(select, tabela, where)
			self.cur.execute(sql, valores)
			resultado = self.cur.fetchall()
			
			self.contador = len(resultado)
			if (len(resultado) < 1):
				self.resultado = None
				return False
			else:
				self.resultado = resultado
				return True

	def checars(self, sql, valores=[]):
		self.cur.execute(sql, valores)
		resultado = self.cur.fetchall()
		
		self.contador = len(resultado)
		if (len(resultado) < 1):
			self.resultado = None
			return False
		else:
			self.resultado = resultado
			return True

	def inserir(self, tabela, post):
		if (self.checar_tabela(tabela) != True):
			return False
		else:
			chaves = ', '.join(list(post.keys()))
			espaco_reservado = ', '.join(self.gerar_espaco_reservado(len(list(post.keys()))))
			valores = list(post.values())

			try:
				sql = "INSERT INTO {}({}) VALUES({})".format(tabela, chaves, espaco_reservado)
				inserir = self.cur.execute(sql, valores)
				self.con.commit()
				self.id_inserido = inserir.lastrowid
				return True
			except Exception as e:
				print(e)
				return False

	def atualizar(self, tabela, post, where='', valores=[]):
		if (self.checar_tabela(tabela) != True):
			return False
		else:
			chaves = list(post.keys())
			chaves_join = '=?, '.join(chaves) + '=?'
			valoresp = list(post.values())
			valores = valoresp + valores

			try:
				sql = "UPDATE {} SET {} {}".format(tabela, chaves_join, where)
				print(sql)
				print(valores)
				atualizar = self.cur.execute(sql, valores)
				self.con.commit()
				self.linhas_atualizadas = atualizar.rowcount
				if (self.linhas_atualizadas < 1):
					return False
				else:
					return True
			except Exception as e:
				print(e)
				return False

	def deletar(self, tabela, where='', valores=[]):
		if (self.checar_tabela(tabela) != True):
			return False
		else:
			try:
				sql = "DELETE FROM {} {}".format(tabela, where)
				deletar = self.cur.execute(sql, valores)
				self.con.commit()
				self.linhas_deletadas = deletar.rowcount

				if (self.linhas_deletadas < 1):
					return False
				else:
					return True
			except Exception as e:
				print(e)
				return False
