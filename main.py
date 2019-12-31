import wx
import gui
import config
import sqlite3
import bancodedados


# TODO
# Lembrar de colocar isso:
# conexao.row_factory = dict_factory
# Quando declarar a variável de conexao.

programa = wx.App()
interface = gui.meuPrograma(None, "Cátia Corrige v1.0")
programe.MainLoop()

