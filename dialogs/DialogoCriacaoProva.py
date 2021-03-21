import wx

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
        self.inputEnunciado = wx.TextCtrl(questaoStaticBox,
                              style=wx.TE_MULTILINE | wx.TE_PROCESS_TAB)
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