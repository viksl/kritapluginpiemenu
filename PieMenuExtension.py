from krita import *
from .ActionsList import ActionsList
from .Settings import Settings
from .MenuArea import MenuArea, EventController

# TODO: if key release is before 

class Dialog(QDialog):
  def __init__(self, text, parent=None):
      super(Dialog, self).__init__(parent)
      self.setLayout(QVBoxLayout())
      self.label = QLabel(str(text))
      self.layout().addWidget(self.label)
      self.resize(200, 50)
      self.exec_()
      
class Win(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.width = 900
        self.height = 200
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.Window)
        self.setWindowTitle("Print")
        self.setGeometry(0, 0, self.width, self.height)
        self.label = QLabel("----", self)
        self.label.setFont(QFont('Times', 12))
        self.label.setStyleSheet("color: red")
        self.label.move(10, 10)

        self.label2 = QLabel("----", self)
        self.label2.setFont(QFont('Times', 12))
        self.label2.setStyleSheet("color: red")
        self.label2.move(10, 40)

        self.label3 = QLabel("----", self)
        self.label3.setFont(QFont('Times', 12))
        self.label3.setStyleSheet("color: red")
        self.label3.move(10, 70)

        self.label4 = QLabel("----", self)
        self.label4.setFont(QFont('Times', 12))
        self.label4.setStyleSheet("color: red")
        self.label4.move(10, 100)

        self.label5 = QLabel("----", self)
        self.label5.setFont(QFont('Times', 12))
        self.label5.setStyleSheet("color: red")
        self.label5.move(10, 130)
        
        self.show()

    def p(self, txt):
        self.label.resize(self.width, 20)
        self.label.setText( format(txt,".2f") )
        
    def p2(self, txt):
        self.label2.resize(self.width, 20)
        self.label2.setText( str( txt ) )
        
    def p3(self, txt):
        self.label3.resize(self.width, 20)
        self.label3.setText( str( txt ) )

    def p4(self, txt):
        self.label4.resize(self.width, 20)
        self.label4.setText( str( txt ) )

    def p5(self, txt):
        self.label5.resize(self.width, 20)
        self.label5.setText( str( txt ) )

class mdiAFilter(QMdiArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.win = Win()
        self.count = 0
    def eventFilter(self, obj, event):
        # if event.type() == QtCore.QEvent.MouseMove:
        if event.type() == QEvent.KeyRelease:
            self.count += 1
            self.win.p2("test " + str(self.count))
            
        return False
        
mdi = mdiAFilter()

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
    if (not self.qWin.underMouse()):
      return

    self.menuArea.keyReleased = False
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
    
    self.pieMenuAction = window.createAction("pieMenu", "Pie Menu", "tools/scripts")
    self.pieMenuAction.setAutoRepeat(False)

    self.pieMenuSettingsAction = window.createAction("pieMenuSettings", "Pie Menu Settings", "tools/scripts")
    self.pieMenuSettingsAction.setAutoRepeat(False)

    self.pieMenuAction.triggered.connect(self.openPieMenu)

    self.pieMenuSettingsAction.triggered.connect(self.openSettings)