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
		wx.Frame.__init__(self, parent=parent, title=title, style=wx.DEFAULT_FRAME_STYLE ^ wx.MAXIMIZE)

		# ==== DEFINIÇÃO SIZERS ====
		sizerPrincipal = wx.BoxSizer(wx.HORIZONTAL)
		leftMiddleSizer = wx.BoxSizer(wx.VERTICAL)
		middleMiddleSizer=  wx.BoxSizer(wx.VERTICAL)
		rightMiddleSizer = wx.BoxSizer(wx.VERTICAL)
		# =========================

		treeCtrlAlunos = self.criarTreeCtrl(elementos)

		string = ('QUESTÃO 5:\nLorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur dignissim quis nisl eget'
		'euismod. Prae sent id viverra tortor, sed consectetur urna.\n'
		'Proin finibus vulputate massa, sed ornare orci tempor ut.')
		
		staticEnunciado = wx.StaticText(self, label=string)
		txtCtrlCodigo = wx.TextCtrl(self, style=wx.TE_MULTILINE)
		codeControl = self.criarControles()

		
		saidaCodigo = py.shell.Shell(self)
		avaliacao = wx.StaticText(self, label='teste')

		leftMiddleSizer.Add(treeCtrlAlunos, 1, wx.EXPAND)

		middleMiddleSizer.Add(staticEnunciado, 1, wx.EXPAND)
		middleMiddleSizer.Add(txtCtrlCodigo, 6, wx.EXPAND)
		middleMiddleSizer.Add(codeControl, 1, wx.EXPAND)

		rightMiddleSizer.Add(saidaCodigo, 2, wx.EXPAND)
		rightMiddleSizer.Add(avaliacao, 1, wx.EXPAND)

		sizerPrincipal.Add(leftMiddleSizer, 1, wx.EXPAND)
		sizerPrincipal.Add(middleMiddleSizer, 5, wx.EXPAND)
		sizerPrincipal.Add(rightMiddleSizer, 1, wx.EXPAND)
		

		self.SetSizer(sizerPrincipal)
		self.SetAutoLayout(1)
		sizerPrincipal.Fit(self)
		self.Show(True)
	
	def criarControles(self):
		sizer = wx.BoxSizer(wx.HORIZONTAL)
		sizer.AddSpacer(8)

		botaoPlay = wx.Button(self, label="Play")
		botaoPause = wx.Button(self, label="Pause")

		sizer.Add(botaoPlay, wx.EXPAND)
		sizer.Add(botaoPause, wx.EXPAND)
		return sizer

	def criarTreeCtrl(self, elementos):
		treeCtrlAlunos = wx.TreeCtrl(self)#, size=(200, 200))

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