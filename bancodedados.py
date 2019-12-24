import sqlite3
import os

class BD_CRUD:
    def __init__(self):
        pass

    def create(self, tabela, valores):
        pass

    def read(self, tabela, itens_para_buscar, chaves):
        pass

    def readMany(self):
        pass

    def update(self, tabela, novo_valor, chaves):
        pass

    def delete(self):
        pass

    def applyChanges(self):
        pass

def Prova(BD_CRUD):
    def __init__(self):
        pass

    def criarQuestaoEmBranco(self):
        pass

    def obterQuestao(self):
        pass

    def obterQuestoes(self):
        pass

    def __bool__(self): # Substitui "ja existe prova"
        if CONDICAO:
            return True
        else:
            return False

    def __iter__(self): # Para percorrer as questoes
        pass

def Questao(BD_CRUD):
    def __init__(self):

    def __hash__(self):
        pass

    def __eq__(self):
        pass

    def __ne__(self):
        pass

    def obterValor(self):
        return self.valor_questao

    def editarValor(self, novo_valor_questao):
        self.valor_questao = novo_valor_questao
        
        deu_certo = self.update('tbl_prova',
            {'valor_questao': novo_valor_questao},
            {'numero_questao': self.numero_questao})
        
        return True if deu_certo else False


    def obterEnunciado(self):
        return self.enunciado

    def editarEnunciado(self, novo_enunciado):
        self.enunciado = novo_enunciado
        
        deu_certo = self.update('tbl_prova',
            {'enunciado':novo_enunciado},
            {'numero_questao': self.numero_questao})
        
        return True if deu_certo else False

    def obterCriterio(self, id_criterio):
        criterio = self.read('tbl_criterios', '*', {'id_criterio': id_criterio})
        if criterio:
            return Criterio(questao=self,
                id_criterio=id_criterio,
                nome_criterio=criterio['nome_criterio'],
                peso_criterio=criterio['peso_criterio'])
        else:
            return False

    def obterCriterios(self):
        return self.read('tbl_criterios', '*', False)

    def cadastrarCriterio(self):
        criterio_criado = Criterio(self)
        criterio_criado = 
        return criterio_criado

    def obterNumeroQuestao(self):
        pass

    def editarNumeroQuestao(self):
        pass


def Criterio(BD_CRUD):
    def __init__(self, questao, id_criterio=None, nome_criterio=None, peso_criterio=None):
        self.questao = questao
        self.id_criterio = id_criterio
        self.nome_criterio = nome_criterio
        self.peso_criterio = peso_criterio


    def __hash__(self):
        return hash((self.questao, self.id_criterio, self.nome_criterio, self.peso_criterio))

    def __eq__(self, outro):
        dados_self = (self.questao, self.id_criterio, self.nome_criterio, self.peso_criterio)
        dados_outro = (outro.questao, outro.id_criterio, outro.nome_criterio, outro.peso_criterio)
        
        if isinstance(outro, Criterio) and dados_self == dados_outro:
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
        return self.nome_criterio

    def editarNomeCriterio(self, novo_nome_criterio):
        self.nome_criterio = novo_nome_criterio
        self.update('tbl_criterios',
            {'nome_criterio': novo_nome_criterio},
            {'id_criterio':self.id_criterio})

    def obterPesoCriterio(self):
        return self.peso_criterio

    def editarPesoCriterio(self, novo_peso_criterio):
        self.peso_criterio = novo_peso_criterio
        self.update('tbl_criterios',
            {'peso_criterio': novo_peso_criterio},
            {'id_criterio': self.id_criterio})

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

        self.id_aluno = self.create('tbl_alunos', {'nome':nome, 'matricula':matricula})
        self.respostas = {}

    def obterCodigo(self, questao):
        return self.respostas[questao]

    def obterIdAluno(self):
        return self.id_aluno

    def obterMatricula(self):
        return self.matricula if self.matricula else 'Não cadastrada'

    def editarMatricula(self, nova_matricula):
        self.matricula = nova_matricula
        deu_certo = self.update('tbl_alunos', {'matricula': nova_matricula}, {'id_aluno': self.id_aluno})
        
        return True if deu_certo else False

    def obterNome(self):
        return self.nome

    def editarNome(self, novo_nome):
        self.nome = novo_nome
        deu_certo = self.update('tbl_alunos', {'nome': novo_nome}, {'id_aluno': self.id_aluno})
        
        return True if deu_certo else False

    def obterRespostas(self):
        return self.respostas
        #return [Resposta(c['criterio'], c['questao'], self) for c in self.readMany('tbl_notas', {'aluno':self.id_aluno})]

    def obterResposta(self, questao, criterio=None):
        if criterio:
            return self.respostas[questao][criterio]
        else:
            return self.respostas[questao]
        # if criterio:
        #     resp = self.read('tbl_notas', {'criterio': criterio, 'questao':questao, 'aluno': self.id_aluno})
        # else:
        #     resp = self.read('tbl_notas', {'questao':questao, 'aluno': self.id_aluno})
        # return Resposta(resp['criterio'], resp['questao'], self)

    def cadastrarResposta(self, criterio, questao):
        resp = Resposta(criterio, questao, self)

        self.respostas[questao][criterio] = resp
        
        return resp.cadastrarRespostaEmBranco()

    def obterNotaAluno(self, questao=False, criterio=False):
        if questao:
            if criterio:
                pass
            else:
                pass
        else:
            pass

    def __iter__(self): # Para percorrer as respostas
        pass

def Resposta(BD_CRUD):
    def __init__(self, criterio, questao, aluno):
        self.criterio = criterio
        self.questao = questao
        self.aluno = aluno

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
        return self.nota

    def editarNota(self, nova_nota):
        self.nota = nova_nota
        deu_certo = self.update('tbl_notas',
            {'nota': nova_nota},
            {'criterio': self.criterio, 'questao': self.questao, 'aluno': self.aluno.obterIdAluno()})
        if deu_certo:
            return True
        else:
            return False

    def obterCodigo(self):
        return self.codigo

    def editarCodigo(self, novo_codigo):
        self.codigo = novo_codigo
        deu_certo = self.update('tbl_notas',
            {'codigo': novo_codigo},
            {'criterio': self.criterio, 'questao': self.questao, 'aluno': self.aluno.obterIdAluno()})

        return True if deu_certo else False


class PastaProjetos:
    def __init__(self):
        pass

    def obterAlunos(self):
        pass

    def listaProjetos(self):
        pass