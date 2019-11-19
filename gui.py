import wx

class meuPrograma(wx.Frame):
	def __init__(self, parent, title):
		super().__init__(parent=parent, title=title, style=wx.DEFAULT_FRAME_STYLE | wx.MAXIMIZE)



prog = wx.App()
meuPrograma(None, "teste")
prog.MainLoop()