import re

class VisualGCode():

	def __init__(self, code):
		self.code = code
		self.so_algoritmo = code.split("Inicio")[1] if "Inicio" in  code else code


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
			'facaEnquanto':self.facaEnquanto
		}

	def compreenderTipo(self, codigo):
		tipos = {
			'atribuicaoVariavel': r'(\w+) *<- *(.+)',
			'selecaoSe': r'se \((((\w+) *([<>=]{1}[>=]?) *(\w+) *)+)\) entao',
			'senao': r'senao',
			'lacoEnquanto': r'lacoEnquanto',
			'lacoPara': r'lacoPara',
			'escolhaCaso': r'escolhaCaso',
			'escreva': r'escreva',
			'leia': r'leia',
			'repitaAte': r'repitaAte',
			'facaEnquanto': r'facaEnquanto'
		}

		for tipo in tipos:
			if re.match(tipos[tipo], codigo):
				return tipo

		return -1

	def converterPraPython(self):
		linhas = self.so_algoritmo.split("\n")
		codigo = ''
		tabs = ''
		for i in linhas:
			tipo = self.compreenderTipo(i)
			if tipo in self.tipos:
				codigoConvertido, tab = self.tipos[tipo](i)
				
				if (tab == 1):
					tab += '\n'
				if (tab == -1):
					tabs = tabs[:-1]

				codigo += tabs + codigoConvertido
			codigo += '\n'

		self.codigo_em_visualg = codigo
		return codigo


	def atribuicaoVariavel(self, codigo):
		nomeVariavel, valor = re.match(r'(\w+) *<- *(.+)', codigo).groups()
		return "{0} = {1}".format(nomeVariavel, valor), 0

	def selecaoSe(self, codigo):
		pass

	def senao(self, codigo):
		pass

	def lacoEnquanto(self, codigo):
		pass

	def lacoPara(self, codigo):
		pass

	def escolhaCaso(self, codigo):
		pass

	def escreva(self, codigo):
		pass

	def leia(self, codigo):
		pass


	def repitaAte(self, codigo):
		pass

	def facaEnquanto(self, codigo):
		pass


#codigo = "z<- 10"

codigo = """Algoritmo "semnome"
// AP1 
// Eu kkkk 
// Descrição   : Aqui você descreve o que o programa faz! (função)
// Autor(a)    : Nome do(a) aluno(a)
// Data atual  : 19/11/2019
Var
// Seção de Declarações das variáveis 
inteiro: x, y
real: z

Inicio
// Seção de Comandos, procedimento, funções, operadores, etc... 
x<-30
y<-10
z <- (x+y)/2

Fimalgoritmo"""
codigo_visualg = VisualGCode(codigo)
codigo_visualg.converterPraPython()
print(codigo_visualg.codigo_em_visualg)

exec(codigo_visualg.codigo_em_visualg)

print(z)
