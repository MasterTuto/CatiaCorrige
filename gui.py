from pathlib import WindowsPath, Path
import bancodedados
import wx.py as py
import subprocess
import threading
import tempfile
import config
import utils
import wx
import re
import os

import time

class DialogoCompilacao(wx.Dialog):
	def __init__(self, *args, **kwargs):
		wx.Dialog.__init__(self, *args, **kwargs)

		sizer = wx.BoxSizer(wx.VERTICAL)

		textoAcima = wx.StaticText(self, label="Compilando o código...")
		self.gauge = wx.Gauge(self, range=75)

		sizer.Add(textoAcima,1, wx.EXPAND)
		sizer.Add(self.gauge,1, wx.EXPAND)

		self.Bind(wx.EVT_TIMER, self.mudarValorGauge)
		self.timer = wx.Timer(self)
		self.timer.Start(100)

		self.SetSizer(sizer)
		sizer.Fit(self)
		self.Show(True)

	def mudarValorGauge(self, event):
		self.gauge.Pulse()


class DialogoCriacaoProva(wx.Dialog):
	def __init__(self, parent, prova, *args, **kwargs):
		wx.Dialog.__init__(self, parent=parent,
			style=wx.DEFAULT_DIALOG_STYLE | wx.CAPTION | wx.MINIMIZE_BOX | wx.RESIZE_BORDER, title="Configuração de prova",
			size=(500, 500),
			*args, **kwargs)

		self.prova = prova
		self.dadosTemporarios = {}

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
		self.Bind(wx.EVT_TEXT, self.aoMudarNomeCriterio, self.inputCriterio)
		self.Bind(wx.EVT_SPINCTRL, self.aoMudarPesoCriterio, self.inputPesoCriterio)
		self.Bind(wx.EVT_TEXT, self.aoMudarEnunciadoQuestao, self.inputEnunciado)
		self.Bind(wx.EVT_SPINCTRL, self.aoMudarValorQuestao, self.inputValor)

		self.painel.SetSizer(sizerPrincipal)
		sizerPrincipal.Fit(self)
		self.Show(True)

	def aoMudarNomeCriterio(self, event):
		criterio = self.treeCtrlProva.GetSelection()
		itemQuestao = self.treeCtrlProva.GetItemParent(criterio)
		numeroQuestao = int(self.treeCtrlProva.GetItemText( itemQuestao ).split()[-1])
		numeroDeCriterio = int(self.treeCtrlProva.GetItemText( criterio ).split('_')[-1])
		
		novoNomeCriteiro = self.inputCriterio.GetValue()

		self.dadosTemporarios[numeroQuestao][numeroDeCriterio-1].editarNomeCriterio(
																 novoNomeCriteiro + "_" + str(numeroDeCriterio))

		self.treeCtrlProva.SetItemText(criterio, novoNomeCriteiro + "_" + str(numeroDeCriterio))

	def aoMudarPesoCriterio(self, event):
		criterio = self.treeCtrlProva.GetSelection()
		itemQuestao = self.treeCtrlProva.GetItemParent(criterio)
		numeroQuestao = int(self.treeCtrlProva.GetItemText( itemQuestao ).split()[-1])
		numeroDeCriterio = int(self.treeCtrlProva.GetItemText( criterio ).split('_')[-1])
		
		novoPesoCriterio = self.inputPesoCriterio.GetValue()
		self.dadosTemporarios[numeroQuestao][numeroDeCriterio-1].editarPesoCriterio(novoPesoCriterio)

	def aoMudarEnunciadoQuestao(self, event):
		itemQuestao = self.treeCtrlProva.GetSelection()
		numeroQuestao = int(self.treeCtrlProva.GetItemText( itemQuestao ).split()[-1])
		
		novoEnunciado = self.inputEnunciado.GetValue()
		self.prova.obterQuestao(numeroQuestao).editarEnunciado(novoEnunciado)

	def aoMudarValorQuestao(self, event):
		itemQuestao = self.treeCtrlProva.GetSelection()
		numeroQuestao = int(self.treeCtrlProva.GetItemText( itemQuestao ).split()[-1])
		
		novoValorQuestao = self.inputValor.GetValue()
		self.prova.obterQuestao(numeroQuestao).editarPesoCriterio(novoValorQuestao)
	
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

	def ativarOkSePossivel(self):
		if self.treeCtrlProva.GetChildrenCount(self.rootTreeCtrlProva, recursively=False) == 0:
			self.botaoOk.Disable()
			return False
		
		filhoAtual = self.treeCtrlProva.GetFirstChild(self.rootTreeCtrlProva)
		while (filhoAtual):
			if not filhoAtual[0]: break
			if self.treeCtrlProva.GetChildrenCount(filhoAtual[0], recursively=False) == 0:
				self.botaoOk.Disable()
				return False
			filhoAtual = self.treeCtrlProva.GetNextChild(*filhoAtual)

		self.botaoOk.Enable()
		return True

	def adicionarCriterio(self, event):
		itemSelecionado = self.treeCtrlProva.GetSelection()
		itemAdicionado = None
		
		if itemSelecionado.IsOk() and itemSelecionado != self.rootTreeCtrlProva:
			pai = self.treeCtrlProva.GetItemParent(itemSelecionado)
			if pai == self.rootTreeCtrlProva:
				numeroDeCriterios = self.treeCtrlProva.GetChildrenCount(itemSelecionado)
				itemAdicionado = self.treeCtrlProva.AppendItem(itemSelecionado, "Criterio_%s"%(numeroDeCriterios+1))

				numeroQuestao = int(self.treeCtrlProva.GetItemText( itemSelecionado ).split()[-1])
				questao = self.prova.obterQuestao(numeroQuestao)
				criterio = questao.cadastrarCriterio()

				self.dadosTemporarios[numeroQuestao].append(criterio)

		self.ativarOkSePossivel()

		return itemAdicionado

	def adicionarQuestao(self, event):
		itemSelecionado = self.treeCtrlProva.GetSelection()
		numeroDeQuestoes = self.treeCtrlProva.GetChildrenCount(self.rootTreeCtrlProva, recursively=False)
		itemAdicionado = self.treeCtrlProva.AppendItem(self.rootTreeCtrlProva, "Questão %s"% (numeroDeQuestoes+1))

		questao = self.prova.criarQuestaoEmBranco(numeroDeQuestoes+1)
		self.dadosTemporarios[questao.obterNumeroQuestao()] = []

		self.ativarOkSePossivel()
		
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

		self.ativarOkSePossivel()


	def gerarTreeCtrlProva(self):
		treeCtrl = wx.TreeCtrl(self.painel)
		self.rootTreeCtrlProva = treeCtrl.AddRoot("Prova")
		return treeCtrl


