from krita import *
from PyQt5 import *
from .ActionsList import ActionsList
from .Settings import Settings
from .MenuArea import MenuArea, EventController
from .GUISettings import GUISettings
from .Debug import Logger

class PieMenuExtension(Extension):
  def __init__(self,parent):
    super(PieMenuExtension, self).__init__(parent)
    self.l = Logger()

  def setup(self):
    pass

  def updateMenus(self, sectionsUpdate=False):
    if self.guiSettings.GUISettingsActive == True or sectionsUpdate == True:
      if self.menuArea.menu.initCursorPosition != None:
        if sectionsUpdate == True:
          self.menuArea.menus["menu"] = self.settings.GetMenus()["menu"]
          QTimer.singleShot(0, lambda: self.menuArea.menu.initNewMenuAt(self.menuArea.menus["menu"], self.menuArea.menu.initCursorPosition))

        self.OnNewOptionsReady()
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

    # l.print(self.menuArea.menu.parent() is QMainWindow)
    self.l.print(type(self.menuArea.parent()) is QMainWindow)
    # CHECK FOR ACTIVE WID MDIAREA TO COMPARE
    # qw = krita.instance().activeWindow().qwindow()
    # self.l.print( len( qw.findChildren(QMdiArea)[0].findChildren(QMdiSubWindow) ) > 0 )
    # for o in parent.findChildren(QMdiArea)[0].findChildren(QMdiSubWindow):
    #     self.l.print("o object name:")

    self.menuArea.menu.setParent(Krita.instance().activeWindow().qwindow())

    if type(self.menuArea.parent()) is QMainWindow:
      # parent = self.menuArea.parent()
      parent = Krita.instance().activeWindow().qwindow()
      QMArea = parent.findChildren(QMdiArea)[0]
      subWindows = QMArea.findChildren(QMdiSubWindow)
      # QMArea.addSubWindow(self.menuArea.menu)




      # if len( subWindows ) > 0:
      #     for o in subWindows[0].children():
      #       if type(o) is QVBoxLayout:
      #         o.addWidget(self.menuArea.menu)
      #       self.l.print("o object:")
      #       self.l.print(type(o))
      #       self.l.print("o object name:")
      #       self.l.print(o.objectName())

      #       self.l.print("Widget:")
      #       if hasattr(o, "addWidget"):
      #         self.l.print("addWidget")
      #       if hasattr(o, "setWidget"):
      #         self.l.print("setWidget")
      #         # if (o.objectName() == "view_0"):
      #             # o.setWidget(self.menuArea.menu)

    self.menuArea.menu.previousAction = None
    self.menuArea.menu.initNewMenuAt(self.menuArea.menus["menu"], QCursor.pos())
    self.menuArea.menu.show()

    if self.guiSettings.GUISettingsActive == False:
      self.menuArea.eventController = EventController(self.menuArea.menu, self.menuArea.menu.parent(), self.menuArea)
      QApplication.setOverrideCursor(Qt.ArrowCursor)

    if self.guiSettings.GUISettingsActive == True:
      QTimer.singleShot(0, self.menuArea.menu.OnGUISettingsUpdate)
    
  def openSettings(self):
    cursor = QCursor.pos()
    self.settings.move(cursor)
    self.settings.show()

    guiPosition = cursor
    guiPosition.setX(guiPosition.x() - self.guiSettings.width())

    self.guiSettings.move(guiPosition)
    self.guiSettings.show()

    self.guiSettings.GUISettingsActive = True

    self.updateMenus()
    QTimer.singleShot(0, self.OnOpenSettingsLoadSettings)

  def OnOpenSettingsLoadSettings(self):
    self.settings.loadSettings( self.settings.settingsFormLayout )

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
    self.settings.settingsChanged.connect(lambda: self.updateMenus( True ))
    self.menus = self.settings.menus

    self.guiSettings = GUISettings(self.actionsList, self.qWin)
    self.guiSettings.newOptionsReady.connect(self.OnNewOptionsReady)
    self.guiSettings.GUISettingsClosed.connect(self.OnGUISettingsClosed)
    
    self.actionsList.SetOptions(self.guiSettings.options)
    
    self.menuArea = MenuArea(self.menus, self.actionsList, self.guiSettings.options, self.qWin)

    self.pieMenuAction = window.createAction("kritapluginpiemenu", "Pie Menu", "tools/scripts")
    self.pieMenuAction.setAutoRepeat(False)

    self.pieMenuSettingsAction = window.createAction("pieMenuSettings", "Pie Menu Settings", "tools/scripts")
    self.pieMenuSettingsAction.setAutoRepeat(False)

    self.pieMenuAction.triggered.connect(lambda: QTimer.singleShot(0, self.openPieMenu))

    self.pieMenuSettingsAction.triggered.connect(self.openSettings)
