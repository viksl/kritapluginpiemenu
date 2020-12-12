from krita import *
from PyQt5 import *
from PyQt5.QtCore import pyqtSignal
import math

class Dialog(QDialog):
  def __init__(self, text, parent=None):
      super(Dialog, self).__init__(parent)
      self.setLayout(QVBoxLayout())
      self.label = QLabel(str(text))
      self.layout().addWidget(self.label)
      self.resize(200, 50)
      self.exec_()

class MenuArea(QObject):
    def __init__(self, menus, parent=None):
        super().__init__(parent)

        self.menus = menus
        
        self.menu = PieMenu(QCursor.pos(), self.menus["menu"], parent)
        self.menu.initNewMenuSignal.connect(self.initNewMenu)
        #self.eventController = EventController(self.menu, parent)

    def initNewMenu(self):
        index = self.menu.labels["activeLabel"]
        submenuRef = self.menus["menu"][index]["ref"]
        self.menu.initNewMenuAt(self.menus["submenus"][str(submenuRef)] , QCursor.pos() )

#Handles events mouse move + mouse press and sends it where needed (TODO: key release)
class EventController(QMdiArea):
    def __init__(self, eventObj=None, parent=None, controllerOwner=None):
        super().__init__(parent)

        self.installEventFilter(self)
        self.setMouseTracking(True)
        self.eventObj = eventObj
        self.controllerOwner = controllerOwner
        
    def eventFilter(self, source, event):
        if (event.type() == QEvent.KeyRelease
            and not event.isAutoRepeat()
            and Krita.instance().action("pieMenu").shortcut().matches(event.key()) > 0
            and not self.controllerOwner.keyReleased):

            if hasattr( self.controllerOwner, "eventController" ):
                self.controllerOwner.keyReleased = True

                self.eventObj.ResetGUI()
                self.eventObj.hide()
                
                self.removeEventFilter(self)
                self.controllerOwner.eventController.deleteLater()
                self.eventObj.eventHandler(event, self.controllerOwner.keyReleased)

        elif (event.type() == QtCore.QEvent.MouseMove
            and not self.controllerOwner.keyReleased):
            self.eventObj.eventHandler(event)

        elif (event.type() == QEvent.MouseButtonPress and 
            event.button() == QtCore.Qt.LeftButton):
            return True
            
        return super(EventController, self).eventFilter(source, event)