class painelGenericoQuestao(wx.Panel):
	def __init__(self, parent, enunciado, valor, codigo, *args, **kwargs):
		wx.Panel.__init__(self, parent)
		self.foiEditado = False

		self.mudarCor()
		sizer = wx.BoxSizer(wx.VERTICAL)

		staticEnunciado = wx.StaticText(self, label=enunciado)
		font = wx.Font(wx.FontInfo(10).FaceName('Consolas'))

		self.txtCtrlCodigo = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_PROCESS_TAB | wx.TE_RICH)
		self.txtCtrlCodigo.SetDefaultStyle(wx.TextAttr(wx.Colour(0, 0, 0), font=font))
		self.txtCtrlCodigo.AppendText(codigo)
		#self.txtCtrlCodigo.SetBackgroundColour(wx.Colour(0, 0, 0))

		self.txtCtrlCodigo.Bind(wx.EVT_TEXT, self.setarComoEditado)

		sizer.Add(staticEnunciado, 1, wx.ALL | wx.EXPAND, 10)
		sizer.Add(self.txtCtrlCodigo, 7, wx.ALL | wx.EXPAND, 10)
		self.SetSizer(sizer)

	def setarComoEditado(self, event):
		self.foiEditado = True

	def mudarCor(self):
		self.SetBackgroundColour(wx.Colour(120, 120, 120))


