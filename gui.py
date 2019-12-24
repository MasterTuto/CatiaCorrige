import wx.py as py
import backend
import wx
import re
import os

class DialogoCriacaoProva(wx.Dialog):
	def __init__(self, parent, *args, **kwargs):
		wx.Dialog.__init__(self, parent=parent,
			style=wx.DEFAULT_DIALOG_STYLE | wx.CAPTION | wx.MINIMIZE_BOX | wx.RESIZE_BORDER, title="Configuração de prova",
			size=(500, 500),
			*args, **kwargs)

		self.painel = wx.Panel(self)
		sizerPrincipal = wx.BoxSizer(wx.VERTICAL)
		sizer = wx.BoxSizer(wx.HORIZONTAL)
		sizerBotoesPrincipais = wx.BoxSizer(wx.HORIZONTAL)

		leftSizer = wx.BoxSizer(wx.VERTICAL)
		sizerControles = wx.BoxSizer(wx.HORIZONTAL)

		topRightSizer_ = wx.StaticBoxSizer(wx.VERTICAL, self.painel, "Dados Prova")
		topRightSizer = wx.GridBagSizer(5, 5)
		questaoSizer = wx.StaticBoxSizer(wx.VERTICAL, self.painel, "Questão")
		questaoStaticBox = questaoSizer.GetStaticBox()
		valorSizer = wx.BoxSizer(wx.HORIZONTAL)
		criterioSizer = wx.GridBagSizer(5, 5)
		bottomSizer = wx.BoxSizer(wx.HORIZONTAL)
		rightSizer = wx.BoxSizer(wx.VERTICAL)

		self.treeCtrlProva = self.gerarTreeCtrlProva()
		controles = self.criarControles()

		provaEstatico = wx.StaticText(self.painel, label="Prova:")
		self.inputTituloProva = wx.TextCtrl(self.painel)
		totalProvaEstatico = wx.StaticText(self.painel, label="TOTAL: ")
		self.totalProva = wx.StaticText(self.painel, label="0.0")


		enunciadoEstatico = wx.StaticText(questaoStaticBox, label="Enunciado:")
		self.inputEnunciado = wx.TextCtrl(questaoStaticBox, style=wx.TE_MULTILINE | wx.TE_PROCESS_TAB)
		valorEstatico = wx.StaticText(questaoStaticBox, label='Valor:')
		self.inputValor = wx.SpinCtrl(questaoStaticBox, min=0, max=100)

		nomeCriterioEstatico = wx.StaticText(self.painel, label="Critério")
		nomeEstatico = wx.StaticText(self.painel, label="Nome:")
		self.inputCriterio = wx.TextCtrl(self.painel)
		pesoCriterioEstatico = wx.StaticText(self.painel, label="Peso:")
		self.inputPesoCriterio = wx.SpinCtrl(self.painel, min=0, max=100)
		
		self.botaoOk = wx.Button(self.painel, label="OK", id=wx.ID_OK, style=wx.BU_EXACTFIT)
		botaoCancelar = wx.Button(self.painel, label="Cancelar", id=wx.ID_CANCEL, style=wx.BU_EXACTFIT)
		
		sizerControles.Add(controles)
		leftSizer.Add(self.treeCtrlProva, 6, wx.ALL | wx.EXPAND ^ wx.BOTTOM, 10)
		leftSizer.Add(sizerControles, 1, wx.ALL | wx.EXPAND, 10)

		topRightSizer.Add(provaEstatico, wx.GBPosition(0,0))
		topRightSizer.Add(self.inputTituloProva, wx.GBPosition(0,1))
		topRightSizer.Add(totalProvaEstatico, wx.GBPosition(1,0))
		topRightSizer.Add(self.totalProva, wx.GBPosition(1,1))

		valorSizer.Add(valorEstatico, 1, wx.ALL | wx.EXPAND)
		valorSizer.Add(self.inputValor, 1, wx.ALL)
		
		questaoSizer.Add(enunciadoEstatico, 1, wx.ALL | wx.EXPAND)
		questaoSizer.Add(self.inputEnunciado, 8, wx.ALL | wx.EXPAND)
		questaoSizer.Add(valorSizer, 1, wx.ALL | wx.EXPAND)

		criterioSizer.Add(nomeCriterioEstatico, wx.GBPosition(0, 0))
		criterioSizer.Add(nomeEstatico, wx.GBPosition(1, 0))
		criterioSizer.Add(self.inputCriterio, wx.GBPosition(1, 1))
		criterioSizer.Add(pesoCriterioEstatico, wx.GBPosition(2, 0))
		criterioSizer.Add(self.inputPesoCriterio, wx.GBPosition(2, 1))

		bottomSizer.Add(questaoSizer, 5, wx.ALL | wx.EXPAND)
		bottomSizer.Add(wx.StaticLine(self.painel, style=wx.VERTICAL), 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
		bottomSizer.Add(criterioSizer, 0, wx.ALL | wx.EXPAND)

		rightSizer.Add(topRightSizer, 1, wx.ALL | wx.EXPAND, 10)
		rightSizer.Add(bottomSizer, 5, wx.ALL | wx.EXPAND, 10)

		sizer.Add(leftSizer, 1, wx.EXPAND | wx.ALL | wx.EXPAND)
		sizer.Add(rightSizer, 4, wx.EXPAND | wx.ALL | wx.EXPAND)

		sizerBotoesPrincipais.Add(self.botaoOk, 0, wx.ALIGN_CENTER | wx.RIGHT, 3)
		sizerBotoesPrincipais.Add(botaoCancelar, 0, wx.ALIGN_CENTER | wx.LEFT, 2)

		sizerPrincipal.Add(sizer, 6, wx.EXPAND)
		sizerPrincipal.Add(sizerBotoesPrincipais, 0,  wx.ALIGN_RIGHT | wx.ALL, 5)

		self.inputCriterio.Disable()
		self.inputPesoCriterio.Disable()
		self.inputEnunciado.Disable()
		self.inputValor.Disable()
		self.botaoOk.Disable()

		self.Bind(wx.EVT_TREE_SEL_CHANGED, self.quandoItemForFocado, self.treeCtrlProva)

		self.painel.SetSizer(sizerPrincipal)
		sizerPrincipal.Fit(self)
		self.Show(True)

	def quandoItemForFocado(self, event):
		selecionado = self.treeCtrlProva.GetSelection()
		pai = self.treeCtrlProva.GetItemParent(selecionado)
		if (pai == self.rootTreeCtrlProva):
			self.inputCriterio.Disable()
			self.inputPesoCriterio.Disable()

			self.inputEnunciado.Enable()
			self.inputValor.Enable()

		elif (selecionado != self.rootTreeCtrlProva):
			self.inputEnunciado.Disable()
			self.inputValor.Disable()

			self.inputCriterio.Enable()
			self.inputPesoCriterio.Enable()

	def mostrarTamanho(self, event):
		print(self.GetVirtualSize())

	def criarControles(self):
		sizer = wx.BoxSizer(wx.HORIZONTAL)

		addQuestao = wx.Button(self.painel, label="+Q", style=wx.BU_EXACTFIT)
		removeQuestao = wx.Button(self.painel, label="-Q", style=wx.BU_EXACTFIT)
		
		addCriteiro = wx.Button(self.painel, label="+C", style=wx.BU_EXACTFIT)
		remCriterio = wx.Button(self.painel, label="-C", style=wx.BU_EXACTFIT)

		addQuestao.SetToolTip(wx.ToolTip("Adiciona Questão"))
		removeQuestao.SetToolTip(wx.ToolTip("Remove Questão"))
		addCriteiro.SetToolTip(wx.ToolTip("Adiciona Criterio"))
		remCriterio.SetToolTip(wx.ToolTip("Remove Critério"))

		addQuestao.Bind(wx.EVT_BUTTON, self.adicionarQuestao)
		removeQuestao.Bind(wx.EVT_BUTTON, self.removerItem)
		addCriteiro.Bind(wx.EVT_BUTTON, self.adicionarCriterio)
		remCriterio.Bind(wx.EVT_BUTTON, self.removerItem)

		sizer.Add(addQuestao, 0, wx.EXPAND | wx.ALL | wx.EXPAND, 2)
		sizer.Add(removeQuestao, 0, wx.EXPAND | wx.ALL | wx.EXPAND, 2)
		sizer.Add(addCriteiro, 0, wx.EXPAND | wx.ALL | wx.EXPAND, 2)
		sizer.Add(remCriterio, 0, wx.EXPAND | wx.ALL | wx.EXPAND, 2)

		return sizer

	def adicionarCriterio(self, event):
		itemSelecionado = self.treeCtrlProva.GetSelection()
		itemAdicionado = None
		
		if itemSelecionado.IsOk() and itemSelecionado != self.rootTreeCtrlProva:
			pai = self.treeCtrlProva.GetItemParent(itemSelecionado)
			if pai == self.rootTreeCtrlProva:
				numeroDeCriterios = self.treeCtrlProva.GetChildrenCount(itemSelecionado)
				itemAdicionado = self.treeCtrlProva.AppendItem(itemSelecionado, "Criterio %s"%(numeroDeCriterios+1))

		return itemAdicionado

	def adicionarQuestao(self, event):
		itemSelecionado = self.treeCtrlProva.GetSelection()
		numeroDeQuestoes = self.treeCtrlProva.GetChildrenCount(self.rootTreeCtrlProva, recursively=False)
		itemAdicionado = self.treeCtrlProva.AppendItem(self.rootTreeCtrlProva, "Questão %s"% (numeroDeQuestoes+1))
		return itemAdicionado


	def removerItem(self, event):
		itemSelecionado = self.treeCtrlProva.GetSelection()

		if itemSelecionado.IsOk():
			if itemSelecionado == self.rootTreeCtrlProva:
				event.Skip()
				return

			dialogo = wx.MessageDialog(parent=self,
				message="Tem certeza de quer apagar?",
				style=wx.CENTRE | wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)

			respostaDialogo = dialogo.ShowModal()
			if respostaDialogo == wx.ID_YES:
				self.treeCtrlProva.Delete(itemSelecionado)


	def gerarTreeCtrlProva(self):
		treeCtrl = wx.TreeCtrl(self.painel)
		self.rootTreeCtrlProva = treeCtrl.AddRoot("Prova")
		return treeCtrl



class painelGenericoQuestao(wx.Panel):
	def __init__(self, parent, enunciado, valor, codigo, *args, **kwargs):
		wx.Panel.__init__(self, parent)

		self.mudarCor()
		sizer = wx.BoxSizer(wx.VERTICAL)

		staticEnunciado = wx.StaticText(self, label=enunciado)
		font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, faceName="Chiller")

		self.txtCtrlCodigo = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_PROCESS_TAB, value=codigo)

		sizer.Add(staticEnunciado, 1, wx.ALL | wx.EXPAND, 10)
		sizer.Add(self.txtCtrlCodigo, 7, wx.ALL | wx.EXPAND, 10)
		self.SetSizer(sizer)

	def mudarCor(self):
		self.SetBackgroundColour(wx.Colour(120, 120, 120))


