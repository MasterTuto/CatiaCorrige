import re

implementacaoEscolhaCaso = """
class escolha(object):
    def __init__(self, valor):
        self.valor = valor
        self.terminou = False

    def __iter__(self):
        yield self.tentativa
        raise StopIteration

    def tentativa(self, *args):
        if self.terminou or not args:
            return True
        elif self.valor in args:
            self.terminou = True
            return True
        else:
            return False
"""

class VisualGCode():
	tempEscolhaCaso = []
	poeBreak = False
	jaPosImplementacao = False

	def __init__(self, code):
		self.code = code
		self.so_algoritmo = code.split("Inicio")[1] if "Inicio" in  code else code

		areaVariaveis = code.split("Var")[1].split("Inicio")[0]
		self.tiposDasVariaveis = {}
		self.processarTiposDasVariaveis(areaVariaveis)


		self.tipos = {
			'atribuicaoVariavel': self.atribuicaoVariavel,
			'selecaoSe': self.selecaoSe,
			'senao': self.senao,
			'lacoEnquanto': self.lacoEnquanto,
			'lacoPara': self.lacoPara,
			'escolhaCaso': self.escolhaCaso,
			'caso': self.caso,
			'escreva': self.escreva,
			'leia': self.leia,
			'repitaAte': self.repitaAte,
			'facaEnquanto':self.facaEnquanto,
			'fimse': self.fimse,
			
			'fimenquanto': lambda x: ('',-1),#self.fimenquanto,
			'fimpara': lambda x: ('', -1),
			'fimescolha': lambda x: ('', -2),
			'outrocaso': lambda x: ('if (caso()):', 0),
			'interrompa': lambda x: ('break', -1)
		}

	def processarTiposDasVariaveis(self, areaVariaveis):
		for linha in areaVariaveis.split('\n'):
			linha = linha.strip()
			if not re.match(r'((?:[\t ]*([\w\_,]+)+))*: *(inteiro|real|logico|caractere)', linha, re.IGNORECASE):
				continue

			nomes, tipo = linha.strip().split(":")

			tipo = tipo.strip()
			for variavel in nomes.split(","):
				variavel = variavel.strip()
				self.tiposDasVariaveis[variavel] = tipo

	def compreenderTipo(self, codigo):
		tipos = {
			'atribuicaoVariavel': r'(\w+) *<- *(.+)',
			'selecaoSe': r'se \(((([a-zA-Z0-9% ]+) *([<>=]{1}[>=]?) *(["\']?[a-zA-Z0-9]+["\']?) *)+)\) ent(?:a|ã)o',
			'senao': r'sen(?:a|ã)o',
			'lacoEnquanto': r'enquanto \(((( *\(? *?(\w+) *([<>=]{1}[>=]?) *(\w+) *\)? *)(e|ou)? *)+)\) fa(?:c|ç)a',
			'lacoPara': r'para +([\w\_\(\)\*\+\-\/]+) +de +([\w\_\(\)\*\+\-\/]+) +ate +([\w\_\(\)\*\+\-\/]+) *(?:passo +([\w\_\(\)\*\+\-\/]+))? *fa(?:ç|c)a',
			'escolhaCaso': r'[ \t]*escolha +[\w_]+',
			'caso': r'[ \t]*caso +[\w_]+',
			'escreva': r'[\w ]*escreva(l?)\(([\'"]?.+[\'"]?)\)',
			'leia': r'[ \w]*leia\(( *[a-zA-Z0-9]+ *)\)',
			'repitaAte': r'repitaAt(?:é|e)',
			'facaEnquanto': r'facaEnquanto',

			'fimse': r'fimse',
			'fimenquanto': r'fimenquanto',
			'fimpara': r'fimpara',
			'fimrepita': r'fimrepita',
			'fimfaca': r'fimfaca',
			'fimescolha': r'fimescolha',

			'outrocaso': r'outrocaso',
			'interrompa': r'interrompa'

		}


		for tipo in tipos:
			if re.match(tipos[tipo], codigo):
				return tipo

		return -1

	def converterPraPython(self):
		linhas = self.so_algoritmo.split("\n")
		codigo = ''
		tabs = ''
		for linha in linhas:
			linha = linha.strip()
			tipo = self.compreenderTipo(linha)
			if tipo in self.tipos:
				if self.poeBreak and (tipo == 'caso' or tipo == "outrocaso" or tipo == "fimescolha"):
					codigo += tabs + "break\n"

				if (tipo == "escolhaCaso" and not self.jaPosImplementacao):
					codigo =  implementacaoEscolhaCaso + "\n" + codigo
					jaPosImplementacao = True
				
				codigoConvertido, tab = self.tipos[tipo](linha)

				if tipo == 'senao':
					codigo += tabs[:-2] + codigoConvertido
				elif tipo == "caso" or tipo == "outrocaso":
					codigo += tabs[:-2] + codigoConvertido
					self.poeBreak = True
				else:
					codigo += tabs + codigoConvertido
				
				if (tab >= 1):
					tabs += '  '*tab
				if (tab <= -1):
					tabs = tabs[:tab*2]



			codigo += '\n'

		self.codigo_em_python = codigo
		return codigo


	def atribuicaoVariavel(self, codigo):
		nomeVariavel, valor = re.match(r'(\w+) *<- *(.+)', codigo).groups()
		return "{0} = {1}".format(nomeVariavel, valor), 0

	def selecaoSe(self, codigo):
		reg = r'se \(((([a-zA-Z0-9% ]+) *([<>=]{1}[>=]?) *(["\']?[a-zA-Z0-9]+["\']?) *)+)\) ent(?:a|ã)o'
		primeiroValor, operador, segundoValor = re.match(reg, codigo).groups()[2:]
		if (operador == '<>'):
			operador = "!="
		elif (operador == "="):
			operador = "=="

		return "if ({0} {1} {2}):".format(primeiroValor, operador, segundoValor), 1

	def senao(self, codigo):
		return 'else:', 0

	def fimenquanto(self, codigo):
		return '\n', -1
	
	def fimse(self, codigo):
		return '\n', -1

	def escreva(self, codigo):
		reg = r'[ \t]*escreva(l?)\(([\'"]?.*[\'"]?)\)'
		l, mensagem = re.match(reg, codigo, re.I).groups()

		return ("print({0})".format(mensagem), 0) if l else ("print({0}, end='')".format(mensagem), 0)
	

	def lacoEnquanto(self, codigo):
		reg = r'enquanto \(((([\w]+) *([<>=]{1}[>=]?) *(["\']?[\w]+["\']?) *)+)\) faca'
		primeiroValor, operador, segundoValor = re.match(reg, codigo).groups()[2:]
		if (operador == '<>'):
			operador = "!="
		elif (operador == "="):
			operador = "=="

		return "while ({0} {1} {2}):".format(primeiroValor, operador, segundoValor), 1

		def mostrarGrupos(abc):

			return 'while' + abc.group(2) + ':'
		
		reg = r'(enquanto)([\W\d\w]+)(fa(?:c|ç)a)'
		codigo = re.sub(reg, mostrarGrupos, codigo)
		return codigo, 1

	def lacoPara(self, codigo):
		print("teste")
		def trocarPara(codigo):
			passo = codigo.group(4)
			if not passo: passo = 1

			return 'for {0} in range({1}, {2}, {3}):'.format(codigo.group(1),
															codigo.group(2),
															codigo.group(3),
															passo)

		reg = r"para +([\w\_\(\)\*\+\-\/]+) +de +([\w\_\(\)\*\+\-\/]+) +ate +([\w\_\(\)\*\+\-\/]+) *(?:passo +([\w\_\(\)\*\+\-\/]+))? *fa(?:ç|c)a"

		codigo = re.sub(reg, trocarPara, codigo)
		return codigo, 1

	def caso(self, codigo):
		reg = r'[ \t]*caso +([\w_]+)'
		valorVariavel = re.match(reg, codigo, re.IGNORECASE).group(1)
		return "if caso({0}):".format(valorVariavel), 0


	def escolhaCaso(self, codigo):
		reg = r'[ \t]*escolha +([\w_]+)'
		nomeVariavel = re.match(reg, codigo, re.IGNORECASE).group(1)
		self.tempEscolhaCaso.append(nomeVariavel)
		return "for caso in escolha(" + nomeVariavel + "):", 2
		

	def leia(self, codigo):
		reg = r'[ \w]*leia\(( *[a-zA-Z0-9]+ *)\)'
		nomeVariavel = re.match(reg, codigo).groups()[0]
		tipo = self.tiposDasVariaveis[nomeVariavel]
		if (tipo == 'inteiro'):
			tipo = 'int'
		elif (tipo == "real"):
			tipo = 'float'
		elif (tipo == 'caractere'):
			tipo = 'str'
		elif (tipo == 'logico'):
			tipo = 'bool'

		return "{0} = {1}(input())".format(nomeVariavel, tipo), 0


	def repitaAte(self, codigo):
		pass

	def facaEnquanto(self, codigo):
		pass


import os
index = 0
itens = os.listdir('.')
for item in itens:
	print("[%s] %s" % (index, item))
	index += 1

escolha_ = int(input("Escolha qual arquivo executar (digite o numero correspondente): "))
arquivo = open(itens[escolha_], 'r')
codigo = arquivo.read()
arquivo.close()


codigo_visualg = VisualGCode(codigo)
codigo_visualg.converterPraPython()
#print(codigo_visualg.codigo_em_python)
print("===============================================")
print(codigo_visualg.codigo_em_python)
print("===============================================")
print("Saida do codigo: ")
exec(codigo_visualg.codigo_em_python)
	