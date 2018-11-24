# Geral
from functools import partial
# Kivy
from kivy.clock import Clock
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
# Base
from plugins.db import DB
from plugins.ferramentas import Ferramentas
from gerenciador import Gerenciador

db = DB()
ge = Gerenciador()
fe = Ferramentas()

__all__ = ['db', 'ge', 'fe', 'Formulario', 'FormEntradaMascara', 'FormEntrada', 'FormConteudo', 'FormRotulo', 'FormAviso', 'FormBotao', 'FormSeletorOpcoesConteudo', 'FormSeletorOpcao', 'FormSeletor', 'FormSeletorPopupConteudo', 'MenuBotao', 'Menu', 'PesquisaBotao', 'PesquisaResultado', 'PesquisaResultadoConteudo', 'PesquisaResultadoTitulo', 'PesquisaResultadoTituloRotulo', 'PesquisaResultadoComum', 'PesquisaResultadoComumRotulo', 'PesquisaResultadoComumBotao']

# [1. Widgets dos Formulários]:

# Widget Principal
class Formulario(ScrollView):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		# Identificar se Formulário está sendo enviado 
		self.enviando = False
		# Exibir Aviso de Sucesso se o envio for bem sucedido
		self.aviso_sucesso = False
		# Armazena os dados do Formulário durante o envio
		self.dados = {}

	# Método responsável por enviar os dados dos Widgets do Formulário
	def enviar_dados(self, nome):
		# Se existirem Widgets Filhos no Formulário
		if (len(self.children) > 0 and self.enviando == False):

			self.enviando = True

			# Acessando Widgets Filhos do Formulário
			form_conteudo = self.children[0]
			form_conteudo_itens = form_conteudo.children

			# Resetando Dados
			self.dados = {}

			for i in range(len(form_conteudo_itens)):
				widget = form_conteudo_itens[i]
				# Se o Widget tiver o método "obter_valor()" e "nome", será adicionado à "self.dados"
				try:
					if (len(widget.nome) > 0):
						self.dados[widget.nome] = widget.obter_valor()
				except Exception as e:
					pass

			# Enviando o Formulário através do método "envio_formulário" de "Gerenciador
			ge.envio_formulario(nome, self.dados, self, self.aviso_sucesso)

			self.enviando = False

	# Reseta as informações dos campos do Formulário 
	def resetar(self, manter_aviso=False):
		# Se existirem Widgets Filhos no Formulário
		if (len(self.children) > 0):

			# Acessando Widgets Filhos do Formulário
			form_conteudo = self.children[0]
			form_conteudo_itens = form_conteudo.children
			
			for i in range(len(form_conteudo_itens)):
				widget = form_conteudo_itens[i]
				# Se o Widget tiver o método "resetar()" ele terá suas informações resetadas
				try:
					if (manter_aviso == True):
						# Se for um Widget "FormAviso"
						if (widget.__class__.__name__ != 'FormAviso'):
							widget.resetar()
					else:
						widget.resetar()
				except Exception as e:
					# Widget não possui o método "resetar()"
					pass
	
	# Exibe o AVISO do Formulário					
	def aviso(self, texto, cor='vermelho'):
		# Se existirem Widgets Filhos no Formulário
		if (len(self.children) > 0):

			# Acessando Widgets Filhos do Formulário
			form_conteudo = self.children[0]
			form_conteudo_itens = form_conteudo.children
			
			for i in range(len(form_conteudo_itens)):
				widget = form_conteudo_itens[i]
				try:
					# Se for um Widget "FormAviso"
					if (widget.__class__.__name__ == 'FormAviso'):
						# Executa o método "revelar"
						widget.revelar(texto, cor)
						break
				except Exception as e:
					# Widget não é de FormAviso
					pass

# TextInput com Máscara
class FormEntradaMascara(TextInput):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		# Formato da Máscara
		self.mascara = ''

	def resetar(self):
		self.text = ''

	def obter_valor(self):
		return self.text

	# Quando o texto for alterado
	def on_text(self, instancia, texto):
		# Aplicando método de máscara ao texto
		texto = fe.mascara(texto, self.mascara)
		
		# Modificando texto no TextInput para a versão mascarada
		self.text = texto

		# Mover cursor para o fim do texto
		Clock.schedule_once(partial(self.do_cursor_movement, 'cursor_end'))

# TextInput Normal
class FormEntrada(TextInput):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

	def resetar(self):
		self.text = ''

	def obter_valor(self):
		return self.text

class FormConteudo(BoxLayout):
	pass

class FormRotulo(Label):
	pass

class FormAviso(ButtonBehavior, BoxLayout):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		# Cores do Aviso
		self.cores = {
			'vermelho': (.85, .27, .27, 1), 
			'azul': (.1, .5, .85, 1), 
			'verde': (.10, .85, .32, 1)
		}

	def resetar(self):
		self.ocultar()

	def ocultar(self):
		self.texto = ''
		self.cor = 0, 0, 0, 0

	def revelar(self, texto, cor='vermelho'):
		if (len(texto) > 0):
			self.texto = texto
			self.cor = self.cores[cor]

