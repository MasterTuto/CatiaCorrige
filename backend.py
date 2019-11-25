import sqlite3
import re
import os

class BaseDeDados:
    def __init__(self, caminho='', nome=''):
        self.caminho = caminho
        self.nome = nome
        self.conexao = sqlite3.connect(caminho + '\\' + nome + '.bd')
        self.database = self.conexao.cursor()


    def criarTabelaProva(self):
        query = """CREATE TABLE IF NOT EXISTS prova_questoes (
            id_questao INTEGER AUTO INCREMENT PRIMARY KEY,
            descricao  TEXT NOT NULL,
            valor      REAL NOT NULL
        );"""
        
        self.database.execute(query)

    def criarTabelaAluno(self):
        query = """CREATE TABLE IF NOT EXISTS {0}  (
            id_aluno INTEGER AUTO INCREMENT PRIMARY KEY,
            nome_completo TEXT NOT NULL,
            nota_final REAL,
            
            matricula TEXT NOT NULL);
        """.format(self.nome)
        self.database.execute(query)

        query = """CREATE TABLE IF NOT EXISTS notas (
            id_nota INTEGER AUTO INCREMENT PRIMARY KEY,
            questao TEXT NOT NULL,
            nota REAL NOT NULL,
            id_aluno INTEGER NOT NULL,

            FOREIGN KEY (id_nota) REFERENCES {0}(id_aluno)
            
        );""".format(self.nome)
        self.database.execute(query)

    def cadastrarAluno(self):
        query = "INSERT INTO {0} (nome_completo, matricula) VALUES ('{0}', '{1}');" .format(
            self.nome, self.matricula)
        
        self.database.execute(query)
        return self.database.lastrowid

    def adicionarNota(self, nota, questao):
        self.database.execute("INSERT INTO notas SET questao={0}, nota={1}, id_aluno={2};".format(questao, nota, 1) )
        return self.database.lastrowid

    def editarNota(self, nota, questao):
        query = "UPDATE notas SET nota = %s WHERE questao=%s" % (nota, questao)

        self.database.execute(query)

    def obterDescricaoDaQuestao(self, questao):
        dados = (questao,)
        query = "SELECT descricao FROM prova_questoes WHERE id_questao = ?"
        query = self.database.execute(query, dados).fetchall()
        return query[0][0]

    def cadastrarQuestaoProva(self, descricao, valor):
        query = "INSERT INTO prova_questoes (descricao, valor) VALUES ('%s', %f);" % (descricao, valor)

        #query = "INSERT INTO prova_questoes SET descricao = '%s', valor=%d" % (descricao, valor)
        print(query)

        self.database.execute(query)

    def fecharConexao(self):
        self.conexao.close()


    def obterQuestoes(self):
        query = "SELECT * FROM prova_questoes ORDER BY id_questao"
        query = self.database.execute(query)

        return query.fetchall()

    def apagarProva(self):
        query = "DROP TABLE prova_questoes"
        self.database.execute(query)

    def editarQuestao(self, descricao='', valor=-1):
        query = "UPDATE prova_questoes SET "
        if (descricao != ''):
            query += ' descricao = \'' + descricao + '\' '
        if (valor != -1):
            query += ' valor = %f ' % (valor)
        
        if query == "UPDATE prova_questoes SET ":
            return False

        query += ';'

        self.database.execute(query)

    def apagarQuestao(self, questao_id):
        query = "DELETE FROM prova_questoes WHERE id_questao = %s;" % (questao_id)

        self.database.execute(query)

    def obterValorProva(self):
        query = "SELECT SUM(valor) FROM prova_questoes;"
        query = self.database.execute(query).fetchall()
        return query[0][0]

    def obterNota(self, questao):
        query = "SELECT nota FROM notas WHERE questao = %d;" % (questao)
        query = self.database.execute(query).fetchall()
        return query[0][0]

    def obterNotaAluno(self):
        query = "SELECT SUM(nota) FROM notas;"
        query = self.database.execute(query).fetchall()
        return query[0][0]

    def obterNotas(self):
        query = "SELECT nota FROM notas;"
        query = self.database.execute(query).fetchall()
        return query

    def registrarNota(self, questao, nota):
        query = "INSERT INTO notas (questao, nota, id_aluno) VALUES (%d, %f, %d);" % (questao, nota, 1)
        self.database.execute(query)

    def obterMatricula(self):
        query = "SELECT matricula FROM {};".format(self.nome)
        query = self.database.execute(query).fetchall()
        matricula = query[0][0]
        return matricula

    def mudarMatricula(self, matricula):
        query = "UPDATE {0} SET matricula = {1};".format(self.nome, matricula)
        self.database.execute(query)

    def mudarNome(self, novo_nome):
        query = "UPDATE {} SET nome_completo = '{1}';".format(self.nome, novo_nome)
        self.database.execute(query)

class Prova(BaseDeDados):
    numeroDeQuestoes = 0
    
    def __init__(self, caminho):
        super().__init__(caminho, 'prova')

    def obterQuestao(self, indice):
        questoes = self.obterQuestoes()
        return Questao(questoes[indice])