class PieMenu(QWidget):
    initNewMenuSignal = pyqtSignal()

    def __init__(self, cursorPosition, menuSections, parent=None):
        QWidget.__init__(self, parent)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setStyleSheet("background: transparent;")
        self.setWindowTitle("Quick Access Pie Menu")        
        self.radius = 300
        self.width = int(self.radius * 2)
        self.height = int(self.radius * 2)
        self.halfWidth = int(self.width / 2)
        self.halfHeight = int(self.height / 2)
        self.wheelIconOuterRadius = 13 *2
        self.wheelIconInnerRadius = 5 *2
        self.wheelColor = QColor(47, 47, 47, 200)
        self.lineColor = QColor(255, 255, 255, 30)
        self.wheelIconLineThickness = 1
        
        self.labelRadius = self.wheelIconInnerRadius + 180

        self.baseVector = [1, 0]

        self.labelPaintPoint = False
        self.distancePassed = False
        self.labelBaseColor = "rgba(47, 47, 47, 200)"
        self.labelActiveColor = "rgba(30, 30, 30, 250)"
        self.labelHighlightColor = "green"
        self.labelStyleBase = "background-color:" + self.labelBaseColor + "; color: white;"
        self.labelStyleActive = "background-color:" + self.labelActiveColor + "; color: white;"
        self.clearPainter = False
        
        self.previousAction = None
        #self.initNewMenuAt( menuSections, cursorPosition )

    def initNewMenuAt(self, menuSections, cursorPosition):
        self.clearPainter = False
        self.distance = None
        screen = QGuiApplication.screenAt(cursorPosition)
        self.setGeometry(screen.geometry())
        self.menuSections = menuSections
        self.cursorInitPosition = QPoint( cursorPosition.x() - screen.geometry().x(), cursorPosition.y() - screen.geometry().y() )
        self.totalSplitSections = len(self.menuSections)
        self.splitSectionAngle = 2 * math.pi / self.totalSplitSections
        self.splitSectionOffAngle = -(math.pi / 2) - self.splitSectionAngle/2 

        if hasattr(self, "labels") and len(self.labels["children"]) > 0:
            for label in self.labels["children"]:
                label.hide()
                label.deleteLater()

        self.labels = {
            "children": [None] * self.totalSplitSections,
            "activeLabel": None
        }

        for i in range(len(self.labels["children"])):
            p = self.circleCoor(self.cursorInitPosition.x(), self.cursorInitPosition.y(), self.labelRadius, i * self.splitSectionAngle + self.splitSectionAngle / 2)
    
            self.labels["children"][i] = QLabel(str(self.menuSections[i]["name"]), self)
            self.labels["children"][i].setFont(QFont('Times', 12))
            self.labels["children"][i].adjustSize()
            self.labels["children"][i].setGeometry(int(p["x"]), int(p["y"]), 170, 60)
            self.labels["children"][i].move(int(self.labels["children"][i].x() - self.labels["children"][i].width() / 2), int(self.labels["children"][i].y() - self.labels["children"][i].height()/ 2))
            self.labels["children"][i].setStyleSheet(self.labelStyleBase)
            self.labels["children"][i].setAlignment(QtCore.Qt.AlignCenter) 
            self.labels["children"][i].setWordWrap(True)
            self.labels["children"][i].show()
        
        self.update()

    def ResetGUI( self ):
        self.clearPainter = True

        if hasattr(self, "labels") and len(self.labels["children"]) > 0:
            for label in self.labels["children"]:
                label.hide()
                label.deleteLater()
            self.labels["children"] = []

        self.update()
        QApplication.processEvents()

    def getLabelPositionAt(self, index):
        return self.circleCoor(self.cursorInitPosition.x(), self.cursorInitPosition.y(), self.labelRadius, index * self.splitSectionAngle + self.splitSectionAngle / 2)

    def dotProduct(self, v1, v2):
        return v1[0] * v2[0] + v1[1] * v2[1]

    def determinant(self, v1, v2):
        return v1[0] * v2[1] - v1[1] * v2[0]

    def vectorAngle(self, v1, v2):
        angle = math.atan2(self.determinant(v1, v2), self.dotProduct(v1, v2))
        if angle < 0:
            angle += 2 * math.pi
        return  angle

    def twoPointDistance(self, v1, v2):
      return math.sqrt( math.pow(( v2.x() - v1.x() ), 2) + math.pow(( v2.y() - v1.y() ), 2)  )

    def circleCoor(self, x0, y0, r, angle):
        return {
            "x": x0 + r * math.cos(angle - self.splitSectionOffAngle),
            "y": y0 + r * math.sin(angle - self.splitSectionOffAngle)
        }

    def drawWheel(self):
        # Wheel ring
        path = QPainterPath()
        path.addEllipse(self.cursorInitPosition.x() - self.wheelIconOuterRadius, self.cursorInitPosition.y() - self.wheelIconOuterRadius, self.wheelIconOuterRadius * 2, self.wheelIconOuterRadius * 2)
        path.addEllipse(self.cursorInitPosition.x() - self.wheelIconInnerRadius, self.cursorInitPosition.y() - self.wheelIconInnerRadius, self.wheelIconInnerRadius * 2, self.wheelIconInnerRadius * 2)
        self.painter.fillPath(path, self.wheelColor)
        
        # Split lines
        self.painter.setPen(QPen(self.lineColor, self.wheelIconLineThickness, Qt.SolidLine))
        
        for i in range(self.totalSplitSections):
            p0 = self.circleCoor(self.cursorInitPosition.x(), self.cursorInitPosition.y(), self.wheelIconInnerRadius, i * self.splitSectionAngle)
            p1 = self.circleCoor(self.cursorInitPosition.x(), self.cursorInitPosition.y(), self.wheelIconOuterRadius, i * self.splitSectionAngle)            
            self.painter.drawLine(p0["x"], p0["y"], p1["x"], p1["y"])

    def paintEvent(self, event):
        self.painter = QPainter(self)
        self.painter.eraseRect(event.rect())
        self.painter.setRenderHints( QPainter.HighQualityAntialiasing )

        if not self.clearPainter:
            self.drawWheel()

        self.painter.end()

    def eventHandler(self, event, keyReleased=False):        
        if event.type() == QEvent.KeyRelease:
            if self.distance < self.wheelIconInnerRadius:
                return

            elif not (self.previousAction is None) and self.distance >= self.wheelIconInnerRadius and self.distance < self.wheelIconOuterRadius:
                action = Krita.instance().action( self.previousAction )

                if action != None:
                    action.trigger()

            elif not(self.labels["activeLabel"] is None):
                action = Krita.instance().action( self.menuSections[self.labels["activeLabel"]]["actionID"] )

                if action != None:
                    action.trigger()

        elif event.type() == QtCore.QEvent.MouseMove:
            if (not self.cursorInitPosition):
                self.cursorInitPosition = QCursor.pos()

            self.distance = self.twoPointDistance(self.cursorInitPosition, QCursor.pos())
            
            if self.distance >= self.wheelIconOuterRadius:
                screen = QGuiApplication.screenAt(QCursor.pos())
                v1 = [self.baseVector[0], self.baseVector[1]]
                v2 = [QCursor.pos().x() - screen.geometry().x() - self.cursorInitPosition.x(), QCursor.pos().y() - screen.geometry().y() - self.cursorInitPosition.y()]
                angle = self.vectorAngle(v1, v2)

                for i in range(0, self.totalSplitSections):
                    if ((angle + self.splitSectionOffAngle) % (2*math.pi) > i * self.splitSectionAngle and
                        (angle + self.splitSectionOffAngle) % (2*math.pi) <=  (i + 1) * self.splitSectionAngle):

                        if not (self.labels["activeLabel"] is None):
                            self.labels["children"][self.labels["activeLabel"]].setStyleSheet(self.labelStyleBase)
                        
                        self.labels["children"][i].setStyleSheet(self.labelStyleActive)
                        self.labels["activeLabel"] = i

                        # Display submenu
                        if not(self.labels["activeLabel"] is None) and self.menuSections[self.labels["activeLabel"]]["isSubmenu"]:
                            self.previousAction = self.menuSections[self.labels["activeLabel"]]["actionID"]
                            self.initNewMenuSignal.emit()
                        break
            else:
                for label in self.labels["children"]:
                    label.setStyleSheet(self.labelStyleBase)