class meuPrograma(wx.Frame):
	def __init__(self, parent, title, elementos=None):
		wx.Frame.__init__(self, parent=parent, title=title, size=(200,-1))
		self.CreateStatusBar()
		
		barraDeMenu = wx.MenuBar()

		self.preencherBarraDeMenus(barraDeMenu)

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
		
		self.notebookGerado = self.gerarNotebook()
		codeControl = self.criarControles()
		
		avaliacao = self.gerarTelaDeAvaliacao()

		elementosBottomSizer = self.gerarElementoBottomSizer()

		topSizer.Add(elementosTopSizer, 1, wx.ALIGN_CENTER, 5)

		leftMiddleSizer.Add(treeCtrlAlunos, 1, wx.EXPAND, 5)

		middleMiddleSizer.Add(self.notebookGerado, 6, wx.EXPAND | wx.ALL | wx.EXPAND, 10)
		middleMiddleSizer.Add(codeControl, 1, wx.EXPAND | wx.ALL | wx.EXPAND, 10)

		rightMiddleSizer.Add(avaliacao, 1, wx.EXPAND| wx.ALL | wx.EXPAND, 10)

		middleSizer.Add(leftMiddleSizer, 1, wx.EXPAND| wx.ALL | wx.EXPAND, 10)
		middleSizer.Add(middleMiddleSizer, 3, wx.EXPAND| wx.ALL | wx.EXPAND, 10)
		middleSizer.Add(rightMiddleSizer, 1, wx.EXPAND| wx.ALL | wx.EXPAND, 10)

		bottomSizer.Add(elementosBottomSizer, 5)

		sizerPrincipal.Add(topSizer, 1, wx.ALIGN_CENTER, 5)
		sizerPrincipal.Add(middleSizer, 5, wx.EXPAND, 5)
		sizerPrincipal.Add(bottomSizer, 1,  wx.ALIGN_CENTER, 5)
		

		self.SetMenuBar(barraDeMenu)
		self.painel.SetSizer(sizerPrincipal)
		self.painel.SetAutoLayout(1)
		sizerPrincipal.Fit(self.painel)
		sizerPrincipal.RecalcSizes()
		self.Show(True)

	def gerarNotebook(self):
		notebook = wx.Notebook(self.painel)
		notebook.DeleteAllPages()
		return notebook


	def preencherItemDeMenu(self, elementos):
		item = wx.Menu()
		for i in elementos:
			if i:
				item.Append( *i)
			else:
				item.AppendSeparator()
		return item

	def criarNovaProva(self, event):
		pass

	def salvarProva(self, event):
		pass

	def enviarParaSagres(self, event):
		pass

	def exportar(self, event):
		pass

	def limparNotas(self, event):
		pass

	def editarProva(self, event):
		pass

	def mostrarResumo(self, event):
		pass

	def configurarGcc(self, event):
		pass

	def configurarSagres(self, event):
		pass

	def popupSobre(self, event):
		pass
	
	
	def preencherBarraDeMenus(self, menu):
		funcoes = [self.criarNovaProva, self.salvarProva, self.abrirPastaDaProva, self.enviarParaSagres,
				   self.exportar, self.limparNotas, self.editarProva, self.mostrarResumo, self.configurarGcc,
				   self.configurarSagres, self.popupSobre]

		elementosArquivo = [(101, "Nova Prova\tCtrl+N", "Cria nova prova"),
							(102, "Salvar Prova\tCtrl+S", "Salva prova"),
							(103, "Abrir Pasta da Prova\tCtrl+O", "Abre prova"),
							False,
							(104, "Enviar notas para sagres...\tCtrl+G", "Enviar logo para o Sagres (necessária configuração"),
							(105, "Exportar...", "Exportar arquivo para excel, xml, html, json, sql ou csv.")]

		elementosEditar = [(106, "Limpar notas", "Apaga todas as notas da avaliação"),
							(107, "Editar Prova/Questões", "Edite as questões da prova"),
							(108, "Resumo", "Calcular média, mediana, nota dos alunos, maior e menor")]

		elementosOpcoes = [(109, "Configurar gcc/compilador", "Configurar qual compilador usar"),
							(110, "Configurações Sagres", "Configurar conta do Sagres")]
		
		elementosSobre = [(111, "Sobre", "Mostrar informações sobre o programa")]

		arquivo = self.preencherItemDeMenu(elementosArquivo)
		editar  = self.preencherItemDeMenu(elementosEditar)
		opcoes  = self.preencherItemDeMenu(elementosOpcoes)
		sobre   = self.preencherItemDeMenu(elementosSobre)
		menu.Append(arquivo, "Arquivo")
		menu.Append(editar, "Editar")
		menu.Append(opcoes, "Opções")
		menu.Append(sobre, "Sobre")

		for i in range(11):
			self.Bind(wx.EVT_MENU, funcoes[i], id=101+i)

	def carregarQuestoesDoAluno(self, idAluno):
		nomeAluno = self.treeCtrlAlunos.GetItemText(idAluno)
		respostas = self.projetos[nomeAluno].obterRespostas()
		for resposta in respostas:
			if not resposta.endswith(".bd"):
				numero = int(re.match(resposta, r".+([0-9]).+").group(1))
				questao = self.prova.obterQuestao(numero-1)

				painelGenerico = painelGenericoQuestao(
					parent=self.notebookGerado,
					descricao = questao.obterEnunciado(),
					valor = questao.obterValor(),
					codigo = self.projetos[nomeAluno].obterCaminho() + resposta
					)
				self.notebookGerado.AddPage(painelGenerico)

		self.notebookGerado.ChangeSelection(0)


	def abrirPastaDaProva(self, event):
		self.pastaProjeto = wx.DirSelector()
		self.projetos = backend.PastaProjetos(self.pastaProjeto)

		self.prova = backend.Prova(self.pastaProjeto)
		if not (self.prova.jaExisteProva()):
			wx.MessageBox("Não existe prova cadastrada, clique OK para criar",
				parent=self,
				style=wx.ICON_EXCLAMATION | wx.OK)

			with DialogoCriacaoProva(self) as dlg:
				retornoDlg = dlg.ShowModal()
				if retornoDlg == wx.ID_CANCEL:
					wx.MessageBox("Criação cancelada",
						parent=self,
						style=wx.ICON_INFORMATION | wx.OK)
					return False

		self.preencherTreeCtrl(self.projetos.obterAlunos())
		self.carregarQuestoesDoAluno(self.treeCtrlAlunos.GetFirstChild(self.rootTreeCtrl))

	def obterTextCtrl(self):
		paginaAtual = self.notebookGerado.GetCurrentPage()
		for child in paginaAtual.GetChildren():
			if isinstance(child, wx.TextCtrl):
				return child

	def irParaPrimeiraQuestao(self, event):
		self.notebookGerado.ChangeSelection(0)

		self.txtCtrlCodigoAtual = self.obterTextCtrl()

	def irParaQuestaoAnterior(self, event):
		paginaAtual = self.notebookGerado.GetSelection()
		if (paginaAtual > 0):
			self.notebookGerado.ChangeSelection(paginaAtual-1)

		self.txtCtrlCodigoAtual = self.obterTextCtrl()

	def irParaProximaQuestao(self, event):
		paginaAtual = self.notebookGerado.GetSelection()
		totalDePaginas = self.notebookGerado.GetPageCount()
		if (paginaAtual < totalDePaginas-1):
			self.notebookGerado.ChangeSelection(paginaAtual+1)

		self.txtCtrlCodigoAtual = self.obterTextCtrl()


	def irParaUltimaQuestao(self, event):
		totalDePaginas = self.notebookGerado.GetPageCount()
		self.notebookGerado.ChangeSelection(totalDePaginas)

		self.txtCtrlCodigoAtual = self.obterTextCtrl()

	def salvarCriterio(self, event):
		pass

	def salvarCriterios(self, event):
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
		sizer.Add(botaoPrimeiro, 0, wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 5)
		sizer.Add(botaoAnterior, 0, wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 5)
		sizer.Add(textoQuestaoAtual, 0, wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 5)
		sizer.Add(botaoProximo, 0, wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 5)
		sizer.Add(botaoUltimo, 0, wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 5)

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
		sizer.Add(botaoPrimeiro, 0, wx.ALIGN_CENTER| wx.ALL | wx.EXPAND, 5)
		sizer.Add(botaoAnterior, 0, wx.ALIGN_CENTER| wx.ALL | wx.EXPAND, 5)
		sizer.Add(textoQuestaoAtual, 0, wx.ALIGN_CENTER| wx.ALL | wx.EXPAND, 5)
		sizer.Add(botaoProximo, 0, wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 5)
		sizer.Add(botaoUltimo, 0, wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 5)

		return sizer

	def AoMudarValorAvaliacao(self, event):
		self.notasCriterios[self.valores.index(event.GetId())].SetLabel(str(event.GetInt()))


	def gerarTelaDeAvaliacao(self):
		sizer = wx.BoxSizer(wx.VERTICAL)
		linhaNome = wx.BoxSizer(wx.HORIZONTAL)
		linhaMatricula = wx.BoxSizer(wx.HORIZONTAL)
		
		avaliacaoSizer = wx.StaticBoxSizer(wx.VERTICAL, self.painel, "Avaliação")
		
		staticNome = wx.StaticText(self.painel, label="Nome:")
		nome = wx.StaticText(self.painel, label="Aluno 1")

		staticMatricula = wx.StaticText(self.painel, label="Matrícula:")
		matricula = wx.StaticText(self.painel, label="201911648")

		nomes = ['menu + laço','saldo', 'saque', 'depós', 'fim']
		self.notasCriterios = []
		self.valores = []
		for i in range(5):
			linhaCriterio = wx.BoxSizer(wx.HORIZONTAL)
			linhaValorCriterio = wx.BoxSizer(wx.HORIZONTAL)
			
			staticCriterio = wx.StaticText(self.painel, label="Criterio %s:" % (i+1))
			criterioTextCtrl = wx.TextCtrl(self.painel, value=nomes[i], size=(200, -1))
			criterioTextCtrl.Disable()

			staticValor = wx.StaticText(self.painel, label="Nota:")
			valor = wx.Slider(self.painel, style=wx.SL_AUTOTICKS, minValue=0, maxValue=10)
			self.valores.append(valor.GetId())
			salvarValorbtn = wx.Button(self.painel, label="S", style=wx.BU_EXACTFIT)

			texto = wx.StaticText(self.painel, label=str(valor.GetValue()))
			self.notasCriterios.append(texto)
			self.Bind(wx.EVT_SLIDER, self.AoMudarValorAvaliacao, id=valor.GetId())

			linhaCriterio.Add(staticCriterio, 0, wx.ALL | wx.EXPAND, 1)
			linhaCriterio.Add(criterioTextCtrl, 0, wx.ALL | wx.EXPAND, 1)

			linhaValorCriterio.Add(staticValor, 0, wx.ALL | wx.EXPAND, 1)
			linhaValorCriterio.Add(valor, 0, wx.ALL | wx.EXPAND, 1)
			linhaValorCriterio.Add(texto, 0, wx.ALL | wx.EXPAND, 1)
			linhaValorCriterio.Add(salvarValorbtn, 0, wx.ALL | wx.EXPAND, 1)

			avaliacaoSizer.Add(linhaCriterio, 0, wx.ALL | wx.EXPAND, 1)
			avaliacaoSizer.Add(linhaValorCriterio, 0, wx.ALL | wx.EXPAND, 1)

		salvarCriteriosbtn = wx.Button(self.painel, label="SALVAR")
		total = wx.StaticText(self.painel, label="TOTAL: 20")

		linhaNome.Add(staticNome, 0, wx.ALL | wx.EXPAND, 1)
		linhaNome.Add(nome, 0, wx.ALL | wx.EXPAND, 1)

		linhaMatricula.Add(staticMatricula, 0, wx.ALL | wx.EXPAND, 1)
		linhaMatricula.Add(matricula, 0, wx.ALL | wx.EXPAND, 1)

		avaliacaoSizer.Add(salvarCriteriosbtn, 0, wx.ALL | wx.EXPAND, 1)
		avaliacaoSizer.Add(total, 0, wx.ALL | wx.EXPAND, 1)

		sizer.Add(linhaNome, 0, wx.ALL | wx.EXPAND, 1)
		sizer.Add(linhaMatricula, 0, wx.ALL | wx.EXPAND, 1)
		sizer.Add(avaliacaoSizer, 0, wx.ALL | wx.EXPAND, 1)

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


	def preencherTreeCtrl(self, alunosEQuestoes=None):
		for aluno in alunosEQuestoes:
			alunoAtual = self.treeCtrlAlunos.AppendItem(self.rootTreeCtrl, aluno)

			for questao in alunosEQuestoes[aluno].obterRespostas():
				if not (questao.endswith('bd')):
					self.treeCtrlAlunos.AppendItem(alunoAtual, questao)

	
	def duploCliqueEmItem(self, event):
		item = event.GetItem()
		pai = self.treeCtrlAlunos.GetItemParent(item)
		if (pai != self.rootTreeCtrl):
			self.preencherTextCtrlParaAluno(item)
		
		elif (pai == self.rootTreeCtrl):
			self.carregarQuestoesDoAluno()

	def preencherTextCtrlParaAluno(self, item):
		nomePai = self.treeCtrlAlunos.GetItemText(pai)

		projetos_ = self.projetos.listarProjetos()

		nomeArquivo = projetos_[nomePai].obterCaminho() + "\\"+self.treeCtrlAlunos.GetItemText(item)

		matchNumero = re.match(r'([0-9])\.\w+$', nomeArquivo)
		if(matchNumero):
			numero = matchNumero.group(1)

		self.atualizarParaQuestao(nomeArquivo)


	def atualizarParaQuestao(self, nomeArquivo):
		self.txtCtrlCodigoAtual.LoadFile(nomeArquivo)

	def criarTreeCtrl(self, elementos=None):
		self.treeCtrlAlunos = wx.TreeCtrl(self.painel)
		self.rootTreeCtrl = self.treeCtrlAlunos.AddRoot("Alunos")

		self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.duploCliqueEmItem, self.treeCtrlAlunos)

		return self.treeCtrlAlunos

prog = wx.App()
meuPrograma(None, "teste")
prog.MainLoop()