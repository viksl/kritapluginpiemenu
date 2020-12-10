from krita import *
from .Settings import Settings
from .MenuArea import MenuArea

class PieMenuExtension(Extension):
  def __init__(self,parent):
    super(PieMenuExtension, self).__init__(parent)
    self.settings = None
    self.menuArea = None
    self.menuArea = MenuArea(QCursor.pos(), Krita.instance().activeWindow().qwindow())

  def setup(self):
    pass

  def openPieMenu( self ):
    if (not self.qWin.underMouse()):
      return
    #self.menuArea.show()

  def openSettings( self ):
    self.settings = Settings(Krita.instance().activeWindow().qwindow())

  def createActions(self, window):
    self.qWin = window

    self.pieMenuAction = window.createAction("pieMenu", "Pie Menu")
    self.pieMenuSettingsAction = window.createAction("pieMenuSettings", "Pie Menu Settings")

    self.pieMenuAction.triggered.connect(self.openPieMenu)
    self.pieMenuAction.setAutoRepeat(False)

    self.pieMenuSettingsAction.triggered.connect(self.openSettings)
    self.pieMenuSettingsAction.setAutoRepeat(False)