class meuPrograma(wx.Frame):
	def __init__(self, parent, title, elementos=None):
		wx.Frame.__init__(self, parent=parent, title=title)
		self.CreateStatusBar()

		self.alunoAtual = ''
		self.projetos=False
		self.valores= []
		self.notasCriterios = []
		
		barraDeMenu = wx.MenuBar()

		self.preencherBarraDeMenus(barraDeMenu)

		self.painel = wx.Panel(self)

		# ==== DEFINIÇÃO SIZERS ====
		self.sizerPrincipal = wx.BoxSizer(wx.VERTICAL)
		
		topSizer = wx.BoxSizer(wx.HORIZONTAL)
		
		self.middleSizer = wx.BoxSizer(wx.HORIZONTAL)
		leftMiddleSizer = wx.BoxSizer(wx.VERTICAL)
		middleMiddleSizer=  wx.BoxSizer(wx.VERTICAL)
		self.rightMiddleSizer = wx.BoxSizer(wx.VERTICAL)

		bottomSizer = wx.BoxSizer(wx.HORIZONTAL)
		# =========================

		elementosTopSizer = self.gerarElementoTopSizer()

		listCtrlAlunos = self.criarListCtrlAlunos(elementos)
		
		self.notebookGerado = self.gerarNotebook()
		codeControl = self.criarControles()
		
		self.criteriosAtuais = self.gerarTelaDeAvaliacao()

		elementosBottomSizer = self.gerarElementoBottomSizer()

		topSizer.Add(elementosTopSizer, 1, wx.ALIGN_CENTER, 5)

		leftMiddleSizer.Add(listCtrlAlunos, 1, wx.EXPAND, 5)

		middleMiddleSizer.Add(self.notebookGerado, 6, wx.EXPAND | wx.ALL | wx.EXPAND, 5)
		middleMiddleSizer.Add(codeControl, 1, wx.EXPAND | wx.ALL | wx.EXPAND, 5)

		self.rightMiddleSizer.Add(self.criteriosAtuais, 1, wx.EXPAND| wx.ALL | wx.EXPAND, 5)

		self.middleSizer.Add(leftMiddleSizer, 1, wx.EXPAND| wx.ALL | wx.EXPAND, 5)
		self.middleSizer.Add(middleMiddleSizer, 3, wx.EXPAND| wx.ALL | wx.EXPAND, 5)
		self.middleSizer.Add(self.rightMiddleSizer, 1, wx.EXPAND| wx.ALL | wx.EXPAND, 5)

		bottomSizer.Add(elementosBottomSizer, 5)

		self.sizerPrincipal.Add(topSizer, 1, wx.ALIGN_CENTER, 5)
		self.sizerPrincipal.Add(self.middleSizer, 13, wx.EXPAND, 5)
		self.sizerPrincipal.Add(bottomSizer, 1,  wx.ALIGN_CENTER, 5)
		

		self.SetMenuBar(barraDeMenu)
		self.painel.SetSizer(self.sizerPrincipal)
		self.painel.SetAutoLayout(1)
		self.sizerPrincipal.Fit(self.painel)
		self.sizerPrincipal.RecalcSizes()
		self.Show(True)

	def gerarNotebook(self):
		notebook = wx.Notebook(self.painel)
		notebook.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.aoMudarPaginaNotebook)
		notebook.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, self.cancelarMudancaPagina)
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

	def carregarQuestoesDoAluno(self, nomeAluno):
		self.alunoAtual = nomeAluno
		respostas = self.projetos.obterAluno(nomeAluno).obterRespostas()
		self.notebookGerado.DeleteAllPages()
		for questao in respostas:
			numero = questao.obterNumeroQuestao()

			
			aluno = self.projetos.obterAluno(nomeAluno)
			respostas = aluno.obterResposta(questao)
			painelGenerico = painelGenericoQuestao(
				parent=self.notebookGerado,
				descricao = questao.obterEnunciado(),
				valor = questao.obterValor(),
				codigo = respostas['codigo'],
				enunciado=self.prova.obterQuestao(numero).obterEnunciado())
			self.notebookGerado.AddPage(painelGenerico, "Questão %s" % (questao.obterNumeroQuestao()))
		
		self.sizerPrincipal.Layout()
		self.rightMiddleSizer.Detach(self.criteriosAtuais)
		self.middleSizer.Detach(self.rightMiddleSizer)

		self.criteriosAtuais.Destroy()
		self.rightMiddleSizer.Destroy()

		self.rightMiddleSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.criteriosAtuais = self.gerarTelaDeAvaliacao()

		self.rightMiddleSizer.Add(self.criteriosAtuais, 1, wx.EXPAND)
		
		self.middleSizer.Add(self.rightMiddleSizer)
		self.sizerPrincipal.Layout()

		self.notebookGerado.SetSelection(0)


	def abrirPastaDaProva(self, event):
		self.pastaProjeto = wx.DirSelector()
		if (self.pastaProjeto):
			self.projetos = bancodedados.PastaProjetos(self.pastaProjeto)
			if not (self.projetos.tem_permissao):
				wx.MessageBox("Pasta não possui permissão! Escolha outra.",
							  parent=self,
							  style=wx.ICON_EXCLAMATION | wx.OK)
				event.Veto()
				return
			
			self.conexao = self.projetos.obterConexao()
			self.cursor_conexao = self.projetos.obterCursor()

		else:
			self.projetos = None
			event.Skip()
			return False

		self.prova = bancodedados.Prova(self.conexao, self.cursor_conexao)
		if not self.prova:
			self.prova.criarProva()
			wx.MessageBox("Não existe prova cadastrada, clique OK para criar",
				parent=self,
				style=wx.ICON_EXCLAMATION | wx.OK)

			with DialogoCriacaoProva(self,self.prova) as dlg:
				retornoDlg = dlg.ShowModal()
				
				if retornoDlg == wx.ID_CANCEL:
					wx.MessageBox("Criação cancelada",
						parent=self,
						style=wx.ICON_INFORMATION | wx.OK)

					self.projetos.fecharConexao()
					os.remove(self.pastaProjeto+'/CatiaCorrige.bd')
					return False

		self.projetos.alterarProva(self.prova)
		self.projetos.processarPasta()
		self.projetos.applyChanges()
		self.preencherListCtrl(self.projetos.listarProjetos())
		nomeAluno = self.listCtrlAlunos.GetItemText(self.listCtrlAlunos.GetItem(0).GetId()).split('_')[0]
		self.carregarQuestoesDoAluno(nomeAluno)
		self.listCtrlAlunos.Select(0)
		self.listCtrlAlunos.Focus(0)
		self.notebookGerado.SetSelection(1)
		self.notebookGerado.SetSelection(0)

	def obterTextCtrl(self, event): # Chamado pelo aoMudarPaginaNotebook, nao eh evento
		paginaAtual = self.notebookGerado.GetPage(event.GetSelection())
		return paginaAtual.txtCtrlCodigo

	def cancelarMudancaPagina(self, event=None):
		painelGenerico = self.notebookGerado.GetCurrentPage()

		if (painelGenerico.foiEditado and self.notebookGerado.GetSelection() != 0):
			dialogo = wx.MessageDialog(self,
							 message="Arquivo foi editado, deseja mudar mesmo assim?",
							 style=wx.YES_NO|wx.NO_DEFAULT|wx.ICON_QUESTION)

			respostaDialogo = dialogo.ShowModal()
			if (respostaDialogo == wx.ID_NO):
				event.Skip()
				return True
		return False

	def aoMudarPaginaNotebook(self, event):
		self.txtCtrlCodigoAtual = self.obterTextCtrl(event)

	def irParaPrimeiraQuestao(self, event):
		if self.cancelarMudancaPagina(): event.Skip(); return

		print(self.notebookGerado.GetCurrentPage())
		self.notebookGerado.SetSelection(0)
		print(self.notebookGerado.GetCurrentPage())

		self.textoQuestaoAtual.SetLabel(self.notebookGerado.GetPageText(0))

	def irParaQuestaoAnterior(self, event):
		if self.cancelarMudancaPagina(): event.Skip(); return

		paginaAtual = self.notebookGerado.GetSelection()
		if (paginaAtual > 0):
			self.notebookGerado.SetSelection(paginaAtual-1)
			self.textoQuestaoAtual.SetLabel(self.notebookGerado.GetPageText(paginaAtual-1))

	def irParaProximaQuestao(self, event):
		if self.cancelarMudancaPagina(): event.Skip(); return

		paginaAtual = self.notebookGerado.GetSelection()
		totalDePaginas = self.notebookGerado.GetPageCount()
		if (paginaAtual < totalDePaginas-1):
			self.notebookGerado.SetSelection(paginaAtual+1)
			self.textoQuestaoAtual.SetLabel(self.notebookGerado.GetPageText(paginaAtual+1))


	def irParaUltimaQuestao(self, event):
		if self.cancelarMudancaPagina(): event.Skip(); return

		totalDePaginas = self.notebookGerado.GetPageCount()
		self.notebookGerado.SetSelection(totalDePaginas-1)
		self.textoQuestaoAtual.SetLabel(self.notebookGerado.GetPageText(totalDePaginas))

	def salvarCriterio(self, event):
		pass

	def salvarCriterios(self, event):
		self.sizerAvaliacao.Add(wx.Button(self.painel, id=wx.ID_OK))

	def gerarElementoTopSizer(self):
		botaoPrimeiro = wx.Button(self.painel, label='Primeira')
		botaoAnterior = wx.Button(self.painel, label='Anterior')
		self.textoQuestaoAtual = wx.StaticText(self.painel, label='Questao 1')
		botaoProximo = wx.Button(self.painel, label="Proximo")
		botaoUltimo = wx.Button(self.painel, label='Ultima')

		self.Bind(wx.EVT_BUTTON, self.irParaPrimeiraQuestao, botaoPrimeiro)
		self.Bind(wx.EVT_BUTTON, self.irParaQuestaoAnterior, botaoAnterior)
		self.Bind(wx.EVT_BUTTON, self.irParaProximaQuestao, botaoProximo)
		self.Bind(wx.EVT_BUTTON, self.irParaUltimaQuestao, botaoUltimo)

		sizer = wx.BoxSizer(wx.HORIZONTAL)
		sizer.Add(botaoPrimeiro, 0, wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 2)
		sizer.Add(botaoAnterior, 0, wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 2)
		sizer.Add(self.textoQuestaoAtual, 0, wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 2)
		sizer.Add(botaoProximo, 0, wx.ALIGN_CENTER | wx.ALL | wx.EXPAND,2)
		sizer.Add(botaoUltimo, 0, wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 2)

		return sizer

	def gerarElementoBottomSizer(self):
		botaoPrimeiro = wx.Button(self.painel, label='Primeiro')
		botaoAnterior = wx.Button(self.painel, label='Anterior')
		self.textoAlunoAtual = wx.StaticText(self.painel, label='Aluno 1')
		botaoProximo = wx.Button(self.painel, label="Proximo")
		botaoUltimo = wx.Button(self.painel, label='Ultimo')

		self.Bind(wx.EVT_BUTTON, self.irParaPrimeiraQuestao, botaoPrimeiro)
		self.Bind(wx.EVT_BUTTON, self.irParaQuestaoAnterior, botaoAnterior)
		self.Bind(wx.EVT_BUTTON, self.irParaProximaQuestao, botaoProximo)
		self.Bind(wx.EVT_BUTTON, self.irParaUltimaQuestao, botaoUltimo)

		sizer = wx.BoxSizer(wx.HORIZONTAL)
		sizer.Add(botaoPrimeiro, 0, wx.ALIGN_CENTER| wx.ALL | wx.EXPAND, 5)
		sizer.Add(botaoAnterior, 0, wx.ALIGN_CENTER| wx.ALL | wx.EXPAND, 5)
		sizer.Add(self.textoAlunoAtual, 0, wx.ALIGN_CENTER| wx.ALL | wx.EXPAND, 5)
		sizer.Add(botaoProximo, 0, wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 5)
		sizer.Add(botaoUltimo, 0, wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 5)

		return sizer

	def AoMudarValorAvaliacao(self, event):
		self.notasCriterios[self.valores.index(event.GetId())].SetLabel(str(event.GetInt()))

	def obterNomeAluno(self):
		return self.listCtrlAlunos.GetItemText(self.listCtrlAlunos.GetFocusedItem())
	
	def preencherCriterios(self, parent):
		print("KKKKKKKK fui chamado de filho da puta kkk")
		avaliacaoSizer = wx.StaticBoxSizer(wx.VERTICAL, parent, "Avaliação")

		nomePagina = self.notebookGerado.GetPageText(self.notebookGerado.GetSelection())
		numeroQuestao = nomePagina.split()[-1]
		questaoObjeto = self.prova.obterQuestao(numeroQuestao)
		criterios = questaoObjeto.obterCriterios()
		
		itensCriterios = list(criterios.items())
		for idCriterio, criterio in itensCriterios:#enumerate(criterios):
			i = itensCriterios.index((idCriterio, criterio))
			notaAtual = self.projetos.obterAluno( self.obterNomeAluno() ).obterNotaAluno(questaoObjeto, criterio)
			nomeCriterio = criterio.obterNomeCriterio()

			linhaCriterio = wx.BoxSizer(wx.HORIZONTAL)
			linhaValorCriterio = wx.BoxSizer(wx.HORIZONTAL)
			
			staticCriterio = wx.StaticText(avaliacaoSizer.GetStaticBox(), label="Criterio %s:" % (i+1))
			criterioTextCtrl = wx.TextCtrl(avaliacaoSizer.GetStaticBox(), value=nomeCriterio, size=(200, -1))
			criterioTextCtrl.Disable()

			staticValor = wx.StaticText(avaliacaoSizer.GetStaticBox(), label="Nota:")
			valor = wx.Slider(avaliacaoSizer.GetStaticBox(), style=wx.SL_AUTOTICKS, minValue=0, maxValue=10)
			self.valores.append(valor.GetId())
			salvarValorbtn = wx.Button(avaliacaoSizer.GetStaticBox(), label="S", style=wx.BU_EXACTFIT)

			texto = wx.StaticText(avaliacaoSizer.GetStaticBox(), label=str(valor.GetValue()))
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
		return avaliacaoSizer


	def gerarTelaDeAvaliacao(self, doDuploClique=False):
		painelTemp = wx.Panel(self.painel, size=(300,-1))

		sizer = wx.BoxSizer(wx.VERTICAL)
		linhaNome = wx.BoxSizer(wx.HORIZONTAL)
		linhaMatricula = wx.BoxSizer(wx.HORIZONTAL)
		
		avaliacaoSizer = wx.StaticBoxSizer(wx.VERTICAL, painelTemp, "Avaliação")
		
		elementoFocado = self.listCtrlAlunos.GetFocusedItem()
		if (elementoFocado != -1):
			nomeAluno = self.listCtrlAlunos.GetItemText(elementoFocado)
		else:
			nomeAluno = '<vazio>'
		
		if (doDuploClique):
			alunoObjeto = self.projetos.obterAluno(nomeAluno)
			print(nomeAluno)
			matriculaAluno = alunoObjeto.obterMatricula()
		else:
			matriculaAluno = "<vazio>"
		
		staticNome = wx.StaticText(painelTemp, label="Nome:")
		font = wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD)
		staticNome.SetFont(font)
		self.nomeAluno = wx.StaticText(painelTemp, label=nomeAluno)

		staticMatricula = wx.StaticText(painelTemp, label="Matrícula:")
		staticMatricula.SetFont(font)
		self.matricula = wx.StaticText(painelTemp, label=matriculaAluno)

		if doDuploClique:
			avaliacaoSizer = self.preencherCriterios(painelTemp)
		else:
			avaliacaoSizer = wx.BoxSizer(wx.HORIZONTAL)

		salvarCriteriosbtn = wx.Button(painelTemp, label="SALVAR")
		self.notaTotal = wx.StaticText(painelTemp, label="TOTAL: 20")

		linhaNome.Add(staticNome, 0, wx.ALL | wx.EXPAND, 1)
		linhaNome.Add(self.nomeAluno, 0, wx.ALL | wx.EXPAND, 1)

		linhaMatricula.Add(staticMatricula, 0, wx.ALL | wx.EXPAND, 1)
		linhaMatricula.Add(self.matricula, 0, wx.ALL | wx.EXPAND, 1)

		avaliacaoSizer.Add(salvarCriteriosbtn, 1, wx.ALL | wx.EXPAND, 1)
		avaliacaoSizer.Add(self.notaTotal, 0, wx.ALL | wx.EXPAND, 1)

		sizer.Add(linhaNome, 0, wx.ALL | wx.EXPAND, 1)
		sizer.Add(linhaMatricula, 0, wx.ALL | wx.EXPAND, 1)
		sizer.Add(avaliacaoSizer, 0, wx.ALL | wx.EXPAND, 1)

		painelTemp.SetSizer(sizer)

		return painelTemp
		
	def criarControles(self):
		sizer = wx.BoxSizer(wx.HORIZONTAL)
		sizer.AddSpacer(8)

		self.botaoSalvar = wx.Button(self.painel, label="Salvar")
		self.botaoCompilar = wx.Button(self.painel, label="Compilar")
		self.botaoPlay = wx.Button(self.painel, label="Rodar código")
		self.botaoPause = wx.Button(self.painel, label="Parar")

		sizer.Add(self.botaoSalvar, 0, wx.RIGHT | wx.ALIGN_RIGHT, 2)
		sizer.Add(self.botaoCompilar, 0, wx.RIGHT | wx.LEFT | wx.ALIGN_RIGHT, 2)
		sizer.Add(self.botaoPlay, 0, wx.RIGHT | wx.LEFT | wx.ALIGN_RIGHT, 2)
		sizer.Add(self.botaoPause, 0, wx.LEFT | wx.ALIGN_RIGHT, 2)

		self.Bind(wx.EVT_BUTTON, self.salvarCodigo, self.botaoSalvar)
		self.Bind(wx.EVT_BUTTON, self.compilarCodigo, self.botaoCompilar)
		self.Bind(wx.EVT_BUTTON, self.darPlayNoCodigo, self.botaoPlay)
		self.Bind(wx.EVT_BUTTON, self.pausarCodigo, self.botaoPause)
		return sizer

	def salvarCodigo(self, event=None, nomeArquivo=False):
		if not (nomeArquivo):
			nomePagina = self.notebookGerado.GetPageText(self.notebookGerado.GetSelection())
			numeroQuestao = nomePagina.split()[-1]

			caminhoArquivo = self.projetos.obterPastaAluno(self.alunoAtual, numeroQuestao)
			nomeArquivo = str(caminhoArquivo)

		with open(nomeArquivo, 'w') as arquivoDoCodigo:
			conteudoTextCtrl = self.txtCtrlCodigoAtual.GetValue()
			arquivoDoCodigo.write(conteudoTextCtrl)

		self.foiEditado = False

	def atualizarCompilacao(self, widget, valor=5):
		if valor>100: widget.Destroy(); return
		widget.Update(valor)
		wx.CallLater(10, self.atualizarCompilacao, widget, valor+5)

	
	def compilarCodigo(self, event):

		def innerCompilar(windowCompilando):
			if (config.Configuracoes.caminhoCompilador == ':visualg:'):
				pastaTemp = tempfile.gettempdir()
			else:
				nomePagina = self.notebookGerado.GetPageText(self.notebookGerado.GetSelection())
				numeroQuestao = nomePagina.split()[-1]

				caminhoArquivo = self.projetos.obterPastaAluno(self.alunoAtual, numeroQuestao)
				nomeArquivo = str(caminhoArquivo)
				
				os.chdir(config.Configuracoes.caminhoCompilador.parent)
				print([config.Configuracoes.caminhoCompilador.parts[-1], nomeArquivo, '-o', str(nomeArquivo)+'.exe'])
				subprocess.call([config.Configuracoes.caminhoCompilador.parts[-1], nomeArquivo, '-o', str(nomeArquivo)+'.exe'])
				os.chdir(WindowsPath(__file__).parent)

			windowCompilando.Destroy()

		windowCompilando = DialogoCompilacao(self)
		#self.atualizarCompilacao(windowCompilando)
		#EVT_NOTEBOOK_PAGE_CHANGING
		compilacao = threading.Thread(target=innerCompilar, args=(windowCompilando,))
		compilacao.start()


	def darPlayNoCodigo(self, event):
		os.chdir(WindowsPath(__file__).parent)
		if (config.Configuracoes.caminhoCompilador == ':visualg:'):
			pastaTemp = tempfile.gettempdir()
		else:
			nomePagina = self.notebookGerado.GetPageText(self.notebookGerado.GetSelection())
			numeroQuestao = nomePagina.split()[-1]

			
			nomeArquivo = self.projetos.obterPastaAluno(self.alunoAtual, numeroQuestao)
			nomeArquivo_ = str(nomeArquivo)
		if (nomeArquivo_ in os.listdir(Path(self.pastaProjeto).parent)):
			os.remove(nomeArquivo+'.exe')
		
		subprocess.Popen(['start', 'python', 'executar_e_perguntar.py', nomeArquivo_+'.exe'], shell=True)

	def pausarCodigo(self, event):
		pass
	
	def preencherListCtrl(self, pastas=[]):
		for pasta in range(len(pastas)):
			self.listCtrlAlunos.InsertItem(pasta, pastas[pasta])

		self.listCtrlAlunos.Select(0)
	
	
	def mudarDadosDoAluno(self, nomeAluno):
		self.nomeAluno.SetLabel(nomeAluno)
		self.matricula.SetLabel(self.projetos.obterAluno(nomeAluno).obterMatricula())
	

	def duploCliqueEmItem(self, event):
		self.rightMiddleSizer.Detach(self.criteriosAtuais)
		self.criteriosAtuais.Destroy()

		self.middleSizer.Detach(self.rightMiddleSizer)
		self.rightMiddleSizer.Destroy()

		self.rightMiddleSizer = wx.BoxSizer(wx.VERTICAL)

		self.criteriosAtuais = self.gerarTelaDeAvaliacao(True)
		self.rightMiddleSizer.Add(self.criteriosAtuais, 1, wx.EXPAND)
		self.rightMiddleSizer.Layout()

		self.middleSizer.Add(self.rightMiddleSizer, 4, wx.EXPAND | wx.ALL, 10)
		self.middleSizer.Layout()
		
		self.Layout()
		self.Refresh()
		self.Update()
		
		if event: item = event.GetItem()
		else: item = self.listCtrlAlunos.GetItem(self.listCtrlAlunos.GetFocusedItem())
		nomeAluno = self.listCtrlAlunos.GetItemText(item.GetId()).split('_')[0]
		self.carregarQuestoesDoAluno(nomeAluno)
		self.mudarDadosDoAluno(nomeAluno)
		self.notebookGerado.SetSelection(0)


	def atualizarParaQuestao(self, nomeArquivo):
		self.txtCtrlCodigoAtual.LoadFile(nomeArquivo)

	def criarListCtrlAlunos(self, elementos=None):
		self.listCtrlAlunos = wx.ListCtrl(self.painel, style=wx.LC_REPORT)

		coluna = wx.ListItem()
		coluna.Text = "Nome da Pasta"
		coluna.Width = 200
		self.listCtrlAlunos.InsertColumn(0, coluna)

		self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.duploCliqueEmItem, self.listCtrlAlunos)

		return self.listCtrlAlunos

if __name__ == '__main__':
	prog = wx.App()
	meuPrograma(None, "teste")
	prog.MainLoop()