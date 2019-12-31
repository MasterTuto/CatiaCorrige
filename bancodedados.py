import sqlite3
import pathlib
import utils
import re



class BD_CRUD:
    def __init__(self, conexao, cursor_conexao):
        self.conexao = conexao
        self.cursor_conexao = cursor_conexao

    def query(self, query, dicionario_itens={}):
        if (dicionario_itens):
            query = self.cursor_conexao.execute(query. dicionario_itens)
            if (query):
                if (query.startswith('SELECT')):
                    return query.fetchall()
                # elif (query.startswith('INSERT')):
                #     return query.lastrowid
                else:  
                    return query
            else:
                return False
        else:
            query = self.cursor_conexao.execute(query)

    def check_table_existence(self):
        try:
            self.read('prova_questoes', '*', False)
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
            valores_colunas ++ "%s, " % valores[valor]

        nomes_colunas.rstrip(', ')
        valores_colunas.rstrip(', ')
        query = "INSERT INTO {0} ({1}) VALUES ({2})".format(tabela, nomes_colunas, valores_colunas)
        return self.query(query)

    def read(self, tabela, itens_para_buscar=("*"), where={}, order_by=(), group=()):

        itens_para_buscar = ', '.join(itens_para_buscar)

        texto_where = ' WHERE '
        for chave in where:
            texto_where += "%s=:%s, " % (chave, chave)
        texto_where.rstrip(', ')

        texto_group = ' GROUP BY ' + ', '.join(group)

        texto_order_by = ' ORDER BY ' + ", ".join(order_by)

        query = "SELECT {} FROM {};".format(itens_para_buscar, tabela)

        if where:
            query += texto_where

        if group:
            query += texto_group

        if  order_by:
            query += texto_order_by

        return self.query(query)

    def update(self, tabela, novo_valor, chaves={}):
        texto_novo_valor = ''
        for chave in novo_valor:
            texto_novo_valor += ' %s=:%s, ' % (chave, chave)
        texto_novo_valor.rstrip(', ')

        texto_chaves = ''
        for chave in chaves:
            texto_chaves += ' %s=:%s_chaves, ' % (chave, chave)
            chaves[chave + '_chaves'] = chaves[chave]
            del chaves[chave]

        texto_chaves.rstrip(', ')

        base_query = 'UPDATE {} SET {}c'.format(tabela, novo_valor)
        if chaves:
           base_query += texto_chaves
        
        return self.query(base_query, novo_valor.update(chaves))

    def delete(self, tabela, where):
        texto_where = ''
        for chave in where:
            texto_where += " {0}=:{0}, " % (chave)
        texto_where.rstrip(', ')

        query = "DELETE FROM tabela WHERE " + texto_where
        return self.query(query, where)

    def applyChanges(self):
        self.conexao.commit()

def Prova(BD_CRUD):
    CDG_OK = 1
    CDG_JA_EXISTE_NUMERO = 2
    def __init__(self):
        self.questoes = {}

    def criarQuestaoEmBranco(self, numero_questao):
        questao = Questao(numero_questao)
        codigo = questao.cadastrarQuestaoEmBranco()
        if codigo = self.CDG_OK:
            self.questoes[numero_questao] = questao
            return questao
        elif codigo = self.CDG_JA_EXISTE_NUMERO:
            return False

    def obterQuestao(self, numero_questao):
        if (numero_questao in self.questoes):
            return self.questoes[numero_questao]
        else:
            resultado = self.read('tbl_prova',  where={'numero_questao': numero_questao})
            if (resultado):
                questao = Questao(resultado['numero_questao'],
                               resultado['valor_questao'],
                               resultado['enunciado'])
                self.questao[numero_questao] = questao
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
        return self.check_table_existence(nome_tabela)

    def __iter__(self): # Para percorrer as questoes
        pass

def Questao(BD_CRUD):
    CDG_OK = 1
    CDG_JA_EXISTE_NUMERO = 2
    def __init__(self, numero_questao, valor_questao=0, enunciado=''):
        self.numero_questao = numero_questao
        self.valor_questao = valor_questao
        self.enunciado = enunciado
        self.criterios = {}

    def __hash__(self):
        return hash((self.numero_questao, self.valor_questao, self.enunciado))

    def __eq__(self, outro):
        if isinstance(outro, Questao):
            dados_self = (self.numero_questao, self.valor_questao, self.enunciado)
            dados_outro = (outro.numero_questao, outro.valor_questao, outro.enunciado)
            if (dados_self == dados_outro)
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
                                           ('valor_questao'),
                                           {'numero_questao': self.numero_questao})['valor_questao']
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
            criterio = self.read('tbl_criterios', where={'id_criterio': id_criterio})
            if criterio:
                self.criterios[id_criterio] = Criterio(questao=self,
                    id_criterio=id_criterio,
                    nome_criterio=criterio['nome_criterio'],
                    peso_criterio=criterio['peso_criterio'])
                return self.criterios[id_criterio]
            else:
                return False

    def obterCriterios(self):
        criterios_obtidos =  self.read('tbl_criterios', ('*'), False, sort_by=('nome_criterio'))
        criterios_ = {}
        for criterio in criterios_obtidos:
            criterios_[criterio['id_criterio']] = Criterio(self,
                                                        id_criterio=criterio['id_criterio'],
                                                        nome_criterio=criterio['nome_criterio'],
                                                        peso_criterio=criterio['peso_criterio'])
        return criterios_

    def cadastrarCriterio(self):
        criterio_criado = Criterio(self)
        criterio_criado.criarCriterioEmBranco()
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


