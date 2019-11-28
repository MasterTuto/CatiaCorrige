import wx
import wx.py as py

class treeCtrlAlunos():
	def __init__(self):
		pass

class painelDescricao(wx.Panel):
	def __init__(self, parent, **kwargs):
		wx.__init(self, parent, **kwargs)

		textoEscrito = wx.StaticText(self, label="Lorem ipsum doro si amet")
		textoEscrito
		self.Show(True)


class meuPrograma(wx.Frame):
	def __init__(self, parent, title, elementos=None):
		wx.Frame.__init__(self, parent=parent, title=title, size=(200,-1))
		self.CreateStatusBar()

		self.painel = wx.Panel(self)

		# ==== DEFINIÇÃO SIZERS ====
		sizerPrincipal = wx.BoxSizer(wx.VERTICAL)
		
		topSizer = wx.BoxSizer(wx.HORIZONTAL)
		
		middleSizer = wx.BoxSizer(wx.HORIZONTAL)
		leftMiddleSizer = wx.BoxSizer(wx.VERTICAL)
		middleMiddleSizer=  wx.BoxSizer(wx.VERTICAL)
		rightMiddleSizer = wx.BoxSizer(wx.VERTICAL)

		bottomSizer = wx.BoxSizer(wx.HORIZONTAL)
		# =========================

		elementosTopSizer = self.gerarElementoTopSizer()

		treeCtrlAlunos = self.criarTreeCtrl(elementos)

		string = ('QUESTÃO 5:\nLorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur dignissim quis nisl eget'
		'euismod. Prae sent id viverra tortor, sed consectetur urna.\n'
		'Proin finibus vulputate massa, sed ornare orci tempor ut.')
		
		staticEnunciado = wx.StaticText(self.painel, label=string)
		txtCtrlCodigo = wx.TextCtrl(self.painel, style=wx.TE_MULTILINE)
		codeControl = self.criarControles()

		
		avaliacao = self.gerarTelaDeAvaliacao()

		elementosBottomSizer = self.gerarElementoBottomSizer()

		topSizer.Add(elementosTopSizer, 1, wx.ALIGN_CENTER, 3)

		leftMiddleSizer.Add(treeCtrlAlunos, 1, wx.EXPAND, 3)

		middleMiddleSizer.Add(staticEnunciado, 1, wx.EXPAND | wx.ALL, 10)
		middleMiddleSizer.Add(txtCtrlCodigo, 6, wx.EXPAND | (wx.ALL ^ wx.BOTTOM), 5)
		middleMiddleSizer.Add(codeControl, 1, wx.EXPAND| (wx.ALL ^ wx.TOP) | wx.ALIGN_RIGHT, 10)

		rightMiddleSizer.Add(avaliacao, 1, wx.EXPAND| wx.ALL, 10)

		middleSizer.Add(leftMiddleSizer, 1, wx.EXPAND| wx.ALL, 10)
		middleSizer.Add(middleMiddleSizer, 3, wx.EXPAND| wx.ALL, 10)
		middleSizer.Add(rightMiddleSizer, 1, wx.EXPAND| wx.ALL, 10)

		bottomSizer.Add(elementosBottomSizer, 3)

		sizerPrincipal.Add(topSizer, 1, wx.ALIGN_CENTER, 3)
		sizerPrincipal.Add(middleSizer, 5, wx.EXPAND, 3)
		sizerPrincipal.Add(bottomSizer, 1,  wx.ALIGN_CENTER, 3)
		

		self.painel.SetSizer(sizerPrincipal)
		self.painel.SetAutoLayout(1)
		sizerPrincipal.Fit(self.painel)
		self.Show(True)
	
	def irParaPrimeiraQuestao(self, event):
		pass

	def irParaQuestaoAnterior(self, event):
		pass

	def irParaProximaQuestao(self, event):
		pass


	def irParaUltimaQuestao(self, event):
		pass

	def salvarCriterio(self, event):
		pass

	def adicionarNovoCriterio(self, event):
		pass

	def gerarElementoTopSizer(self):
		botaoPrimeiro = wx.Button(self.painel, label='Primeira')
		botaoAnterior = wx.Button(self.painel, label='Anterior')
		textoQuestaoAtual = wx.StaticText(self.painel, label='Questao 1')
		botaoProximo = wx.Button(self.painel, label="Proximo")
		botaoUltimo = wx.Button(self.painel, label='Ultima')

		self.Bind(wx.EVT_BUTTON, self.irParaPrimeiraQuestao, botaoPrimeiro)
		self.Bind(wx.EVT_BUTTON, self.irParaQuestaoAnterior, botaoAnterior)
		self.Bind(wx.EVT_BUTTON, self.irParaProximaQuestao, botaoProximo)
		self.Bind(wx.EVT_BUTTON, self.irParaUltimaQuestao, botaoUltimo)

		sizer = wx.BoxSizer(wx.HORIZONTAL)
		sizer.Add(botaoPrimeiro, 0, wx.ALIGN_CENTER | wx.ALL, 5)
		sizer.Add(botaoAnterior, 0, wx.ALIGN_CENTER | wx.ALL, 5)
		sizer.Add(textoQuestaoAtual, 0, wx.ALIGN_CENTER | wx.ALL, 5)
		sizer.Add(botaoProximo, 0, wx.ALIGN_CENTER | wx.ALL, 5)
		sizer.Add(botaoUltimo, 0, wx.ALIGN_CENTER | wx.ALL, 5)

		return sizer

	def gerarElementoBottomSizer(self):
		botaoPrimeiro = wx.Button(self.painel, label='Primeiro')
		botaoAnterior = wx.Button(self.painel, label='Anterior')
		textoQuestaoAtual = wx.StaticText(self.painel, label='Aluno 1')
		botaoProximo = wx.Button(self.painel, label="Proximo")
		botaoUltimo = wx.Button(self.painel, label='Ultimo')

		self.Bind(wx.EVT_BUTTON, self.irParaPrimeiraQuestao, botaoPrimeiro)
		self.Bind(wx.EVT_BUTTON, self.irParaQuestaoAnterior, botaoAnterior)
		self.Bind(wx.EVT_BUTTON, self.irParaProximaQuestao, botaoProximo)
		self.Bind(wx.EVT_BUTTON, self.irParaUltimaQuestao, botaoUltimo)

		sizer = wx.BoxSizer(wx.HORIZONTAL)
		sizer.Add(botaoPrimeiro, 0, wx.ALIGN_CENTER| wx.ALL, 5)
		sizer.Add(botaoAnterior, 0, wx.ALIGN_CENTER| wx.ALL, 5)
		sizer.Add(textoQuestaoAtual, 0, wx.ALIGN_CENTER| wx.ALL, 5)
		sizer.Add(botaoProximo, 0, wx.ALIGN_CENTER | wx.ALL, 5)
		sizer.Add(botaoUltimo, 0, wx.ALIGN_CENTER | wx.ALL, 5)

		return sizer

	def gerarTelaDeAvaliacao(self):
		sizer = wx.BoxSizer(wx.VERTICAL)
		linhaNome = wx.BoxSizer(wx.HORIZONTAL)
		linhaMatricula = wx.BoxSizer(wx.HORIZONTAL)
		
		avaliacaoSizer = wx.StaticBoxSizer(wx.VERTICAL, self.painel, "Avaliação")
		linhaCriterio = wx.BoxSizer(wx.HORIZONTAL)
		linhaValorCriterio = wx.BoxSizer(wx.HORIZONTAL)
		
		staticNome = wx.StaticText(self.painel, label="Nome:")
		nome = wx.StaticText(self.painel, label="Aluno 1")

		staticMatricula = wx.StaticText(self.painel, label="Matrícula:")
		matricula = wx.StaticText(self.painel, label="201911648")

		staticCriterio = wx.StaticText(self.painel, label="Criterio 1:")
		criterioTextCtrl = wx.TextCtrl(self.painel, value="Digite o nome do critério:")

		staticValor = wx.StaticText(self.painel, label="Nota:")
		valor = wx.SpinCtrlDouble(self.painel, style=wx.SP_WRAP | wx.SP_ARROW_KEYS, max=10.0, inc=0.1)
		salvarValorbtn = wx.Button(self.painel, label="S")

		adicionarNovoCriteriobtn = wx.Button(self.painel, label="[+]")

		linhaNome.Add(staticNome, 0, wx.ALL, 3)
		linhaNome.Add(nome, 0, wx.ALL, 3)

		linhaMatricula.Add(staticMatricula, 0, wx.ALL, 3)
		linhaMatricula.Add(matricula, 0, wx.ALL, 3)

		linhaCriterio.Add(staticCriterio, 0, wx.ALL, 3)
		linhaCriterio.Add(criterioTextCtrl, 0, wx.ALL, 3)

		linhaValorCriterio.Add(staticValor, 0, wx.ALL, 3)
		linhaValorCriterio.Add(valor, 0, wx.ALL, 3)
		linhaValorCriterio.Add(salvarValorbtn, 0, wx.ALL, 3)

		avaliacaoSizer.Add(linhaCriterio, 0, wx.ALL, 3)
		avaliacaoSizer.Add(linhaValorCriterio, 0, wx.ALL, 3)
		avaliacaoSizer.Add(adicionarNovoCriteriobtn, 0, wx.ALL, 3)

		sizer.Add(linhaNome, 0, wx.ALL, 3)
		sizer.Add(linhaMatricula, 0, wx.ALL, 3)
		sizer.Add(avaliacaoSizer, 0, wx.ALL, 3)


		self.Bind(wx.EVT_BUTTON, self.adicionarNovoCriterio, adicionarNovoCriteriobtn)
		self.Bind(wx.EVT_BUTTON, self.salvarCriterio, salvarValorbtn)


		return sizer
		

	def criarControles(self):
		sizer = wx.BoxSizer(wx.HORIZONTAL)
		sizer.AddSpacer(8)

		botaoCompilar = wx.Button(self.painel, label="Compilar")
		botaoPlay = wx.Button(self.painel, label="Rodar código")
		botaoPause = wx.Button(self.painel, label="Parar")

		sizer.Add(botaoCompilar, 0, wx.RIGHT | wx.ALIGN_RIGHT, 4)
		sizer.Add(botaoPlay, 0, wx.RIGHT | wx.ALIGN_RIGHT, 2)
		sizer.Add(botaoPause, 0, wx.LEFT | wx.ALIGN_RIGHT, 2)
		return sizer


	def criarTreeCtrl(self, elementos):
		treeCtrlAlunos = wx.TreeCtrl(self.painel)#, size=(200, 200))

		if not elementos: root = treeCtrlAlunos.AddRoot("Alunos")

		alunosEQuestoes = {
			'aluno1': ['questao1', 'questao2', 'questao3'],
			'aluno2': ['questao1', 'questao2', 'questao3'],
			'aluno3': ['questao1', 'questao2', 'questao3'],
			'aluno4': ['questao1', 'questao3', 'questao4'],
			'aluno5': ['questao1', 'questao3', 'questao5']
		}

		for aluno in alunosEQuestoes:
			alunoAtual = treeCtrlAlunos.AppendItem(root, aluno)
			for questao in alunosEQuestoes[aluno]:
				treeCtrlAlunos.AppendItem(alunoAtual, questao)

		return treeCtrlAlunos



prog = wx.App()
meuPrograma(None, "teste")
prog.MainLoop()