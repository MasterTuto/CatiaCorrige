import sqlite3
import pathlib
import random
import utils
import re

class BD_CRUD:
    def __init__(self, conexao, cursor_conexao):
        self.conexao = conexao
        self.cursor_conexao = cursor_conexao

    def query(self, txt_query, dicionario_itens={}):
        if (dicionario_itens):
            query = self.cursor_conexao.execute(txt_query, dicionario_itens)

            if (query):
                if (txt_query.startswith('SELECT')):
                    a = query.fetchall()
                    return a
                else:  
                    return query
            else:
                return False
        else:
            query = self.cursor_conexao.execute(txt_query)
            return query.fetchall()

    def check_table_existence(self, nome_tabela):
        try:
            self.read(nome_tabela)
            return True
        except sqlite3.OperationalError:
            return False

    def create_table(self, nome_tabela, colunas_e_tipos):

        '''
        template colunas_e_tipos:
            [('c1', 'int primary key not null'), ('c2', 'text'), ...]
        '''
        colunas_para_query = ', '.join(['%s %s'%(c[0], c[1]) for c in colunas_e_tipos])
        query = 'CREATE TABLE {0} ({1});'.format(nome_tabela, colunas_para_query)
        self.query(query)

    def create(self, tabela, valores):
        nomes_colunas = ""
        valores_colunas = ""
        for valor in valores:
            nomes_colunas += "%s, " % valor
            valores_colunas += ":%s, " % valor

        nomes_colunas = nomes_colunas.rstrip(', ')
        valores_colunas = valores_colunas.rstrip(', ')

        query = "INSERT INTO {0} ({1}) VALUES ({2})".format(tabela, nomes_colunas, valores_colunas)
        return self.query(query, valores)

    def read(self, tabela, itens_para_buscar=("*"), where={}, order_by=(), group=()):
        itens_para_buscar = ', '.join(itens_para_buscar)

        texto_where = ' WHERE '
        for chave in where:
            texto_where += "%s=:%s, " % (chave, chave)
        texto_where = texto_where.rstrip(', ')

        texto_group = ' GROUP BY ' + ', '.join(group)

        texto_order_by = ' ORDER BY ' + ", ".join(order_by)

        query = "SELECT {} FROM {}".format(itens_para_buscar, tabela)

        if where:
            query += texto_where

        if group:
            query += texto_group

        if  order_by:
            query += texto_order_by
        query += ';'

        return self.query(query, where)

    def update(self, tabela, novo_valor, chaves={}):
        texto_novo_valor = ''
        for chave in novo_valor:
            texto_novo_valor += ' %s=:%s, ' % (chave, chave)
        texto_novo_valor = texto_novo_valor.rstrip(', ')

        texto_chaves = ' WHERE'
        novas_chaves = {}
        for chave in chaves:
            texto_chaves += ' %s=:%s_chaves AND ' % (chave, chave)
            novas_chaves[chave + '_chaves'] = chaves[chave]

        texto_chaves = texto_chaves.rstrip(' AND ')

        base_query = 'UPDATE {} SET {}'.format(tabela, texto_novo_valor)
        if novas_chaves:
           base_query += texto_chaves
        
        novo_valor.update(novas_chaves)
        return self.query(base_query, novo_valor)

    def delete(self, tabela, where):
        texto_where = ''
        for chave in where:
            texto_where += " {0}=:{0}, " % (chave)
        texto_where.rstrip(', ')

        query = "DELETE FROM tabela WHERE " + texto_where
        return self.query(query, where)

    def applyChanges(self):
        self.conexao.commit()

