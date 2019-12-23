import sqlite3
import os

class BD_CRUD:
    def __init__(self):
        pass

    def create(self, tabela, valores):
        pass

    def read(self):
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
        pass

    def obterValor(self):
        pass

    def editarValor(self):
        pass

    def obterEnunciado(self):
        pass

    def editarEnunciado(self):
        pass

    def obterCriterio(self):
        pass

    def obterCriterios(self):
        pass

    def cadastrarCriterio(self):
        pass

    def obterNumeroQuestao(self):
        pass

    def editarNumeroQuestao(self):
        pass


def Criterio(BD_CRUD):
    def __init__(self, questao):
        self.questao = questao

        self.id_criterio = self.create('tbl_criterios', {'id_questao': questao.obterNumeroQuestao()})

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
    def __init__(self, nome, matricula):
        BD_CRUD.__init__(self)
        self.nome = nome
        self.matricula = matricula

        self.id_aluno = self.create('tbl_alunos', {'nome':nome, 'matricula':matricula})


    def obterIdAluno(self):
        return self.id_aluno

    def obterMatricula(self):
        return self.matricula if self.matricula else 'Não cadastrada'

    def editarMatricula(self, nova_matricula):
        self.matricula = nova_matricula
        self.update('tbl_alunos', {'matricula': nova_matricula}, {'id_aluno': self.id_aluno})

    def obterNome(self):
        return self.nome

    def editarNome(self, novo_nome):
        self.nome = novo_nome
        self.update('tbl_alunos', {'nome': novo_nome}, {'id_aluno': self.id_aluno})

    def obterRespostas(self):
        return [Resposta(c) for c in self.readMany('tbl_notas', {'aluno':self.id_aluno})]

    def obterResposta(self, questao, criterio=None):
        if criterio:
            resp = self.read('tbl_notas', {'criterio': criterio, 'questao':questao, 'aluno': self.id_aluno})
        else:
            resp = self.read('tbl_notas', {'questao':questao, 'aluno': self.id_aluno})
        return Resposta(resp['criterio'], resp['questao'], self)

    def cadastrarResposta(self, criterio, questao):
        resp = Resposta(criterio, questao, self)
        return resp.cadastrarRespostaEmBranco()

    def __iter__(self): # Para percorrer as respostas
        pass

def Resposta(BD_CRUD):
    def __init__(self, criterio, questao, aluno):
        self.criterio = criterio
        self.questao = questao
        self.aluno = aluno

    def cadastrarRespostaEmBranco(self):
        self.id_reposta = self.create('tbl_notas', {'criterio': self.criterio,
                                  'questao': self.questao, 
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
        self.update('tbl_notas',
            {'nota': nova_nota},
            {'criterio': self.criterio, 'questao': self.questao, 'aluno': self.aluno.obterIdAluno()})

    def obterCodigo(self):
        return self.codigo

    def editarCodigo(self, novo_codigo):
        self.codigo = novo_codigo
        self.update('tbl_notas',
            {'codigo': novo_codigo},
            {'criterio': self.criterio, 'questao': self.questao, 'aluno': self.aluno.obterIdAluno()})
