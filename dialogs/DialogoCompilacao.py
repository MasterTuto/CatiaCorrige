import wx

class DialogoCompilacao(wx.Dialog):
    def __init__(self, *args, **kwargs):
        wx.Dialog.__init__(self, *args, **kwargs)

        sizer = wx.BoxSizer(wx.VERTICAL)

        textoAcima = wx.StaticText(self, label="Compilando o código...")
        self.gauge = wx.Gauge(self, range=75)

        sizer.Add(textoAcima, 1, wx.EXPAND)
        sizer.Add(self.gauge, 1, wx.EXPAND)

        self.Bind(wx.EVT_TIMER, self.mudarValorGauge)
        self.timer = wx.Timer(self)
        self.timer.Start(100)

        self.SetSizer(sizer)
        sizer.Fit(self)
        self.Show(True)

    def mudarValorGauge(self, event):
        self.gauge.Pulse()