class Prova(BD_CRUD):
    CDG_OK = 1
    CDG_JA_EXISTE_NUMERO = 2
    def __init__(self, conexao, cursor_conexao):
        self.questoes = {}
        self.conexao = conexao
        self.cursor_conexao = cursor_conexao

        BD_CRUD.__init__(self, self.conexao, self.cursor_conexao)

    def criarProva(self):
        if not (self.check_table_existence('tbl_prova')):
            self.create_table('tbl_prova', [('titulo_prova', 'VARCHAR(255)'),
                                             ('numero_questao', 'INT'),
                                             ('valor_questao', 'REAL'),
                                             ('enunciado', 'TEXT'),
                                             ('FOREIGN KEY (numero_questao)', 'REFERENCES tbl_criterios(id_questao)'),
                                             ('FOREIGN KEY (numero_questao)', 'REFERENCES tbl_notas(questao)')])

    def criarQuestaoEmBranco(self, numero_questao):
        questao = Questao(numero_questao, conexao=self.conexao, cursor_conexao=self.cursor_conexao)
        codigo = questao.cadastrarQuestaoEmBranco()
        
        if codigo == self.CDG_OK:
            self.questoes[numero_questao] = questao
            return questao
        elif codigo == self.CDG_JA_EXISTE_NUMERO:
            return False

    def obterQuestao(self, numero_questao):
        if (numero_questao in self.questoes):
            return self.questoes[numero_questao]
        else:
            resultado = self.read('tbl_prova',  where={'numero_questao': numero_questao})
            if (resultado):
                resultado = resultado[0]
                questao = Questao(resultado['numero_questao'],
                               resultado['valor_questao'],
                               resultado['enunciado'],
                               conexao=self.conexao,
                               cursor_conexao=self.cursor_conexao)
                self.questoes[numero_questao] = questao
                return questao
            else:
                return False

    def obterQuestoes(self):
        return self.questoes

    def apagarQuestao(self, numero_questao):
        if (isinstance(numero_questao, int)):
            pass
        elif (isinstance(numero_questao, Questao)):
            numero_questao = numero_questao.obterNumeroQuestao()

        for criterio in self.questoes[questao].obterCriterios():
            self.delete('tbl_criterios', {'id_criterio': criterio.obterIdCriterio()})

        self.delete('tbl_prova', {'numero_questao': numero_questao})
        self.delete('tbl_notas', {'questao': numero_questao})
        
        if deu_certo:
            del self.questoes[numero_questao]
            return True
        else:
            return False

    def trocarQuestao(self, questao1, questao2, numero_temporario):
        if (isinstance(questao1, Questao)):
            questao1 = questao1
        elif (isinstance(questao1, int)):
            questao1 = self.questoes[questao1]

        if (isinstance(questao2, Questao)):
            questao2 = questao2
        elif (isinstance(questao2, int)):
            questao2 = self.questoes[questao2]

        id_questao1 = questao1.obterNumeroQuestao()
        id_questao2 = questao2.obterNumeroQuestao()

        questao1.editarNumeroQuestao(numero_temporario)
        questao2.editarNumeroQuestao(id_questao1)
        questao1.editarNumeroQuestao(id_questao2)

    def __bool__(self): # Substitui "ja existe prova"
        return self.check_table_existence('tbl_prova')

    def __iter__(self): # Para percorrer as questoes
        pass

