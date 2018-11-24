'''
PY 3.6.2 - KV 1.10.1
------------------------------------------
Registrador de Carros - CarX3 (Incompleto)
------------------------------------------
Author:       Vitor Gabriel
Version:      0.0
Date:         2018/11/23
Email:        edvitor13@hotmail.com
Description:  "Um software criado com o objetivo de testar SQLite e Kivy. Permite realizar o registro de usuários, carros e marcas de carros. Gerenciamento dos dados registrados em desenvolvimento."
'''

# Bibliotecas
# Kivy
from kivy.app import App
from kivy.lang.builder import Builder
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition, SlideTransition
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager
# Ferramentas
from fkivy import *


# [1. Configurações Iniciais]:

# Mudando cor de fundo do programa para cinza claro
Window.clearcolor = [.96, .96, .96, 1]
# Configurando teclado do Android para não sobrepor os Inputs
Window.softinput_mode = 'below_target'

# Carregando Código Kvlang via arquivo 
Builder.load_file('kvcode.kv')


# [2. Classes]:

# Classe Geral para ser herdada pelas Telas
class Geral():
	# Método responsável por mudança de tela
	def mudar_tela(self, nome_tela, tipo_transicao='No', direcao='left'):
		if (tipo_transicao == 'Slide'):
			self.manager.transition = eval(tipo_transicao + 'Transition()')
		else:
			self.manager.transition = NoTransition()
		self.manager.transition.direction = direcao
		self.manager.current = nome_tela


# [Classes Kivy]:

# Gerenciador das telas
class GerenciadorDeTelas(ScreenManager):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		# Executar o método "accdr" quando alguma tecla for pressionada
		Window.bind(on_keyboard=self.android_cancelar_clique_de_retorno)

	# Cancela a ação padrão da opção de "voltar" no Android e muda para a "tela_pesquisa" 
	def android_cancelar_clique_de_retorno(self, window, key, *args):
		if (key == 27):
			# Se a tela atual não for a "tela_pesquisa"
			if (self.current != 'tela_pesquisa'):
				# Transita para a "tela_pesquisa"
				self.current = 'tela_pesquisa'
				return True

# Tela responsável por exibir o formulário de cadastro de usuários
class TelaCadastroUsuario(Screen, Geral):
	pass

# Tela responsável por exibir o formulário de cadastro de carros
class TelaCadastroCarro(Screen, Geral):
	pass

# Tela responsável por exibir o formulário de cadastro de marcas
class TelaCadastroMarca(Screen, Geral):
	pass

# Tela responsável por exibir os botões que mudam para as Telas de Pesquisa de: Carro, Usuario e Marca
class TelaPesquisa(Screen, Geral):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

	# Carrega as informações da tela escolhida antes de mudar para ela
	def mudar_tela_carregando(self, nome_tela):
		# Acessando widget da tela escolhida
		tela = self.manager.get_screen(nome_tela)

		# Executando o método "carregar_resultados" da "tela" através do Clock
		Clock.schedule_once(tela.carregar_resultados)

		# Mudando para a "tela"
		self.mudar_tela(nome_tela, 'Slide', 'left')

