import re
import datetime

class Ferramentas():
	def mascara(self, texto, mascara, apenas_numeros=True):
		# Removendo caracteres não numéricos se True
		if (apenas_numeros == True):
			texto = re.sub(r"[^0-9]", '', texto)

		# Máscaras padrão
		if (mascara == 'cpf'):
			mascara = '###.###.###-##'
		elif (mascara == 'cnpj'):
			mascara = '##.###.###/####-##'
		elif (mascara == 'dddtel'):
			mascara = '(##) ####-####'
		elif (mascara == 'tel'):
			mascara = '####-####'
		elif (mascara == 'dddcel'):
			mascara = '(##) # ####-#####'
		elif (mascara == 'cel'):
			mascara = '# ####-#####'
		elif (mascara == 'cep'):
			mascara = '#####-###'
		elif (mascara == 'data'):
			mascara = '##-##-####'
		elif (mascara == 'datai'):
			mascara = '####-##-##'
		else:
			mascara = mascara

		# Iniciando troca da máscara pelo texto
		mascarado = ''
		j = 0
		sa = 0 # Separadores Adicionados
		for i in range(len(mascara)):

			if (mascara[i] == '#'):
				try:
					texto[j]
					mascarado += texto[j]
					j += 1
				except:
					pass
			else:
				if ((len(texto) + sa) < i + 1):
					break
				try:
					mascara[i]
					mascarado += mascara[i]
					sa += 1
				except:
					pass

		return mascarado

	def checar_data(self, data, formato='nacional'):
		try:
			if (formato == 'nacional'):
				datetime.datetime.strptime(data, '%d-%m-%Y')
			else:
				datetime.datetime.strptime(data, '%Y-%m-%d')
			return True
		except:
			return False

	def filtrar(self, texto, tipo='nome'):
		if (tipo == 'nome'):
			texto = re.sub(r"[^A-ZÀ-ÄÒ-ÖÙ-ÜÇ-Ï .]", '', texto, flags=re.MULTILINE | re.IGNORECASE)
		elif (tipo == 'numero'):
			texto = re.sub(r"[^0-9]", '', texto, flags=re.MULTILINE | re.IGNORECASE)
		return texto

	def verificar_post(self, nomes, post):
		for i in range(len(nomes)):
			if (nomes[i] not in post):
				return False
		return True