class Questao(BD_CRUD):
    CDG_OK = 1
    CDG_JA_EXISTE_NUMERO = 2
    def __init__(self, numero_questao, valor_questao=0, enunciado='', conexao=False, cursor_conexao=False):
        self.numero_questao = numero_questao
        self.valor_questao = valor_questao
        self.enunciado = enunciado
        self.criterios = {}

        BD_CRUD.__init__(self, conexao, cursor_conexao)

    def __hash__(self):
        return hash((self.numero_questao, self.valor_questao, self.enunciado))

    def __eq__(self, outro):
        if isinstance(outro, Questao):
            dados_self = (self.numero_questao, self.valor_questao, self.enunciado)
            dados_outro = (outro.numero_questao, outro.valor_questao, outro.enunciado)
            if (dados_self == dados_outro):
                return True
        
        return False

    def __ne__(self, outro):
        return not(self == outro)

    def cadastrarQuestaoEmBranco(self):
        try:
            self.create('tbl_prova', {'numero_questao':self.numero_questao})
            return self.CDG_OK
        except sqlite3.IntegrityError:
            return self.CDG_JA_EXISTE_NUMERO

    
    def obterValor(self):
        if (self.valor_questao):
            return self.valor_questao
        else:
            self.valor_questao = self.read('tbl_prova',
                                           ('valor_questao',),
                                           {'numero_questao': self.numero_questao})[0]['valor_questao']
            return self.valor_questao

    def editarValor(self, novo_valor_questao):
        deu_certo = self.update('tbl_prova',
            {'valor_questao': novo_valor_questao},
            {'numero_questao': self.numero_questao})

        if deu_certo:
            self.valor_questao = novo_valor_questao
            return True
        else:
            return False


    def obterEnunciado(self):
        if (self.enunciado):
            return self.enunciado
        else:
            self.enunciado = self.read('tbl_prova', ('enunciado'),{'numero_questao': self.numero_questao})['enunciado']
            return self.enunciado


    def editarEnunciado(self, novo_enunciado):        
        deu_certo = self.update('tbl_prova',
            {'enunciado':novo_enunciado},
            {'numero_questao': self.numero_questao})

        if deu_certo:
            self.enunciado = novo_enunciado
            return True
        else:
            return False

    def obterCriterio(self, id_criterio):
        if (id_criterio in self.criterios):
            return self.criterios[id_criterio]
        else:
            criterio = self.read('tbl_criterios', where={'id_criterio': id_criterio})[0]
            if criterio:
                self.criterios[id_criterio] = Criterio(questao=self,
                    id_criterio=id_criterio,
                    nome_criterio=criterio['nome_criterio'],
                    peso_criterio=criterio['peso_criterio'],
                    conexao=self.conexao,
                    cursor_conexao=self.cursor_conexao)
                return self.criterios[id_criterio]
            else:
                return False

    def obterCriterios(self):
        criterios_obtidos =  self.read('tbl_criterios', ('*',), {'id_questao': self.numero_questao}, order_by=('nome_criterio',))
        criterios_ = {}
        for criterio in criterios_obtidos:
            criterios_[criterio['id_criterio']] = Criterio(self,
                                                        id_criterio=criterio['id_criterio'],
                                                        nome_criterio=criterio['nome_criterio'],
                                                        peso_criterio=criterio['peso_criterio'],
                                                        conexao=self.conexao,
                                                        cursor_conexao=self.cursor_conexao)
        return criterios_

    def cadastrarCriterio(self):
        criterio_criado = Criterio(self, conexao=self.conexao, cursor_conexao=self.cursor_conexao)
        id_criterio = criterio_criado.criarCriterioEmBranco()
        self.criterios[id_criterio] = criterio_criado
        return criterio_criado

    def obterNumeroQuestao(self):
        return self.numero_questao

    def editarNumeroQuestao(self, novo_numero_questao):
        deu_certo = self.update('tbl_prova',
            novo_valor={'numero_questao': novo_numero_questao},
            chaves={'numero_questao': self.numero_questao})

        if deu_certo:
            self.numero_questao = novo_numero_questao
            return True
        else:
            return False

class Criterio(BD_CRUD):
    def __init__(self, questao, id_criterio=None, nome_criterio=None, peso_criterio=None,
                conexao=False, cursor_conexao=False):
        self.questao = questao
        self.id_criterio = id_criterio
        self.nome_criterio = nome_criterio
        self.peso_criterio = peso_criterio

        BD_CRUD.__init__(self, conexao, cursor_conexao)


    def __hash__(self):
        return hash((self.questao, self.id_criterio, self.nome_criterio, self.peso_criterio))

    def __eq__(self, outro):
        if isinstance(outro, Criterio) and dados_self == dados_outro:
            dados_self = (self.questao, self.id_criterio, self.nome_criterio, self.peso_criterio)
            dados_outro = (outro.questao, outro.id_criterio, outro.nome_criterio, outro.peso_criterio)
            return True
        else:
            return False

    def __ne__(self, outro):
        return not(self == outro)

    def criarCriterioEmBranco(self):
        self.id_criterio = random.randrange(1, 10001)
        try:
            self.create('tbl_criterios', {'id_questao': self.questao.obterNumeroQuestao(), 'id_criterio': self.id_criterio})
        except sqlite3.IntegrityError:
            self.criarCriterioEmBranco()

        return self.id_criterio

    def obterQuestaoRelacionado(self):
        return self.questao

    def obterIdCriterio(self):
        return self.id_criterio

    def obterNomeCriterio(self):
        if (self.nome_criterio):
            return self.nome_criterio
        else:
            return self.read('tbl_criterios', ('nome_criterio',), {'id_criterio': self.id_criterio})[0]['nome_criterio']

    def editarNomeCriterio(self, novo_nome_criterio):
        deu_certo = self.update('tbl_criterios',
            {'nome_criterio': novo_nome_criterio},
            {'id_criterio':self.id_criterio})

        if deu_certo:
            self.nome_criterio = novo_nome_criterio
            return True
        else:
            return False

    def obterPesoCriterio(self):
        if (self.peso_criterio):
            return self.peso_criterio
        else:
            return self.read('tbl_criterios', ('peso_criterio'), {'id_criterio': self.id_criterio})

    def editarPesoCriterio(self, novo_peso_criterio):
        deu_certo = self.update('tbl_criterios',
            {'peso_criterio': novo_peso_criterio},
            {'id_criterio': self.id_criterio})

        if deu_certo:
            self.peso_criterio = novo_peso_criterio
            return True
        else:
            return False

