from krita import *
from .Settings import Settings
from .MenuArea import MenuArea

class PieMenuExtension(Extension):
  def __init__(self,parent):
    super(PieMenuExtension, self).__init__(parent)

  def setup(self):
    pass

  def createActions(self, window):
    self.pieMenuAction = window.createAction("pieMenu", "Pie Menu")
    self.pieMenuSettingsAction = window.createAction("pieMenuSettings", "Pie Menu Settings")
    self.settings = Settings(window.qwindow())
    self.menuArea = MenuArea(QCursor.pos(), window.qwindow())