def Criterio(BD_CRUD):
    def __init__(self, questao, id_criterio=None, nome_criterio=None, peso_criterio=None):
        self.questao = questao
        self.id_criterio = id_criterio
        self.nome_criterio = nome_criterio
        self.peso_criterio = peso_criterio


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
        if not self.id_criterio:
            self.id_criterio = self.create('tbl_criterios', {'id_questao': self.questao.obterNumeroQuestao()})
        else:
            return False

    def obterQuestaoRelacionado(self):
        return self.questao

    def obterIdCriterio(self):
        return self.id_criterio

    def obterNomeCriterio(self):
        if (self.nome_criterio):
            return self.nome_criterio
        else:
            return self.read('tbl_criterios', ('nome_criterio'), {'id_criterio': self.id_criterio})

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

def Aluno(BD_CRUD):
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
    def __init__(self, nome, matricula):
        BD_CRUD.__init__(self)
        self.nome = nome
        self.matricula = matricula

        self.id_aluno = random.randrange(1, 1000)
        self.create('tbl_alunos', {'id_aluno': id_aluno, 'nome':nome, 'matricula':matricula})
        self.respostas = {}

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

    def cadastrarResposta(self, criterio, questao):
        resp = Resposta(criterio, questao, self)

        self.respostas[questao][criterio] = resp
        resp.cadastrarRespostaEmBranco()
        
        return resp

    def obterNotaAlunoDeQuestao(self, questao, criterio=False):
        if (criterio):
            return self.respostas[questao][criterio].obterNota()
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
    def __init__(self, criterio, questao, aluno, codigo='', valor=0):
        self.criterio = criterio
        self.questao = questao
        self.aluno = aluno
        self.codigo = codigo
        self.valor = valor

    def cadastrarRespostaEmBranco(self):
        self.id_reposta = self.create('tbl_notas', {'criterio': self.criterio.obterIdCriterio(),
                                  'questao': self.questao.obterNumeroQuestao(), 
                                  'aluno': self.aluno.obterIdAluno()})
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
        deu_certo = self.update('tbl_notas',
                               novo_valor={'codigo': novo_codigo},
                               chaves= {'criterio': self.criterio.obterIdCriterio(),
                                        'questao': self.questao.obterNumeroQuestao(),
                                        'aluno': self.aluno.obterIdAluno()})

        if deu_certo:
            self.codigo = novo_codigo
            return True
        else:
            return False


class PastaProjetos(BD_CRUD):
    def __init__(self, caminho):
        self.caminho = caminho

        self.conexao = sqlite3.connect(caminho.strip() + "/CatiaCorrige.bd" )
        self.conexao.row_factory = utils.dict_factory
        self.cursor_conexao = self.conexao.cursor()

        BD_CRUD.__init__(self.conexao, self.cursor_conexao)

        if not (check_table_existence('tbl_alunos')):
            self.create_table('tbl_alunos', [('id_aluno', 'INT PRIMARY KEY'),
                                             ('matricula', 'TINYTEXT'),
                                             ('nome', 'TEXT'),
                                             ('FOREIGN KEY (id_aluno)', 'REFERENCES tbl_notas(aluno)')])

        self.alunos = {}

    def obterConexao(self):
        return self.conexao

    def obterCursor(self):
        return self.cursor_conexao

    def processarPasta(self):
        for item in pathlib.Path(caminho).iterdir():
            if item.is_dir():
                deu_match = re.match(r'([\w]+)_(\w+)', str(item))
                
                if (deu_match):
                    nome_aluno, n_matricula = deu_match.groups()

                    aluno = Aluno(nome_aluno, n_matricula)
                    self.alunos[aluno.obterIdAluno()] = aluno

    def obterAlunos(self):
        return self.alunos

    def listasProjetos(self):
        return [x for x in pathlib.Path(caminho).iterdir() if x.is_dir() and re.match(r'([\w]+)_(\w+)', str(x))]