class Aluno(BD_CRUD):
    '''
    Template self.respostas:
        self.respostas = {
            objetoQuestao1: {
                'codigo': 'codigo blah blah blah',
                criterioObjetoA: respostaObjeto1A,
                criterioObjetoB: respostaObjeto1B,
                criterioObjetoC: respostaObjeto1C
                   
            }
        }
    '''
    def __init__(self, nome, matricula, conexao=False, cursor_conexao=False):
        self.nome = nome
        self.matricula = matricula

        self.conexao = conexao
        self.cursor_conexao = cursor_conexao

        self.respostas = {}

        BD_CRUD.__init__(self, conexao, cursor_conexao)
        self.seCadastrar()

    
    def seCadastrar(self):
        self.id_aluno = random.randrange(1, 10001)
        try:
            self.create('tbl_alunos', {'id_aluno': self.id_aluno, 'nome': self.nome, 'matricula': self.matricula})
        except sqlite3.IntegrityError: # Caso já exista usuário com este Id, ele tenta se cadastrar novamente
            self.seCadastrar()

    def obterCodigo(self, questao):
        return self.respostas[questao]['codigo']

    def apagarResposta(self, questao, criterio=False):
        if (isinstance(questao, Questao) and isinstance(criterio, Criterio)):
            id_resposta = self.respostas[questao][criterio].obterIdResposta()
            self.delete('tbl_notas', {'id_resposta': id_resposta})

        if (isinstance(questao, int)):
            id_questao = questao
        elif (isinstance(questao, Questao)):
            id_questao = questao.obterNumeroQuestao()

        if (isinstance(criterio, int)):
            id_criterio = criterio
        elif (isinstance(criterio, Criterio)):
            id_criterio = criterio.obterIdCriterio()

        if (criterio):
            self.delete('tbl_notas', {'questao': id_questao})
        else:
            self.delete('tbl_notas', {'questao': id_questao, 'criterio': id_criterio})

    def obterIdAluno(self):
        return self.id_aluno

    def obterMatricula(self):
        if (self.matricula):
            return self.matricula
        else:
            resultado = self.read('tbl_alunos', ('matricula'), {'id_aluno': self.id_aluno})
            if (resultado):
                return resultado['matricula']
            else:
                return 'Não cadastrada'

    def editarMatricula(self, nova_matricula):
        deu_certo = self.update('tbl_alunos', {'matricula': nova_matricula}, {'id_aluno': self.id_aluno})

        if deu_certo:
            self.matricula = nova_matricula
            return True
        else:
            return False
        
    def obterNome(self):
        return self.nome

    def editarNome(self, novo_nome):
        deu_certo = self.update('tbl_alunos', {'nome': novo_nome}, {'id_aluno': self.id_aluno})

        if deu_certo:
            self.nome = novo_nome
            return True
        else:
            return False

    
    def obterRespostas(self):
        return self.respostas

    def obterResposta(self, questao, criterio=None):
        if criterio:
            return self.respostas[questao][criterio]
        else:
            return self.respostas[questao]

    def cadastrarResposta(self, criterio=False, questao=False, codigo=False):
        resp = Resposta(criterio, questao, self, conexao=self.conexao, cursor_conexao=self.cursor_conexao)
        resp.cadastrarRespostaEmBranco()

        if criterio:
            self.respostas[questao][criterio.obterIdCriterio()] = resp
        else:
            if (codigo):
                self.respostas[questao] = {'codigo': codigo}
            else:
                self.respostas[questao] = {}
        
        
        return resp

    def obterNotaAlunoDeQuestao(self, questao, criterio=False):
        if (criterio):
            try:
                return self.respostas[questao][criterio].obterNota()
            except KeyError: # Ainda não foi cadastrado uma resposta com tal criterio
                return 0

        else:
            total_criterio = 0
            nota_aluno_criterios = 0
            valor_questao = questao.ObterValorQuestao()
            for criteiro in self.respostas[questao]:
                if (criterio == 'codigo'):
                    pass

                total_criterio += criterio.obterPesoCriterio()
                nota_aluno_criterios += self.respostas[questao][criterio].obterNota() * valor_questao
            
            return nota_aluno_criterios / total_criterio


    def obterNotaAluno(self, questao=False, criterio=False):
        if questao:
            if criterio:
                return self.obterNotaAlunoDeQuestao(questao, criterio)
            else:
                return self.obterNotaAlunoDeQuestao(questao)
        else:
            total = 0.0
            for questao in self.respostas:
                total += obterNotaAlunoDeQuestao(questao)
            return total

