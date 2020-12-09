from krita import *
from .MenuArea import MenuArea

class PieMenuExtension(Extension):
  def __init__(self,parent):
    super(PieMenuExtension, self).__init__(parent)
    self.menuArea = MenuArea(QCursor.pos(), window.qwindow())
  def setup(self):
    pass

  def createActions(self, window):
    self.PMAction = window.createAction("pieMenu", "Pie Menu")