import wx

class PainelGenericoQuestao(wx.Panel):
    def __init__(self, parent, descricao, valor, codigo, enunciado, *args, **kwargs):
        print(args, kwargs, sep="\n\n")
        wx.Panel.__init__(self, parent, *args, **kwargs)
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