class Resposta(BD_CRUD):
    def __init__(self, criterio=False, questao=-1, aluno=False, codigo='', valor=0, conexao=False, cursor_conexao=False):
        self.criterio = criterio
        self.questao = questao
        self.aluno = aluno
        self.codigo = codigo
        self.valor = valor

        #resultado

        BD_CRUD.__init__(self, conexao, cursor_conexao)

    def cadastrarRespostaEmBranco(self):
        self.id_resposta = random.randrange(1, 10001)
        try:
            if (self.criterio):
                self.create('tbl_notas', {'criterio': self.criterio.obterIdCriterio(),
                                              'questao': self.questao.obterNumeroQuestao(), 
                                              'aluno': self.aluno.obterIdAluno(),
                                              'id_resposta': self.id_resposta})
            else:
                self.create('tbl_notas', {'questao': self.questao.obterNumeroQuestao(), 
                                              'aluno': self.aluno.obterIdAluno(),
                                              'id_resposta': self.id_resposta})
        except sqlite3.IntegrityError:
            self.cadastrarRespostaEmBranco()
        
        return self.id_resposta

    def obterCriterioAssociado(self):
        return self.criterio

    def obterQuestaoAssociada(self):
        return self.questao

    def obterAlunoAssociado(self):
        return self.aluno

    def obterNota(self):
        if (self.nota):
            return self.nota
        else:
            return self.read('tbl_notas', ('valor'), resposta)

    def editarNota(self, nova_nota):
        deu_certo = self.update('tbl_notas',
            {'nota': nova_nota},
            {'criterio': self.criterio, 'questao': self.questao, 'aluno': self.aluno.obterIdAluno()})
        if deu_certo:
            self.nota = nova_nota
            return True
        else:
            return False

    def obterCodigo(self):
        if (self.codigo):
            return self.codigo
        else:
            return self.read(tabela='tbl_notas',
                             itens_para_buscar=('codigo'),
                             where={'criterio':self.criterio.obterIdCriterio(),
                                    'questao': self.questao.obterNumeroQuestao(),
                                    'aluno': self.aluno.obterIdAluno()})['codigo']

    def editarCodigo(self, novo_codigo):
        chaves_ = {'questao': self.questao.obterNumeroQuestao(),
                   'aluno': self.aluno.obterIdAluno()}

        if (self.criterio): chaves_.update({'criterio': self.criterio.obterIdCriterio()})

        deu_certo = self.update('tbl_notas',
                               novo_valor={'codigo': novo_codigo},
                               chaves=chaves_)

        if deu_certo:
            self.codigo = novo_codigo
            return True
        else:
            return False