class Questao():
    def __init__(self, dados):
        self.id_questao = dados[0]
        self.descricao  = dados[1]
        self.valor      = dados[2]
        

    def obterDescricao(self):
        return self.descricao

    def obterValor(self):
        return self.valor

    def obterNumero(self):
        return self.id_questao
        

class pastaProjetos(object):
    def __init__(self, path):
        self.path = path
        self.__processarProjetos(path)
        
    def __processarProjetos(self, path):
        self.projetos = {}
        pastas = os.listdir(path)
        reg = r'([\w]+)_(\w+)_(\w+)'
        for pasta in pastas:
            it_matches = re.match(reg, pasta)

            if (it_matches):
                nome_aluno, semestre, n_matricula = it_matches.groups()
                caminho = path + '\\' + pasta
                
                self.projetos[nome_aluno] = Aluno({
                    'Nome': nome_aluno,
                    'Semestre': semestre,
                    'Matricula': n_matricula,
                    'Caminho': caminho,
                    'Respostas': os.listdir(caminho)
                })


    def listarProjetos(self):
        for aluno in self.projetos:
            print(aluno,
                  'Matricula: '+self.projetos[aluno].obterMatricula(),
                  'Respostas: ',self.projetos[aluno].obterRespostas(),
                  sep='\n\n')
        return True

    def obterAlunos(self):
        return self.projetos

    def obterDadosAluno(self, aluno):
        return self.projetos[aluno]

    def obterRespostas(self, aluno):
        return self.projetos[aluno]['Respostas']


class Aluno(BaseDeDados):
    def __init__(self, dados):
        self.nome = dados['Nome']
        self.semestre = dados['Semestre']
        self.matricula = dados['Matricula']
        self.respostas = dados['Respostas']
        self.caminho = dados['Caminho']
        
        super().__init__(self.caminho, self.nome)


    def obterNome(self):
        return self.nome

    def obterMatricula(self):
        return self.matricula

    def obterRespostas(self):
        return self.respostas

caminho = "C:\\Users\\breno\\Documents\\TESTESAp1\\"#input("Digite o caminho das pastas: ")   
obj = pastaProjetos(caminho)
prova = Prova(caminho)
prova.criarTabelaProva()

n_questoes = int(input("Digite o numero de questoes da prova: "))

for i in range(n_questoes):
    print("Digite a descrição da questão, entre 'ACABAR' para parar de digitar.\n")
    descricao = ''
    c = input("")
    while(c != 'ACABAR'):
        descricao += c
        c = input("")

    valor = float(input("Digite o valor da questao: "))
    prova.cadastrarQuestaoProva(descricao, valor)

print("===========\nA PROVA VALE %s\n===============" % prova.obterValorProva())


alunos = obj.obterAlunos()
for aluno in alunos:
    print("========================")
    print("ALUNO: " + aluno)
    
    n = n_questoes
    indiceProva = 1
    alunos[aluno].criarTabelaAluno()
    alunos[aluno].cadastrarAluno()
    while (n > 0):
        nota = float(input("Digite a nota da %sª prova: " % indiceProva))
        n-=1

        alunos[aluno].registrarNota(indiceProva, nota)
        indiceProva += 1

print("===================", "Testando Resultados!!", "=========================", sep='\n')

for aluno in alunos:
    print("===========================")
    print("Aluno: ", aluno)
    print("Nota: ", alunos[aluno].obterNotaAluno())

print("===========================================")
numeroQuestoes = len(prova.obterQuestoes())
for i in range(numeroQuestoes):
    print("Questao %i" % i)
    questao = prova.obterQuestao(i)
    print("Descricao: " + questao.obterDescricao() + '\n') 

            
'''
caminho = "C:\\Users\\breno\\Documents\\TESTESAp1\\"#input("Digite o caminho das pastas: ")
obj = pastaProjetos(caminho)
aluno1 = obj.obterDadosAluno('JoaoCarvalho')
aluno1.criarTabelaAluno()
aluno1.cadastrarAluno(201911648, '20191')

prova = Prova(caminho)
prova.criarTabelaProva()
prova.cadastrarQuestaoProva("Recebe um inteiro", 3.5)

aluno1.registrarNota(1, 3.0)

print("=========================")
print(aluno1.obterNota(1))
print(prova.obterQuestoes())
#prova.apagarProva()
prova.cadastrarQuestaoProva(descricao="Cadastre meu nome", valor=2.5)

print(prova.obterQuestoes())
print(prova.obterValorProva())
aluno1.registrarNota(2, 1.5)

print(aluno1.obterNotas())
print(aluno1.obterNotaAluno())

print("===== Aluno 2 =====")
print(obj.obterAlunos())
aluno2 = obj.obterDadosAluno('BrenoCarvalhoDaSilva')
aluno2.criarTabelaAluno()
aluno2.cadastrarAluno(1512, 20191)
aluno2.registrarNota(1, 3.5)
aluno2.registrarNota(2, 2.5)
print(aluno2.obterNota(1))
print(aluno2.obterNotas())
print(aluno2.obterNotaAluno())


'''