# Tela responsável por exibir os Carros registrados no banco de dados
class TelaPesquisaCarro(Screen, Geral):
	
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		# Responsável por armazenar as instâncias do conteúdo dinâmico
		self.inst = []
		

	# Método responsável por remover os widgets do conteúdo da tela
	def remover_widgets(self):
		# Acessando Widget de Conteúdo
		conteudo = self.ids.conteudo

		# Acessando variável responsável por 
		for i in range(len(self.inst)):
			conteudo.remove_widget(self.inst[i])

	# Método responsável por carregar os dados do banco que serão exibidos
	def carregar_resultados(self, *args):
		# Acessando Widget de Conteúdo
		conteudo = self.ids.conteudo
		# Obtendo texto do Input que irá filtrar a seleção dos dados
		filtro = self.ids.filtro.text
		# Filtro adaptado para o "LIKE" da seleção
		fv = '%{}%'.format(filtro)

		# Removendo Widgets do Conteúdo e resetando "self.inst"
		self.remover_widgets()
		self.inst = []
		
		# Se a seleção NÃO for bem sucedida, exibe um AVISO
		if (not db.checars("SELECT c.id, c.modelo, m.marca FROM carros as c INNER JOIN marcas as m ON c.marca = m.id WHERE c.modelo LIKE ? OR c.marca IN (SELECT id FROM marcas WHERE marca LIKE ?)", valores=[fv, fv])):

			# Cria e adiciona um BoxLayot "FormAviso" ao "self.inst"
			self.inst.append(FormAviso())
			# Acessa e altera o "texto" de "FormAviso"
			self.inst[-1].texto = 'Nenhum resultado encontrado'
			# Adiciona o "FormAviso" ao Conteúdo
			conteudo.add_widget(self.inst[-1])

			# Adiciona um Widget em "self.inst" responsável por deixar um espaço proporcinal em branco abaixo do AVISO
			self.inst.append(Widget())
			# O adiciona ao Conteúdo
			conteudo.add_widget(self.inst[-1])

		# Se a seleção for bem sucedida, exibe os dados encontrados
		else:
			# Resultados da busca
			res = db.resultado

			# Widgets responsáveis por exibir a Tabela de com os resultados
			pr = PesquisaResultado()
			prc = PesquisaResultadoConteudo()
			# Titulo Tabela
			prt = PesquisaResultadoTitulo()
			prt.add_widget(PesquisaResultadoTituloRotulo(width='60dp', text='Nº'))
			prt.add_widget(PesquisaResultadoTituloRotulo(text='Modelo'))
			prt.add_widget(PesquisaResultadoTituloRotulo(text='Marca'))
			prt.add_widget(PesquisaResultadoTituloRotulo(width='100dp', text='Editar'))
			prt.add_widget(PesquisaResultadoTituloRotulo(width='100dp', text='Excluir'))
			# Adicionando Widgets
			prc.add_widget(prt)

			# Dados
			for i in range(len(res)):
				# Definindo cor de fundo da Linha da Tabela com base no ímpar ou par
				cor = (.78, .89, .99, 1) if (i % 2 == 0) else (.61, .80, .94, 1)
				# Dados que serão exibidos
				numero = '{}.'.format(i + 1)
				modelo = res[i]['modelo']
				marca = res[i]['marca']
				# Dados que serão utilizados
				ide = res[i]['id']

				# Botões de Edição (1) e Exclusão (2)
				# Criando Box dos botões
				boxbt1 = BoxLayout(size_hint=(None, 1), padding='10dp', width='100dp')
				boxbt2 = BoxLayout(size_hint=(None, 1), padding='10dp', width='100dp')
				# 1 Botão de Edição
				pcb = PesquisaResultadoComumBotao()
				pcb.icone = 'bt_edicao.png'
				boxbt1.add_widget(pcb)
				# 2 Botão de Exclusão
				pcb = PesquisaResultadoComumBotao()
				pcb.icone = 'bt_excluir.png'
				boxbt2.add_widget(pcb)

				# Linha
				prco = PesquisaResultadoComum()
				prco.cor = cor
				# Colunas
				prco.add_widget(PesquisaResultadoComumRotulo(width='60dp', text=numero))
				prco.add_widget(PesquisaResultadoComumRotulo(text=modelo))
				prco.add_widget(PesquisaResultadoComumRotulo(text=marca))
				prco.add_widget(boxbt1)
				prco.add_widget(boxbt2)

				# Adicionando Linha ao Conteúdo da Tabela
				prc.add_widget(prco)

			# Adicionando Tabela ao Conteúdo
			pr.add_widget(prc)
			self.inst.append(pr)
			conteudo.add_widget(self.inst[-1])

class TelaPesquisaUsuario(Screen, Geral):
	
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.inst = []

	def remover_widgets(self):
		conteudo = self.ids.conteudo
		for i in range(len(self.inst)):
			conteudo.remove_widget(self.inst[i])

	def carregar_resultados(self, *args):
		conteudo = self.ids.conteudo
		filtro = self.ids.filtro.text
		fv = '%{}%'.format(filtro)

		self.remover_widgets()
		self.inst = []
		
		if (not db.checars("SELECT p.id, p.nome, p.celular, c.modelo as carro FROM pessoas as p INNER JOIN carros as c ON p.carro = c.id WHERE p.nome LIKE ? OR p.celular LIKE ? OR p.carro IN (SELECT id FROM carros WHERE modelo LIKE ?) UNION ALL SELECT p.id, p.nome, p.celular, carro FROM pessoas as p WHERE (p.nome LIKE ? OR p.celular LIKE ?) AND p.carro = '0'", valores=[fv, fv, fv, fv, fv])):
			self.inst.append(FormAviso())
			self.inst[-1].texto = 'Nenhum resultado encontrado'
			conteudo.add_widget(self.inst[-1])

			self.inst.append(Widget())
			conteudo.add_widget(self.inst[-1])
		else:
			res = db.resultado

			# Widgets do Resultado
			pr = PesquisaResultado()
			prc = PesquisaResultadoConteudo()
			# Titulo Tabela
			prt = PesquisaResultadoTitulo()
			prt.add_widget(PesquisaResultadoTituloRotulo(width='60dp', text='Nº'))
			prt.add_widget(PesquisaResultadoTituloRotulo(text='Nome'))
			prt.add_widget(PesquisaResultadoTituloRotulo(text='Celular'))
			prt.add_widget(PesquisaResultadoTituloRotulo(text='Carro'))
			prt.add_widget(PesquisaResultadoTituloRotulo(width='100dp', text='Editar'))
			prt.add_widget(PesquisaResultadoTituloRotulo(width='100dp', text='Excluir'))
			# Adicionando Widgets
			prc.add_widget(prt)

			# Conteúdo
			for i in range(len(res)):
				cor = (.78, .89, .99, 1) if (i % 2 == 0) else (.61, .80, .94, 1)
				numero = '{}.'.format(i + 1)
				ide = res[i]['id']
				nome = res[i]['nome']
				celular = res[i]['celular']
				carro = 'Nenhum' if (res[i]['carro'] == 0) else str(res[i]['carro'])

				# Botões
				boxbt1 = BoxLayout(size_hint=(None, 1), padding='10dp', width='100dp')
				boxbt2 = BoxLayout(size_hint=(None, 1), padding='10dp', width='100dp')
				pcb = PesquisaResultadoComumBotao()
				pcb.icone = 'bt_edicao.png'
				boxbt1.add_widget(pcb)
				pcb = PesquisaResultadoComumBotao()
				pcb.icone = 'bt_excluir.png'
				boxbt2.add_widget(pcb)

				prco = PesquisaResultadoComum()
				prco.cor = cor
				prco.add_widget(PesquisaResultadoComumRotulo(width='60dp', text=numero))
				prco.add_widget(PesquisaResultadoComumRotulo(text=nome))
				prco.add_widget(PesquisaResultadoComumRotulo(text=celular))
				prco.add_widget(PesquisaResultadoComumRotulo(text=carro))
				prco.add_widget(boxbt1)
				prco.add_widget(boxbt2)

				prc.add_widget(prco)

			pr.add_widget(prc)
			self.inst.append(pr)
			conteudo.add_widget(self.inst[-1])