class FormBotao(ButtonBehavior, Label):
	pass

class FormSeletorOpcoesConteudo(BoxLayout):
	pass

class FormSeletorOpcao(ButtonBehavior, BoxLayout):
	pass

class FormSeletor(ButtonBehavior, BoxLayout):
	# Id (key) da opção escolhida
	id_escolhido = None
	# Texto exibido pelo seletor
	texto = StringProperty('')
	opcoes = ObjectProperty({})
	# Id da opção default
	opcoes_base = None
	padrao = StringProperty('')
	
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

		Clock.schedule_once(self.backup)
		Clock.schedule_once(self.opcoes_via_db)
		Clock.schedule_once(self.opcao_padrao)

	# Gera um Backup das Informações atuais
	def backup(self, *args):
		self.base = {
			'id_escolhido':self.id_escolhido, 
			'texto':self.texto, 
			'opcoes':self.opcoes, 
			'padrao':self.padrao
		}

	def opcoes_via_db(self, *args):
		if (self.opcoes_base == None):
			self.opcoes_base = self.opcoes
		self.opcoes = self.opcoes_base
		try:
			if ('db' in self.opcoes):
				db.checar(self.opcoes['db'][0], self.opcoes['db'][1], self.opcoes['db'][2], self.opcoes['db'][3])
				resultado = db.resultado
				
				if (len(self.opcoes['extra']) > 0):
					self.opcoes = self.opcoes['extra']
				else:
					self.opcoes = {}

				for i in range(len(resultado)):
					self.opcoes[str(resultado[i]['id'])] = resultado[i]['valor']
		except Exception as e:
			print(e)


	def resetar(self):
		self.id_escolhido = self.base['id_escolhido']
		self.texto = self.base['texto']
		self.opcoes = self.base['opcoes']
		self.padrao = self.base['padrao']
		Clock.schedule_once(self.opcao_padrao)

	def obter_valor(self):
		return self.id_escolhido

	def opcao_padrao(self, *args):
		if (self.padrao in self.opcoes):
			self.id_escolhido = self.padrao
			self.texto = self.opcoes[self.padrao]

	def opcao_escolhida(self, identificador, texto):
		self.id_escolhido = identificador
		self.texto = texto
		self.popup.dismiss()

	def exibir_opcoes(self):
		self.opcoes_via_db()
		self.conteudo = FormSeletorPopupConteudo()
		self.fsoc_scroll = ScrollView(pos_hint = {'center_x': .5, 'center_y': .5}, bar_margin=2, do_scroll_x=False, do_scroll_y=True)

		self.fsoc = FormSeletorOpcoesConteudo()
		self.fsoc.form_seletor = self
		self.fso = []
		for i in self.opcoes.items():
			ilista = list(i)
			ide = ilista[0]
			valor = ilista[1]
			self.fso.append(FormSeletorOpcao())
			self.fso[-1].identificador = ide
			self.fso[-1].texto = valor

			if (self.id_escolhido == self.fso[-1].identificador):
				self.fso[-1].ativo = True
			else:
				self.fso[-1].ativo = False
			self.fsoc.add_widget(self.fso[-1])

		self.fsoc_scroll.add_widget(self.fsoc)
		self.conteudo.add_widget(self.fsoc_scroll)

		self.popup = Popup(title='', separator_height=0, size_hint=(.85, .85), auto_dismiss=True, content=self.conteudo, border=(0, 0, 0, 0), background='imagens/sistema/pixel_transparente.png', background_color=[0, 0, 0, .35])

		self.popup.open()

class FormSeletorPopupConteudo(BoxLayout):
	pass


# Widgets do Menu
class MenuBotao(ButtonBehavior, Label):
	pass

class Menu(BoxLayout):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		Clock.schedule_once(self.construir_menu)

	def construir_menu(self, *args):
		op = ge.opcoes_menu()
		for i in range(len(op)):
			cor = (.85, .85, .85, 1) if (op[i]['tela'] != self.tela.name) else (.1, .5, .85, 1)
			cor_borda = (.7, .7, .7, 1) if (op[i]['tela'] != self.tela.name) else (.08, .43, .69, 1)
			icone = op[i]['icone'] if (op[i]['tela'] != self.tela.name) else op[i]['icone_i']
			mb = MenuBotao()
			mb.icone = icone
			mb.cor = cor
			mb.cor_borda = cor_borda
			mb.bind(on_press=partial(self.tela.mudar_tela, op[i]['tela']))
			self.ids.opcoes.add_widget(mb)


# Widgets de exibição dos resultados (Tabela)
class PesquisaBotao(ButtonBehavior, Label):
	pass

class PesquisaResultado(ScrollView):
	pass

class PesquisaResultadoConteudo(BoxLayout):
	pass

class PesquisaResultadoTitulo(BoxLayout):
	pass

class PesquisaResultadoTituloRotulo(Label):
	pass

class PesquisaResultadoComum(BoxLayout):
	pass

class PesquisaResultadoComumRotulo(Label):
	pass

class PesquisaResultadoComumBotao(ButtonBehavior, Label):
	pass