from krita import *
from PyQt5 import *
from PyQt5.QtCore import pyqtSignal
import math

class MenuArea(QObject):
    def __init__(self, menus, actionsList, parent=None):
        super().__init__(parent)

        self.menus = menus
        # self.actionsList = actionsList

        self.keyReleased = False

        self.menu = PieMenu(actionsList, parent)
        self.menu.initNewMenuSignal.connect(self.initNewMenu)
        actionsList.hidePieMenuSignal.connect(self.hidePieMenu)

    def initNewMenu(self):
        index = self.menu.labels["activeLabel"]
        submenuRef = self.menus["menu"][index]["ref"]
        self.menu.initNewMenuAt(self.menus["submenus"][str(submenuRef)] , QCursor.pos() )

    def hidePieMenu(self):
        self.menu.ResetGUI()
        self.menu.hide()

#Handles events mouse move + mouse press and sends it where needed (TODO: key release)
class EventController(QMdiArea):
    def __init__(self, eventObj=None, parent=None, controllerOwner=None):
        super().__init__(parent)

        self.installEventFilter(self)
        self.setMouseTracking(True)
        self.eventObj = eventObj
        self.controllerOwner = controllerOwner
        self.mouseButtonPress = False

    def eventFilter(self, source, event):
        if (event.type() == QEvent.KeyRelease
            and not event.isAutoRepeat()
            and Krita.instance().action("pieMenu").shortcut().matches(event.key()) > 0
            and not self.controllerOwner.keyReleased):

            self.eventObj.eventHandler(event)
            self.deleteEventFilter(source, event)

        elif (event.type() == QEvent.MouseButtonPress
            and event.button() == QtCore.Qt.LeftButton
            and not self.mouseButtonPress):

            self.mouseButtonPress = True
            self.controllerOwner.menu.previousAction = None
            self.controllerOwner.menu.initNewMenuAt(self.controllerOwner.menus["menu"], QCursor.pos())
            self.controllerOwner.menu.show()
            
            return True

        elif event.type() == QEvent.MouseButtonRelease:
            self.mouseButtonPress = False
            self.deleteEventFilter(source, event)
            return True

        elif ( event.type() == QEvent.MouseMove
            and not self.controllerOwner.keyReleased
            and self.mouseButtonPress ):
            self.eventObj.eventHandler(event)

        elif (event.type() == QEvent.TabletMove
            or event.type() == QEvent.TabletPress
            or event.type() == QEvent.KeyPress
            or event.type() == QEvent.MouseButtonPress
            or event.type() == QEvent.MouseButtonRelease):
            
            return True

        return super(EventController, self).eventFilter(source, event)

    def deleteEventFilter(self, source, event):
        if hasattr( self.controllerOwner, "eventController" ):
            self.eventObj.ResetGUI()
            self.eventObj.hide()

            if event.type() != QEvent.MouseButtonRelease:
                self.controllerOwner.keyReleased = True
                self.removeEventFilter(self)
                self.controllerOwner.eventController.deleteLater()
            
            self.eventObj.eventHandler(event, self.controllerOwner.keyReleased)


