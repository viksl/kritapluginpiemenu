from krita import *
from .ActionsList import ActionsList
from .Settings import Settings
from .MenuArea import MenuArea, EventController

class PieMenuExtension(Extension):
  def __init__(self,parent):
    super(PieMenuExtension, self).__init__(parent)

  def setup(self):
    pass

  def updateMenus(self):
    self.menuArea.deleteLater()
    self.menus = self.settings.menus
    self.menuArea = MenuArea(self.menus, self.qWin)
    self.menuArea.menus = self.menus

  def openPieMenu(self):
    if (not self.qWin.underMouse()):
      return

    self.menuArea.keyReleased = False
    self.menuArea.eventController = EventController(self.menuArea.menu, self.menuArea.menu.parent(), self.menuArea)

  def openSettings(self):
    self.settings.move(QCursor.pos())
    self.settings.show()

  def createActions(self, window):
    self.qWin = window.qwindow()
    
    self.actionsList = ActionsList().actionsList

    self.settings = Settings(self.actionsList, self.qWin)
    self.settings.menusChanged.connect(self.updateMenus)
    self.menus = self.settings.menus

    self.menuArea = MenuArea(self.menus, self.qWin)
    self.menuArea.menus = self.menus
    
    self.pieMenuAction = window.createAction("pieMenu", "Pie Menu")
    self.pieMenuAction.setAutoRepeat(False)

    self.pieMenuSettingsAction = window.createAction("pieMenuSettings", "Pie Menu Settings")
    self.pieMenuSettingsAction.setAutoRepeat(False)

    self.pieMenuAction.triggered.connect(self.openPieMenu)

    self.pieMenuSettingsAction.triggered.connect(self.openSettings)