from krita import *
from PyQt5 import *
from PyQt5.QtCore import QTimer, pyqtSignal
from .HelperLib import Gizmo
import math
from .Debug import Logger

class MenuArea(QObject):
    def __init__(self, menus, actionsList, options, parent=None):
        super().__init__(parent)

        self.eventController = None
        self.options = options
        self.menus = menus
        self.menu = PieMenu(actionsList, self.options, parent)
        
        self.menu.initNewMenuSignal.connect(self.initNewMenu)
        actionsList.hidePieMenuSignal.connect(self.hidePieMenu)

    def initNewMenu(self):
        index = self.menu.labels["activeLabel"]
        submenuRef = self.menus["menu"][index]["ref"]

        cursor = self.menu.getCurrentPosition()

        # v = QPoint( ( cursor.x() - self.menu.cursorInitPosition.x() ) * 0.6, ( cursor.y() - self.menu.cursorInitPosition.y() ) * 0.6 )
        v = QPoint( ( cursor.x() - self.menu.cursorInitPosition.x() ) * self.options["submenuPositionOffset"], ( cursor.y() - self.menu.cursorInitPosition.y() ) * self.options["submenuPositionOffset"] )

        newCenter =  QPoint( QCursor.pos().x() + v.x(), QCursor.pos().y() + v.y() ) 

        self.menu.initNewMenuAt( self.menus["submenus"][str(submenuRef)] , newCenter )

    def hidePieMenu(self):
        self.menu.ResetGUI()

#Handles events mouse move + mouse press and sends it where needed
class EventController(QMdiArea):
    def __init__(self, eventObj=None, parent=None, controllerOwner=None):
        super().__init__(parent)

        self.setMouseTracking(True)
        self.eventObj = eventObj
        self.controllerOwner = controllerOwner
        self.mouseButtonPressed = False
        self.buttonReleased = False
        self.resetKeyPressed = False

###################################################################################################
# START EVENT FILTER
###################################################################################################
    def eventFilter(self, source, event):
###################################################################################################
# KEY PRESS EVENT RESET
###################################################################################################
        if (
            hasattr(self, "controllerOwner")
            and hasattr(self.controllerOwner, "eventController")
            and self.controllerOwner.eventController != None
            and self.resetKeyPressed
        ):
            return super(EventController, self).eventFilter(source, event)
###################################################################################################
# KEY PRESS
###################################################################################################
# KeyPress + KeyRelease is needed because on windows the events are not triggered the same
# as on Linux
        if (
            (
                event.type() == QEvent.KeyPress
                or (event.type() == QEvent.KeyRelease
                    and self.mouseButtonPressed)
            )
            and not event.isAutoRepeat()
            and Krita.instance().action("kritapluginpiemenu").shortcut().matches(event.key())
            and hasattr(self, "controllerOwner")
            and hasattr(self.controllerOwner, "eventController")
            and self.controllerOwner.eventController != None
            and not self.resetKeyPressed
            and not self.buttonReleased
        ):
            self.deleteEventFilter()
            self.resetKeyPressed = True

            event.accept()
            return True
###################################################################################################
# MOUSE BUTTON PRESS
###################################################################################################
        elif (
            ((event.type() == QEvent.MouseButtonPress
            and event.button() == QtCore.Qt.LeftButton)
            or event.type() == QEvent.TabletPress)
            and hasattr(self, "controllerOwner")
            and hasattr(self.controllerOwner, "eventController")
            and self.controllerOwner.eventController != None
            and not self.mouseButtonPressed
            and not self.resetKeyPressed
        ):
            self.mouseButtonPressed = True

            event.accept()
            return True
###################################################################################################
# MOUSE BUTTON/TABLET RELEASE
###################################################################################################
        elif (
            (event.type() == QEvent.MouseButtonRelease
            or event.type() == QEvent.TabletRelease)
            and hasattr(self, "controllerOwner")
            and hasattr(self.controllerOwner, "eventController")
            and self.controllerOwner.eventController != None
            and self.mouseButtonPressed
            and not self.buttonReleased
            and not self.resetKeyPressed
        ):
            self.eventObj.eventHandler(event)
            self.deleteEventFilter()
            self.buttonReleased = True

            event.accept()
            return True
###################################################################################################
# MOUSE MOVE
###################################################################################################
        elif (
            event.type() == QEvent.MouseMove
            and hasattr(self, "controllerOwner")
            and hasattr(self.controllerOwner, "eventController")
            and self.controllerOwner.eventController != None
            and self.mouseButtonPressed
            and not self.buttonReleased
            and not self.resetKeyPressed
        ):
            self.eventObj.eventHandler(event)

            event.accept()
            return True
###################################################################################################
# CATCH PROBLEM EVENTS WHILE THE MENU IS ACTIVE
###################################################################################################
        elif (
            event.type() == QEvent.KeyPress
            or event.type() == QEvent.MouseMove
            or event.type() == QEvent.TabletPress
            or event.type() == QEvent.MouseButtonPress
            or event.type() == QEvent.MouseButtonRelease
            or event.type() == QEvent.TabletRelease
        ):
            event.accept()
            return True
