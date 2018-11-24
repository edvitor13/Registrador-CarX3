from plugins.db import DB
from plugins.ferramentas import Ferramentas

db = DB()
fe = Ferramentas()

__all__ = ['GFormularios']

# Gerenciador Formulários
class GFormularios():
	
	def __init__(self):
		self.log = []

	def converter_log(self):
		if (len(self.log) > 0):
			return '\n'.join(self.log)
		else:
			return ''

	def form_cadastro_usuario(self, post):
		self.log = []

		if (not fe.verificar_post(['nome', 'celular', 'carro'], post)):
			self.log.append('Informações inválidas, tente novamente')
			return False
		else:
			p = {}
			p['nome'] = fe.filtrar(post['nome'], 'nome').strip()
			p['celular'] = fe.mascara(post['celular'], '+## (##) # ####-####').strip()
			if (post['carro'] == None):
				post['carro'] = '0'
			p['carro'] = fe.filtrar(post['carro'], 'numero')
			
			verificacao = True
			if (len(p['nome']) < 3):
				self.log.append('Nome muito curto')
				verificacao = False

			if (len(fe.filtrar(p['celular'], 'numero')) != 13):
				self.log.append('Preencha o número de celular corretamente')
				verificacao = False

			if (verificacao == True and db.checar('pessoas', 'WHERE celular=?', 'id', [p['celular']]) == True):
				self.log.append('Já existe alguém registrado com esse celular')
				verificacao = False

			if (p['carro'] != '0'):
				if (db.checar_id('carros', p['carro']) == False):
					self.log.append('Selecione um carro válido')
					verificacao = False

			if (verificacao == False):
				return False
			else:
				if (db.inserir('pessoas', post) == False):
					self.log.append('Falha ao registrar usuário, tente novamente')
					return False
				else:
					self.log.append('Sucesso ao registrar usuário')
					return True

	def form_cadastro_carro(self, post):
		self.log = []

		if (not fe.verificar_post(['modelo', 'marca'], post)):
			self.log.append('Informações inválidas, tente novamente')
			return False
		else:
			p = {}
			p['modelo'] = post['modelo'].strip()
			if (post['marca'] == None):
				post['marca'] = '0'
			p['marca'] = fe.filtrar(post['marca'], 'numero')
			
			verificacao = True

			if (len(p['modelo']) < 1):
				self.log.append('Escreva um modelo válido')
				verificacao = False

			if (db.checar('carros', 'WHERE modelo LIKE ?', 'id', [p['modelo']]) == True):
				self.log.append('O modelo "{}" já está registrado'.format(p['modelo']))
				verificacao = False

			if (db.checar_id('marcas', p['marca']) == False):
				self.log.append('Selecione uma marca válida')
				verificacao = False

			if (verificacao == False):
				return False
			else:
				if (db.inserir('carros', post) == False):
					self.log.append('Falha ao registrar carro, tente novamente')
					return False
				else:
					self.log.append('Sucesso ao registrar carro')
					return True

	def form_cadastro_marca(self, post):
		self.log = []

		if (not fe.verificar_post(['marca'], post)):
			self.log.append('Informações inválidas, tente novamente')
			return False
		else:
			p = {}
			p['marca'] = post['marca'].strip()
			
			verificacao = True

			if (len(p['marca']) < 1):
				self.log.append('Escreva uma marca válida')
				verificacao = False

			if (verificacao == True and db.checar('marcas', 'WHERE marca LIKE ?', 'id', [p['marca']]) == True):
				self.log.append('A marca "{}" já está registrada'.format(p['marca']))
				verificacao = False

			if (verificacao == False):
				return False
			else:
				if (db.inserir('marcas', post) == False):
					self.log.append('Falha ao registrar marca, tente novamente')
					return False
				else:
					self.log.append('Sucesso ao registrar marca')
					return True
