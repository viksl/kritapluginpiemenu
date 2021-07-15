from krita import *
from .ActionsList import ActionsList
from .Settings import Settings
from .MenuArea import MenuArea, EventController
from .GUISettings import GUISettings
from .Debug import Logger

class PieMenuExtension(Extension):
  def __init__(self,parent):
    super(PieMenuExtension, self).__init__(parent)

  def setup(self):
    pass

  def updateMenus(self):
    if self.guiSettings.GUISettingsActive == True:
      return

    self.menuArea.menu.deleteLater()
    self.menuArea.deleteLater()
    self.menus = self.settings.menus
    self.menuArea = MenuArea(self.menus, self.actionsList, self.guiSettings.options, self.qWin)
    self.menuArea.menus = self.menus

  def openPieMenu(self):
    if (
        not self.qWin.underMouse()
        or QGuiApplication.mouseButtons() != QtCore.Qt.NoButton
        or (self.menuArea.eventController != None and not self.menuArea.eventController.buttonReleased)
    ):
      return

    if self.menuArea.eventController != None:
      return

    self.menuArea.menu.previousAction = None
    self.menuArea.menu.initNewMenuAt(self.menuArea.menus["menu"], QCursor.pos())
    self.menuArea.menu.show()

    if self.guiSettings.GUISettingsActive == False:
      self.menuArea.eventController = EventController(self.menuArea.menu, self.menuArea.menu.parent(), self.menuArea)
      QApplication.setOverrideCursor(Qt.ArrowCursor)

    if self.guiSettings.GUISettingsActive == True:
      QTimer.singleShot(0, self.menuArea.menu.OnGUISettingsUpdate)
    
  def openSettings(self):
    self.settings.move(QCursor.pos())
    self.settings.show()
    self.guiSettings.move(QCursor.pos())
    self.guiSettings.show()
    self.guiSettings.GUISettingsActive = True
    self.updateMenus()

  def OnNewOptionsReady(self):
    QTimer.singleShot(0, self.menuArea.menu.OnGUISettingsUpdate)

  def OnGUISettingsClosed(self):
    self.guiSettings.GUISettingsActive = False
    self.updateMenus()

  def createActions(self, window):
    self.qWin = window.qwindow()

    self.actionsList = ActionsList(self.qWin)

    self.settings = Settings(self.actionsList, self.qWin)
    self.settings.menusChanged.connect(self.updateMenus)
    self.menus = self.settings.menus

    self.guiSettings = GUISettings(self.actionsList, self.qWin)
    self.guiSettings.newOptionsReady.connect(self.OnNewOptionsReady)
    self.guiSettings.GUISettingsClosed.connect(self.OnGUISettingsClosed)

    self.menuArea = MenuArea(self.menus, self.actionsList, self.guiSettings.options, self.qWin)

    self.pieMenuAction = window.createAction("kritapluginpiemenu", "Pie Menu", "tools/scripts")
    self.pieMenuAction.setAutoRepeat(False)

    self.pieMenuSettingsAction = window.createAction("pieMenuSettings", "Pie Menu Settings", "tools/scripts")
    self.pieMenuSettingsAction.setAutoRepeat(False)

    self.pieMenuAction.triggered.connect(lambda: QTimer.singleShot(0, self.openPieMenu))

    self.pieMenuSettingsAction.triggered.connect(self.openSettings)
