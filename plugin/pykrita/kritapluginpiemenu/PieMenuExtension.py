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
    self.menuArea = MenuArea(self.menus, self.actionsList, self.qWin)
    self.menuArea.menus = self.menus

  def openPieMenu(self):
    if (
        not self.qWin.underMouse()
        or QGuiApplication.mouseButtons() != QtCore.Qt.NoButton
        or (self.menuArea.eventController != None and not self.menuArea.eventController.buttonReleased)
    ):
      return

    if self.menuArea.eventController != None:
      if self.menuArea.menu.resetCallback != None:
        self.menuArea.menu.InvokeAction(self.menuArea.menu.resetCallback, True)
        # print("press again invoke action")
      self.menuArea.eventController.deleteEventFilter()
      self.menuArea.eventController = None
      # print("press again delete event filter")
      print("openPieMenu delete")
      return
    # TODO: Init pie menu here to avoid dealing with some troublesome parts of eventFilter
    #       Then only mouseMove and mousePress (+ tablet events) will be needed
    #       Eventually maybe a reset for a keyRelease but for not only mouse as base
    self.menuArea.menu.previousAction = None
    self.menuArea.menu.initNewMenuAt(self.menuArea.menus["menu"], QCursor.pos())
    self.menuArea.menu.show()
    self.menuArea.eventController = EventController(self.menuArea.menu, self.menuArea.menu.parent(), self.menuArea)

  def openSettings(self):
    self.settings.move(QCursor.pos())
    self.settings.show()

  def createActions(self, window):
    self.qWin = window.qwindow()
    
    self.actionsList = ActionsList(self.qWin)

    self.settings = Settings(self.actionsList, self.qWin)
    self.settings.menusChanged.connect(self.updateMenus)
    self.menus = self.settings.menus

    self.menuArea = MenuArea(self.menus, self.actionsList, self.qWin)

    self.pieMenuAction = window.createAction("kritapluginpiemenu", "Pie Menu", "tools/scripts")
    self.pieMenuAction.setAutoRepeat(False)

    self.pieMenuSettingsAction = window.createAction("pieMenuSettings", "Pie Menu Settings", "tools/scripts")
    self.pieMenuSettingsAction.setAutoRepeat(False)

    # self.pieMenuAction.triggered.connect(self.openPieMenu)
    self.pieMenuAction.triggered.connect(lambda: QTimer.singleShot(0, self.openPieMenu))

    self.pieMenuSettingsAction.triggered.connect(self.openSettings)