###################################################################################################
        return super(EventController, self).eventFilter(source, event)
###################################################################################################
# END EVENT FILTER
###################################################################################################

    def deleteEventFilter(self):
        if hasattr( self.controllerOwner, "eventController" ):
            self.eventObj.ResetGUI()
            QTimer.singleShot(10, self.eventObj.hide)

            if self.controllerOwner.eventController != None:
                self.controllerOwner.eventController.deleteLater()

        self.controllerOwner.eventController = None
        
        QApplication.restoreOverrideCursor()

class PieMenu(QWidget):
    initNewMenuSignal = pyqtSignal()

    def __init__(self, actionsList, options, parent=None):
        QWidget.__init__(self, parent)

        self.actionsList = actionsList
        self.options = options
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setStyleSheet("background: transparent;")
        self.setWindowTitle("Quick Access Pie Menu")
        self.wheelIconOuterRadius = self.options["wheelInnerRadius"] *2                   # TWEAK
        self.wheelIconInnerRadius = self.options["wheelOuterRadius"] *2                   # TWEAK
        self.wheelColor = self.options["wheelColor"]           # TWEAK
        self.lineColor = self.options["wheelLineColor"]          # TWEAK
        self.wheelIconLineThickness = self.options["wheelLineThickness"]                     # TWEAK
        
        self.labelRadius = self.wheelIconInnerRadius + self.options["labelRadius"]  # TWEAK

        self.baseVector = [1, 0]

        self.labelBaseColor = self.options["labelBaseColor"]       # TWEAK
        self.labelActiveColor = self.options["labelActiveColor"]     # TWEAK
        self.labelStyleBase = "background-color:" + self.labelBaseColor + "; color: white;"
        self.labelStyleActive = "background-color:" + self.labelActiveColor + "; color: white;"

        self.gizmo = Gizmo()

        self.timerTime = 0
        self.labelPaintPoint = False
        self.distancePassed = False
        self.clearPainter = False
        self.previousAction = None
        self.callback = None
        self.resetCallback = None
        self.distance = None
        self.renderGizmo = False
        self.renderWheel = False

        self.gizmo.gizmoUpdatedSignal.connect(self.OnGizmoUpdatedSignal)

    def OnGizmoUpdatedSignal (self):
        self.gizmo.position = self.getCurrentPosition(self.gizmo.position)
        self.renderGizmo = True
        self.update()

    def initNewMenuAt(self, menuSections, cursorPosition):
        self.clearPainter = False
        self.renderGizmo = False
        self.gizmo.enabled = False
        self.renderWheel = True
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
            self.labels["children"][i].setFont(QFont('Times', self.options["fontSize"]))  # TWEAK
            self.labels["children"][i].adjustSize()
            self.labels["children"][i].setGeometry(int(p["x"]), int(p["y"]), self.options["labelWidth"], self.options["labelHeight"])   # TWEAK
            self.labels["children"][i].move(int(self.labels["children"][i].x() - self.labels["children"][i].width() / 2), int(self.labels["children"][i].y() - self.labels["children"][i].height()/ 2))
            self.labels["children"][i].setStyleSheet(self.labelStyleBase)
            self.labels["children"][i].setAlignment(QtCore.Qt.AlignCenter)
            self.labels["children"][i].setWordWrap(True)
            self.labels["children"][i].show()
        
        self.update()

    def ResetGUI( self ):
        self.clearPainter = True
        self.renderWheel = False
        self.renderGizmo = False
        
        if hasattr(self, "labels") and len(self.labels["children"]) > 0:
            for label in self.labels["children"]:
                label.hide()
                label.deleteLater()
            self.labels["children"] = []

        self.update()
        # QApplication.processEvents()

    def InvokeAction(self, action, isCallback=False):
        if action != None:
            if isCallback:
                QTimer.singleShot(self.timerTime, lambda: action())
                return
            elif action.isCheckable():
                QTimer.singleShot(self.timerTime, lambda: action.toggle())
            else:
                QTimer.singleShot(self.timerTime, lambda: action.trigger())

    def eventHandler(self, event):
        if event.type() == QEvent.MouseButtonRelease or event.type() == QEvent.TabletRelease:
            if self.resetCallback != None:
                self.InvokeAction(self.resetCallback , True)
                return
                
            if self.distance == None:
                return

            elif self.previousAction is not None and self.distance < self.wheelIconOuterRadius:
                action = Krita.instance().action( self.previousAction )

                self.InvokeAction(action)

            elif not(self.labels["activeLabel"] is None):
                action = Krita.instance().action( self.menuSections[self.labels["activeLabel"]]["actionID"] )
                
                self.InvokeAction(action)

        elif event.type() == QtCore.QEvent.MouseMove:
            if (not self.cursorInitPosition):
                self.cursorInitPosition = QCursor.pos()

            if self.callback != None:
                self.InvokeAction(self.callback , True)
                return

            self.distance = self.twoPointDistance(self.cursorInitPosition, self.getCurrentPosition())

            if self.distance >= self.wheelIconOuterRadius:
                cursor = self.getCurrentPosition()

                v1 = [self.baseVector[0], self.baseVector[1]]
                v2 = [cursor.x() - self.cursorInitPosition.x(), cursor.y() - self.cursorInitPosition.y()]

                self.angle = self.vectorAngle(v1, v2)

                self.callback = None
                self.resetCallback = None

                for i in range(0, self.totalSplitSections):
                    if ((self.angle + self.splitSectionOffAngle) % (2*math.pi) > i * self.splitSectionAngle and
                        (self.angle + self.splitSectionOffAngle) % (2*math.pi) <=  (i + 1) * self.splitSectionAngle):

                        if self.labels["activeLabel"] is not None:
                            self.labels["children"][self.labels["activeLabel"]].setStyleSheet(self.labelStyleBase)
                        
                        self.labels["children"][i].setStyleSheet(self.labelStyleActive)
                        self.labels["activeLabel"] = i

                        # Display submenu
                        if self.labels["activeLabel"] != None and self.menuSections[self.labels["activeLabel"]]["isSubmenu"] and self.menuSections[self.labels["activeLabel"]]["callback"] == None:
                            self.previousAction = self.menuSections[self.labels["activeLabel"]]["actionID"]
                            self.initNewMenuSignal.emit()

                        # Get callback, reserCallback and Init the action    
                        if self.labels["activeLabel"] != None and not( self.menuSections[self.labels["activeLabel"]]["isSubmenu"] ):
                            if self.menuSections[self.labels["activeLabel"]]["callback"] != None:
                                self.callback = getattr(self.actionsList, self.menuSections[self.labels["activeLabel"]]["callback"] )
                            if self.menuSections[self.labels["activeLabel"]]["resetCallback"] != None:
                                self.resetCallback = getattr(self.actionsList, self.menuSections[self.labels["activeLabel"]]["resetCallback"] )
                            if self.menuSections[self.labels["activeLabel"]]["init"] != None:
                                init = getattr(self.actionsList, self.menuSections[self.labels["activeLabel"]]["init"] )
                                init(self.gizmo)

                        break
            else:
                for label in self.labels["children"]:
                    label.setStyleSheet(self.labelStyleBase)
                self.labels["activeLabel"] = None

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

    def paintWheel(self):
        # Wheel ring
        path = QPainterPath()
        path.addEllipse(self.cursorInitPosition.x() - self.wheelIconOuterRadius, self.cursorInitPosition.y() - self.wheelIconOuterRadius, self.wheelIconOuterRadius * 2, self.wheelIconOuterRadius * 2)
        path.addEllipse(self.cursorInitPosition.x() - self.wheelIconInnerRadius, self.cursorInitPosition.y() - self.wheelIconInnerRadius, self.wheelIconInnerRadius * 2, self.wheelIconInnerRadius * 2)
        self.painter.fillPath(path, self.wheelColor)
        
        # Split lines
        self.painter.setPen(QPen(self.lineColor, self.wheelIconLineThickness, QtCore.Qt.SolidLine))
        
        for i in range(self.totalSplitSections):
            p0 = self.circleCoor(self.cursorInitPosition.x(), self.cursorInitPosition.y(), self.wheelIconInnerRadius, i * self.splitSectionAngle)
            p1 = self.circleCoor(self.cursorInitPosition.x(), self.cursorInitPosition.y(), self.wheelIconOuterRadius, i * self.splitSectionAngle)            
            self.painter.drawLine(p0["x"], p0["y"], p1["x"], p1["y"])

    def paintGizmo( self, gizmo ):
        self.painter.setPen( QPen(QColor(255, 255, 255, gizmo.alpha), 2) )
        self.painter.setBrush( QColor(224, 5, 5, gizmo.alpha) )
        self.painter.drawEllipse(gizmo.position.x() - gizmo.width / 2, gizmo.position.y() - gizmo.height / 2, gizmo.width, gizmo.height)

    def paintEvent(self, event):
        self.painter = QPainter(self)
        self.painter.eraseRect(event.rect())
        self.painter.setRenderHints( QPainter.HighQualityAntialiasing )

        if self.renderWheel:
            self.paintWheel()

        if self.renderGizmo and self.gizmo.enabled:
            self.paintGizmo(self.gizmo)

        self.painter.end()

    def getCurrentPosition(self, aPosition=None):
        position = QCursor.pos() if aPosition == None else aPosition
        screen = QGuiApplication.screenAt(position)

        return QPoint(position.x() - screen.geometry().x(), position.y() - screen.geometry().y())
