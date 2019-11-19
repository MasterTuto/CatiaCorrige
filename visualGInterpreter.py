import re

class VisualGCode():

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
			'escreva': self.escreva,
			'leia': self.leia,
			'repitaAte': self.repitaAte,
			'facaEnquanto':self.facaEnquanto,
		}

	def processarTiposDasVariaveis(self, areaVariaveis):
		for linha in areaVariaveis.split('\n'):
			if linha == '': continue
			nomes, tipo = linha.split(":")

			tipo = tipo.strip()
			for variavel in nomes.split(","):
				variavel = variavel.strip()
				self.tiposDasVariaveis[variavel] = tipo

	def compreenderTipo(self, codigo):
		tipos = {
			'atribuicaoVariavel': r'(\w+) *<- *(.+)',
			'selecaoSe': r'se \((((\w+) *([<>=]{1}[>=]?) *(["\']?[\w]+["\']?") *)+)\) entao',
			'senao': r'senao',
			'lacoEnquanto': r'enquanto \((((\w+) *([<>=]{1}[>=]?) *(\w+) *)+)\) faca',
			'lacoPara': r'para +[a-zA-Z0-9]+ +de +[a-zA-Z0-9]+ +ate +[a-zA-Z0-9]+ *(passo +[a-zA-Z0-9]+)?',
			'escolhaCaso': r'escolhaCaso',
			'escreva': r'[\w ]*escreva(l?)\(([\'"]?.+[\'"]?)\)',
			'leia': r'[ \w]*leia\(( *[a-zA-Z0-9]+ *)\)',
			'repitaAte': r'repitaAte',
			'facaEnquanto': r'facaEnquanto',

			'fimse': r'fimse',
			'fimenquanto': r'fimenquanto',
			'fimpara': r'fimpara',
			'fimrepita': r'fimrepita',
			'fimfaca': r'fimfaca',

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
			print(linha)
			if tipo in self.tipos:
				print(tipo)
				codigoConvertido, tab = self.tipos[tipo](linha)

				codigo += tabs + codigoConvertido if tipo != 'senao' else tabs[:-1] + codigoConvertido
				
				if (tab == 1):
					tabs += '\t'
				if (tab == -1):
					tabs = tabs[:-1]
			codigo += '\n'

		self.codigo_em_visualg = codigo
		return codigo


	def atribuicaoVariavel(self, codigo):
		nomeVariavel, valor = re.match(r'(\w+) *<- *(.+)', codigo).groups()
		return "{0} = {1}".format(nomeVariavel, valor), 0

	def selecaoSe(self, codigo):
		reg = r'se \((((\w+) *([<>=]{1}[>=]?) *(["\']?[\w]+["\']?") *)+)\) entao'
		primeiroValor, operador, segundoValor = re.match(reg, codigo).groups()[2:]
		if (operador == '<>'):
			operador = "!="
		elif (operador == "="):
			operador = "=="

		return "if ({0} {1} {2}):".format(primeiroValor, operador, segundoValor), 1

	def senao(self, codigo):
		return 'else:', 0

	def fimse(self, codigo):
		return '\n', -1

	def escreva(self, codigo):
		reg = r'[ \t]*escreva(l?)\(([\'"]?.*[\'"]?)\)'
		l, mensagem = re.match(reg, codigo).groups()

		return ("print({0})".format(mensagem), 0) if l else ("print({0}, end='')".format(mensagem), 0)
	

	def lacoEnquanto(self, codigo):
		pass

	def lacoPara(self, codigo):
		pass

	def escolhaCaso(self, codigo):
		pass

	def leia(self, codigo):
		print("===1230132")
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


codigo = """
Algoritmo "semnome"
// Descobrir maior
// Descrição   : Descobre o maior numero
// Autor(a)    : Breno Carvalho da Siva
// Data atual  : 28/08/2019
Var
n1: inteiro
n2: inteiro

Inicio
escreval("Insira seu nome: ")
leia(n1)

n2 <- 10

se (n1 > n2) entao
		escreval("Eh maior, porra!!")



Fimalgoritmo"""
print(codigo)
print("===============================================")
codigo_visualg = VisualGCode(codigo)
codigo_visualg.converterPraPython()
#print(codigo_visualg.codigo_em_visualg)
print("===============================================")
print("===============================================")

print(codigo_visualg.codigo_em_visualg)

print("===============================================")
print("===============================================")

print("Saida do codigo: ")
exec(codigo_visualg.codigo_em_visualg)
	