class TelaPesquisaMarca(Screen, Geral):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.inst = []

	def remover_widgets(self):
		conteudo = self.ids.conteudo
		for i in range(len(self.inst)):
			conteudo.remove_widget(self.inst[i])

	def carregar_resultados(self, *args):
		conteudo = self.ids.conteudo
		filtro = self.ids.filtro.text

		self.remover_widgets()
		self.inst = []

		if (not db.checar('marcas', 'WHERE marca LIKE ?', 'id, marca', valores=['%{}%'.format(filtro)])):
			self.inst.append(FormAviso())
			self.inst[-1].texto = 'Nenhum resultado encontrado'
			conteudo.add_widget(self.inst[-1])

			self.inst.append(Widget())
			conteudo.add_widget(self.inst[-1])
		else:
			res = db.resultado

			# Widgets do Resultado
			pr = PesquisaResultado()
			prc = PesquisaResultadoConteudo()
			# Titulo Tabela
			prt = PesquisaResultadoTitulo()
			prt.add_widget(PesquisaResultadoTituloRotulo(width='60dp', text='Nº'))
			prt.add_widget(PesquisaResultadoTituloRotulo(text='Marca'))
			prt.add_widget(PesquisaResultadoTituloRotulo(width='100dp', text='Editar'))
			prt.add_widget(PesquisaResultadoTituloRotulo(width='100dp', text='Excluir'))
			# Adicionando Widgets
			prc.add_widget(prt)

			# Conteúdo
			for i in range(len(res)):
				cor = (.78, .89, .99, 1) if (i % 2 == 0) else (.61, .80, .94, 1)
				numero = '{}.'.format(i + 1)
				ide = res[i]['id']
				marca = res[i]['marca']

				# Botões
				boxbt1 = BoxLayout(size_hint=(None, 1), padding='10dp', width='100dp')
				boxbt2 = BoxLayout(size_hint=(None, 1), padding='10dp', width='100dp')
				pcb = PesquisaResultadoComumBotao()
				pcb.icone = 'bt_edicao.png'
				boxbt1.add_widget(pcb)
				pcb = PesquisaResultadoComumBotao()
				pcb.icone = 'bt_excluir.png'
				boxbt2.add_widget(pcb)

				prco = PesquisaResultadoComum()
				prco.cor = cor
				prco.add_widget(PesquisaResultadoComumRotulo(width='60dp', text=numero))
				prco.add_widget(PesquisaResultadoComumRotulo(text=marca))
				prco.add_widget(boxbt1)
				prco.add_widget(boxbt2)

				prc.add_widget(prco)

			pr.add_widget(prc)
			self.inst.append(pr)
			conteudo.add_widget(self.inst[-1])


# [3. Criando Gerenciador de Telas e Adicionando as Telas]:

# Gerenciador de Telas
sm = GerenciadorDeTelas()
# Adicionando Telas
sm.add_widget(TelaPesquisa(name='tela_pesquisa'))
sm.add_widget(TelaPesquisaCarro(name='tela_pesquisa_carro'))
sm.add_widget(TelaPesquisaUsuario(name='tela_pesquisa_usuario'))
sm.add_widget(TelaPesquisaMarca(name='tela_pesquisa_marca'))
sm.add_widget(TelaCadastroCarro(name='tela_cadastro_carro'))
sm.add_widget(TelaCadastroUsuario(name='tela_cadastro_usuario'))
sm.add_widget(TelaCadastroMarca(name='tela_cadastro_marca'))

# [4. Classe Principal]:
class Programa(App):
	title = 'Registrador CarX3'
	def build(self):
		return sm

# Rodando o programa
Programa().run()