class PieMenu(QWidget):
    initNewMenuSignal = pyqtSignal()

    def __init__(self, actionsList, parent=None):
        QWidget.__init__(self, parent)

        self.actionsList = actionsList

        self.setWindowFlags(self.windowFlags() | QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setStyleSheet("background: transparent;")
        self.setWindowTitle("Quick Access Pie Menu")        
        self.radius = 300
        self.width = int(self.radius * 2)
        self.height = int(self.radius * 2)
        self.halfWidth = int(self.width / 2)
        self.halfHeight = int(self.height / 2)
        self.wheelIconOuterRadius = 18 *2
        self.wheelIconInnerRadius = 13 *2
        self.wheelColor = QColor(47, 47, 47, 200)
        self.lineColor = QColor(255, 255, 255, 30)
        self.wheelIconLineThickness = 1
        
        self.labelRadius = self.wheelIconInnerRadius + 180

        self.baseVector = [1, 0]

        self.labelPaintPoint = False
        self.distancePassed = False
        self.labelBaseColor = "rgba(47, 47, 47, 200)"
        self.labelActiveColor = "rgba(30, 30, 30, 250)"
        self.labelStyleBase = "background-color:" + self.labelBaseColor + "; color: white;"
        self.labelStyleActive = "background-color:" + self.labelActiveColor + "; color: white;"
        self.clearPainter = False
        
        self.previousAction = None
        self.callback = None
        self.resetCallback = None

    def initNewMenuAt(self, menuSections, cursorPosition):
        self.clearPainter = False
        self.distance = None
        self.callback = None
        self.resetCallback = None
        screen = QGuiApplication.screenAt(cursorPosition)
        self.setGeometry(screen.geometry())
        self.menuSections = menuSections
        self.cursorInitPosition = self.getCurrentPosition( cursorPosition )
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

    def eventHandler(self, event, keyReleased=False):
        if event.type() == QEvent.KeyRelease:
            if self.resetCallback != None:
                #self.resetCallback()
                return

        elif event.type() == QEvent.MouseButtonRelease:
            if self.resetCallback != None:
                self.resetCallback()
                return
                
            if self.distance == None:
                return

            elif not (self.previousAction is None) and self.distance < self.wheelIconOuterRadius:
                action = Krita.instance().action( self.previousAction )

                if action != None:
                    if action.isCheckable():
                        action.toggle()
                    else:
                        action.trigger()

            elif not(self.labels["activeLabel"] is None):
                action = Krita.instance().action( self.menuSections[self.labels["activeLabel"]]["actionID"] )

                if action != None:
                    if action.isCheckable():
                        action.toggle()
                    else:
                        action.trigger()

        elif event.type() == QtCore.QEvent.MouseMove:
            if (not self.cursorInitPosition):
                self.cursorInitPosition = QCursor.pos()

            if self.callback != None:
                self.callback()
                return

            self.distance = self.twoPointDistance(self.cursorInitPosition, self.getCurrentPosition())

            if self.distance >= self.wheelIconOuterRadius:
                cursor = self.getCurrentPosition()

                v1 = [self.baseVector[0], self.baseVector[1]]
                v2 = [cursor.x() - self.cursorInitPosition.x(), cursor.y() - self.cursorInitPosition.y()]

                angle = self.vectorAngle(v1, v2)

                self.callback = None
                self.resetCallback = None

                for i in range(0, self.totalSplitSections):
                    if ((angle + self.splitSectionOffAngle) % (2*math.pi) > i * self.splitSectionAngle and
                        (angle + self.splitSectionOffAngle) % (2*math.pi) <=  (i + 1) * self.splitSectionAngle):

                        if not (self.labels["activeLabel"] is None):
                            self.labels["children"][self.labels["activeLabel"]].setStyleSheet(self.labelStyleBase)
                        
                        self.labels["children"][i].setStyleSheet(self.labelStyleActive)
                        self.labels["activeLabel"] = i

                        # Display submenu
                        if self.labels["activeLabel"] != None and self.menuSections[self.labels["activeLabel"]]["isSubmenu"] and self.menuSections[self.labels["activeLabel"]]["callback"] == None:
                            self.previousAction = self.menuSections[self.labels["activeLabel"]]["actionID"]
                            self.initNewMenuSignal.emit()
                        if not(self.menuSections[self.labels["activeLabel"]]["isSubmenu"]) and self.labels["activeLabel"] != None and self.menuSections[self.labels["activeLabel"]]["callback"] != None:
                            self.actionsList.Init()
                            self.callback = getattr(self.actionsList, self.menuSections[self.labels["activeLabel"]]["callback"] )
                        if not(self.menuSections[self.labels["activeLabel"]]["isSubmenu"]) and self.labels["activeLabel"] != None and self.menuSections[self.labels["activeLabel"]]["resetCallback"] != None:
                            self.resetCallback = getattr(self.actionsList, self.menuSections[self.labels["activeLabel"]]["resetCallback"] )

                        break
            else:
                for label in self.labels["children"]:
                    label.setStyleSheet(self.labelStyleBase)

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

    def getCurrentPosition(self, aPosition=None):
        position = QCursor.pos() if aPosition == None else aPosition
        screen = QGuiApplication.screenAt(position)

        return QPoint(position.x() - screen.geometry().x(), position.y() - screen.geometry().y())

class Dialog(QDialog):
  def __init__(self, text, parent=None):
      super(Dialog, self).__init__(parent)
      self.setLayout(QVBoxLayout())
      self.label = QLabel(str(text))
      self.layout().addWidget(self.label)
      self.resize(200, 50)
      self.exec_()