class PastaProjetos(BD_CRUD):
    tem_permissao = False

    def __init__(self, caminho, prova=None):
        self.caminho = caminho
        self.prova = prova

        try:
            self.conexao = sqlite3.connect(caminho.strip() + "\\CatiaCorrige.bd" )            
            self.tem_permissao = True
        except:
            return
        
        self.conexao.row_factory = utils.dict_factory
        self.cursor_conexao = self.conexao.cursor()

        BD_CRUD.__init__(self, self.conexao, self.cursor_conexao)

        self.registrarTabelasSeNaoExistem()
        
        self.alunos = {}
        self.pastas_de_alunos = {}

    def alterarProva(self, prova):
        self.prova = prova

    def registrarTabelasSeNaoExistem(self):
        if not (self.check_table_existence('tbl_alunos')):
            self.create_table('tbl_alunos', [('id_aluno', 'INT PRIMARY KEY'),
                                             ('matricula', 'TINYTEXT'),
                                             ('nome', 'TEXT'),
                                             ('FOREIGN KEY (id_aluno)', 'REFERENCES tbl_notas(aluno)')])

        if not (self.check_table_existence('tbl_notas')):
            self.create_table('tbl_notas', [('id_resposta', 'INT PRIMARY KEY'),
                                             ('criterio', 'INT'),
                                             ('questao', 'INT'),
                                             ('aluno', 'INT'),
                                             ('valor', 'REAL'),
                                             ('codigo', 'TEXT'),
                                             ('FOREIGN KEY (criterio)', 'REFERENCES tbl_criterios(id_criterio)'),
                                             ('FOREIGN KEY (questao)', 'REFERENCES tbl_prova(numero_questao)'),
                                             ('FOREIGN KEY (aluno)', 'REFERENCES tbl_alunos(id_aluno)')])

        # if not (self.check_table_existence('tbl_prova')):
        #     self.create_table('tbl_prova', [('titulo_prova', 'VARCHAR(255)'),
        #                                      ('numero_questao', 'INT'),
        #                                      ('valor_questao', 'REAL'),
        #                                      ('enunciado', 'TEXT'),
        #                                      ('FOREIGN KEY (numero_questao)', 'REFERENCES tbl_criterios(id_questao)'),
        #                                      ('FOREIGN KEY (numero_questao)', 'REFERENCES tbl_notas(questao)')])

        if not (self.check_table_existence('tbl_criterios')):
            self.create_table('tbl_criterios', [('id_questao', 'INT'),
                                             ('id_criterio', 'INT PRIMARY KEY'),
                                             ('nome_criterio', 'VARCHAR(255)'),
                                             ('peso_criterio', 'INT(3)'),
                                             ('FOREIGN KEY (id_questao)', 'REFERENCES tbl_prova(numero_questao)'),
                                             ('FOREIGN KEY (id_criterio)', 'REFERENCES tbl_notas(criterio)')])

    def obterConexao(self):
        return self.conexao

    def obterCursor(self):
        return self.cursor_conexao

    def processarPasta(self):
        for item in pathlib.Path(self.caminho).iterdir():
            if item.is_dir():
                deu_match = re.match(r'([\w]+)_(\w+)$', item.parts[-1])
                if (deu_match):
                    nome_aluno, n_matricula = deu_match.groups()
                    nome_aluno = re.sub(r"([A-Z])", r" \1", nome_aluno).strip()

                    aluno = Aluno(nome_aluno, n_matricula, conexao=self.conexao, cursor_conexao=self.cursor_conexao)
                    self.alunos[nome_aluno] = aluno
                    self.pastas_de_alunos[nome_aluno] = {}

                for item_ in item.iterdir():
                    deu_match = re.match(r'\w*([0-9]+)', str(item_.parts[-1]))
                    if (deu_match):
                        numero_questao = deu_match.group(1)

                        questao = self.prova.obterQuestao(numero_questao)
                        
                        with open(item_, encoding='utf-8') as f:
                            if (str(item_).endswith('.exe')):
                                f.close()
                                continue

                            self.pastas_de_alunos[nome_aluno][numero_questao] = item_
                            codigo = f.read()
                            
                            resposta = aluno.cadastrarResposta(questao=questao, criterio=None, codigo=codigo)
                            resposta.editarCodigo(codigo)

    def obterAlunos(self):
        return self.alunos

    def obterPastaAluno(self, aluno, questao=False):
        if not questao:
            return self.pastas_de_alunos[aluno]
        else:
            return self.pastas_de_alunos[aluno][questao]

    def obterAluno(self, nome_aluno):
        return self.alunos[nome_aluno] if nome_aluno in self.alunos else None

    def listarProjetos(self):
        return list(self.alunos)
        '''
        prs = []
        for i in pathlib.Path(self.caminho).iterdir():
            if i.is_dir():
                prs.append(i.parts[-1])

        return prs
        '''

    def fecharConexao(self):
        self.conexao.close()
