from krita import *
from MenuArea import MenuArea

class PieMenuExtension(Extension):
  def __init__(self,parent):
    super(PieMenuExtension, self).__init__(parent)

  def setup(self):
    pass

  def createActions(self, window):
    self.PMAction = window.createAction("pieMenu", "Pie Menu")
    self.menuArea = MenuArea(QCursor.pos(), window.qwindow())