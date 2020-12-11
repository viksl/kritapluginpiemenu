from krita import *
from .Settings import Settings
from .MenuArea import MenuArea, EventController

class Dialog(QDialog):
  def __init__(self, text, parent=None):
      super(Dialog, self).__init__(parent)
      self.setLayout(QVBoxLayout())
      self.label = QLabel(str(text))
      self.layout().addWidget(self.label)
      self.resize(200, 50)
      self.exec_()

class PieMenuExtension(Extension):
  def __init__(self,parent):
    super(PieMenuExtension, self).__init__(parent)

  def setup(self):
    pass

  def updateMenus(self):
    self.menuArea.deleteLater()
    self.menus = self.settings.menus
    self.menuArea = MenuArea(self.menus, self.qWin)

  def openPieMenu(self):
    if (not self.qWin.underMouse()):
      return

    self.menuArea.keyReleased = False
    self.menuArea.menu.initNewMenuAt(self.menus["menu"], QCursor.pos())
    self.menuArea.eventController = EventController(self.menuArea.menu, self.menuArea.menu.parent(), self.menuArea)
    self.menuArea.menu.show()
    self.menuArea.menu.hide()
    self.menuArea.menu.show()

  def openSettings(self):
    self.settings.move(QCursor.pos())
    self.settings.show()

  def createActions(self, window):
    self.qWin = window.qwindow()
    
    self.actionsList = [
        {"name": "your action name", "actionID": "qaction id here"},
        {"name": "your action name2", "actionID": "qaction id here2"},
        {"name": "your action name3", "actionID": "qaction id here3"},
        {"name": "your action name4", "actionID": "qaction id here4"},
        {"name": "your action name5", "actionID": "qaction id here5"}
    ]

    self.settings = Settings(self.actionsList, self.qWin)
    self.menus = self.settings.menus

    self.menuArea = MenuArea(self.menus, self.qWin)
    self.settings.menusChanged.connect(self.updateMenus)

    self.pieMenuAction = window.createAction("pieMenu", "Pie Menu")
    self.pieMenuAction.setAutoRepeat(False)

    self.pieMenuSettingsAction = window.createAction("pieMenuSettings", "Pie Menu Settings")
    self.pieMenuSettingsAction.setAutoRepeat(False)

    self.pieMenuAction.triggered.connect(self.openPieMenu)

    self.pieMenuSettingsAction.triggered.connect(self.openSettings)