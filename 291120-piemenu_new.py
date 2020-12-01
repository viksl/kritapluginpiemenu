from krita import *
from PyQt5 import *
from PyQt5.QtCore import pyqtSignal
import math

qwin = Krita.instance().activeWindow().qwindow()
#app = QtWidgets.QApplication(sys.argv)

class Dialog(QDialog):
  def __init__(self, text, parent=None):
      super(Dialog, self).__init__(parent)
      self.setLayout(QVBoxLayout())
      self.label = QLabel(str(text))
      self.layout().addWidget(self.label)
      self.resize(200, 50)
      self.exec_()

class win(QWidget):
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

class MenuArea(QObject):
    def __init__(self, cursorPosition, qWin, parent=None):
        super().__init__(parent)
        self.menus = [
                      {
                           "sections": [
                                       {"name": "aaaaaaaaa aaaaaaa1", "isSubmenu": False, "ref": None},
                                       {"name": "aaaaaaaaaaaaaaaaa2", "isSubmenu": True, "ref": 1},
                                       {"name": "aaaaaaa3", "isSubmenu": False, "ref": None},
                                       {"name": "aaaaaa4", "isSubmenu": False, "ref": None},
                                       {"name": "a5", "isSubmenu": False, "ref": None},
                                       {"name": "a6", "isSubmenu": False, "ref": None},
                                       {"name": "a7", "isSubmenu": False, "ref": None},
                                       {"name": "a7", "isSubmenu": False, "ref": None},
                           ]     
                       },
                      {
                           "sections": [
                                       {"name": "b1", "isSubmenu": False, "ref": None},
                                       {"name": "b2", "isSubmenu": False, "ref": None},
                                       {"name": "b3", "isSubmenu": False, "ref": None},
                                       {"name": "b4", "isSubmenu": False, "ref": None},
                                       {"name": "b5", "isSubmenu": False, "ref": None},
                                       {"name": "b6", "isSubmenu": False, "ref": None},
                                       {"name": "b7", "isSubmenu": False, "ref": None},
                           ]     
                       },
        ]

        self.screenWidth = QApplication.desktop().screenGeometry().width()
        self.screenHeight = QApplication.desktop().screenGeometry().height()
        
        self.menu = PieMenu(QCursor.pos(), self.screenWidth, self.screenHeight, self.menus[0]["sections"], qWin)
        self.menu.initNewMenuSignal.connect(self.initNewMenu)
        self.eventController = EventController(self.menu, qWin)
        
    def initNewMenu(self):
        index = self.menu.labels["activeLabel"]
        p = self.menu.getLabelPositionAt(index)
        self.menu.initNewMenuAt(self, self.menus[self.menus[index]["ref"]]["sections"], QPoint(p["x"], p["y"]))
        pass

#Handles events mouse move + mouse press and sends it where needed (TODO: key release)
class EventController(QMdiArea):
    def __init__(self, eventObj=None, parent=None):
        super().__init__(parent)

        self.installEventFilter(self)
        self.setMouseTracking(True)
        self.eventObj = eventObj

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.MouseButtonPress:
            self.eventObj.eventHandler(event)
        elif event.type() == QtCore.QEvent.MouseMove:
            self.eventObj.eventHandler(event)
            
        return super(EventController, self).eventFilter(source, event)

class PieMenu(QWidget):
    initNewMenuSignal = pyqtSignal()

    def __init__(self, cursorPosition, screenWidth, screenHeight, menuSections, parent=None):
        QWidget.__init__(self, parent)

        self.setGeometry(0, 0, screenWidth, screenHeight)
        self.radius = 300
        self.width = int(self.radius * 2)
        self.height = int(self.radius * 2)
        self.halfWidth = int(self.width / 2)
        self.halfHeight = int(self.height / 2)
        self.wheelIconOuterRadius = 22 *2
        self.wheelIconInnerRadius = 13 *2
        self.labelRadius = self.wheelIconInnerRadius + 180

        self.splitSectionOffAngle = 0
        self.wheelColor = QColor(47, 47, 47, 200)
        self.lineColor = QColor(255, 255, 255, 30)
        self.wheelIconLineThickness = 1
        self.baseVector = [1, 0]
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setStyleSheet("background: transparent;")
        self.setWindowTitle("Quick Access Pie Menu")        
        self.labelPaintPoint = False
        self.distancePassed = False
        self.labelBaseColor = "rgba(47, 47, 47, 200)"
        self.labelActiveColor = "rgba(30, 30, 30, 250)"
        self.labelHighlightColor = "green"    
        self.labelStyleBase = "background-color:" + self.labelBaseColor + "; color: white;"
        self.labelStyleActive = "background-color:" + self.labelActiveColor + "; color: white;"
        self.initNewMenuAt(menuSections, cursorPosition)

        self.w = win()
        
        self.show()

    def initNewMenuAt(self, menuSections, cursorPosition):
        self.menuSections = menuSections
        self.cursorInitPosition = cursorPosition
        self.totalSplitSections = len(self.menuSections)
        self.splitSectionAngle = 2 * math.pi / self.totalSplitSections
        self.splitSectionOffAngle = -(math.pi / 2) - self.splitSectionAngle/2 

        self.labels = {
            "children": [None] * self.totalSplitSections,
            "activeLabel": 0
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
        self.painter.setRenderHints( QPainter.HighQualityAntialiasing )
        self.drawWheel()
        self.painter.end()

    def eventHandler(self, event):        
        if event.type() == QtCore.QEvent.MouseButtonPress:
            self.close()
            #if self.menuSections[self.labels["activeLabel"]]["isSubmenu"]:
                #self.initNewMenuSignal.emit()
        
        if event.type() == QtCore.QEvent.MouseMove:
            self.w.p3("cursor X: " + str(QCursor.pos().x()) + " Y:" +  str(QCursor.pos().y()))
            
            if (not self.cursorInitPosition):
                self.cursorInitPosition = QCursor.pos()

            distance = self.twoPointDistance(self.cursorInitPosition, QCursor.pos())
            
            if distance > self.wheelIconInnerRadius:
                v1 = [self.baseVector[0], self.baseVector[1]]
                v2 = [QCursor.pos().x() - self.cursorInitPosition.x(), QCursor.pos().y() - self.cursorInitPosition.y()]
                angle = self.vectorAngle(v1, v2)
                
                self.w.p(math.degrees(angle))

                for i in range(0, self.totalSplitSections):
                    self.w.p2("i: " + str(i) +  " angle: " + str(angle) + ", angle > con1: " + str(i * self.splitSectionAngle - self.splitSectionOffAngle) + ", angle <= con2: " + str((i + 1) * self.splitSectionAngle - self.splitSectionOffAngle))
                    if ((angle + self.splitSectionOffAngle) % (2*math.pi) > i * self.splitSectionAngle and
                        (angle + self.splitSectionOffAngle) % (2*math.pi) <=  (i + 1) * self.splitSectionAngle):

                        self.labels["children"][self.labels["activeLabel"]].setStyleSheet(self.labelStyleBase) 
                        self.labels["children"][i].setStyleSheet(self.labelStyleActive)
                        self.labels["activeLabel"] = i
                        break
#####
#window = PieMenu(QCursor.pos(), qwin)
menus = MenuArea(QCursor.pos(), qwin)