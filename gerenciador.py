from plugins.db import DB
from plugins.ferramentas import Ferramentas
from gformularios import GFormularios

db = DB()
fe = Ferramentas()

class Gerenciador():

	def __init__(self):
		self.gf = GFormularios()
	
	def envio_formulario(self, form_nome, post, formulario=None, aviso_sucesso=False):
		try:
			exec('self.f = self.gf.{}'.format(form_nome))
			self.f = self.f(post)
			if (formulario != None):
				if (self.f == False):
					formulario.aviso(self.gf.converter_log())
				else:
					if (aviso_sucesso == True):
						formulario.aviso(self.gf.converter_log(), 'verde')
						formulario.resetar(manter_aviso=True)
					else:
						formulario.resetar()
			return self.f
		except Exception as e:
			if (formulario != None):
				formulario.aviso('Falha ao enviar dados, tente novamente')
			return False

	def opcoes_menu(self):
		return [
			{'icone':'pesquisa.png', 'icone_i':'pesquisa_i.png', 'tela':'tela_pesquisa'},
			{'icone':'carro.png', 'icone_i':'carro_i.png', 'tela':'tela_cadastro_carro'},
			{'icone':'usuario.png', 'icone_i':'usuario_i.png', 'tela':'tela_cadastro_usuario'},
			{'icone':'marca.png', 'icone_i':'marca_i.png', 'tela':'tela_cadastro_marca'}
		]