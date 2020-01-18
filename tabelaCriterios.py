import wx.grid as grid

class CustomGrid(grid.Grid):
	def __init__(self, parent, *args, **kwargs):
		grid.Grid.__init__(self, parent, *args, **kwargs

		self.CreateGrid(2, 1)