from krita import *
from PyQt5 import *
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
        QWidget.__init__(self, parent)
        self.width = 400
        self.height = 200
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.Window)
        self.setWindowTitle("Print")        
        self.setGeometry(0, 0, self.width, self.height )
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
                
class tt2(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.radius = 300
        self.desktop = QApplication.desktop()
#        self.screenRect = self.desktop.screenGeometry()
        self.screenWidth= self.desktop.screenGeometry().width()
        self.screenHeight= self.desktop.screenGeometry().height()
        self.desktop = None
        self.width = int(self.radius * 2)
        self.height = int(self.radius * 2)
        self.halfWidth = int(self.width / 2)
        self.halfHeight = int(self.height / 2)
        self.wheelIconOuterRadius = 30 *2
        self.wheelIconInnerRadius = 20 *2
        self.labelRadius = self.wheelIconInnerRadius + 100
        self.totalSplitSections = 7
        self.splitSectionAngle = 2 * math.pi / self.totalSplitSections
#        self.splitSectionOffAngle = (math.pi / 2) - self.splitSectionAngle
        self.splitSectionOffAngle = -(math.pi / 2) - self.splitSectionAngle/2  #this one is ok
        self.splitSectionOffAngle = 0
        self.wheelColor = QColor(47, 47, 47, 150)
        self.lineColor = QColor(255, 255, 255, 30)
        self.wheelIconLineThickness = 1
        self.baseVector = [1, 0]
        #self.setWindowFlags(self.windowFlags() | QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint)
        #self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.Window)
        self.setStyleSheet("background: transparent;")
        self.setWindowTitle("Widget")        
        #self.setGeometry(0, 0, int(self.screenWidth), int(self.screenHeight))
        self.setGeometry(0, 0, self.screenWidth, self.screenHeight)
        self.cursorInitPosition = False
        self.labelPaintPoint = False
        self.distancePassed = False
        self.w = win()
        self.labels = [None] * self.totalSplitSections
        self.labelMaxWidth = 150
        self.currentlySelectedOption = 0
        self.labelBaseColor = "color: red"
        self.labelHighlightColor = "color: green"
        self.initLabels()
                
        self.w.p4(str( self.screenWidth ) + " x " + str( self.screenHeight ))
        
        self.setMouseTracking(True)
        self.installEventFilter(self)
        self.show()


    def initLabels(self):
        for i in range(len(self.labels)):
            p = self.circleCoor(self.cursorInitPosition.x(), self.cursorInitPosition.y(), self.labelRadius, i * self.splitSectionAngle + self.splitSectionAngle / 2)
            
            self.labels[i] = QLabel("this is a label " + str(i), self)
            self.labels[i].setFont(QFont('Times', 12))
            self.labels[i].setStyleSheet("color: red")
            self.labels[i].move(int(p["x"] - self.labels[i].width() / 2), int(p["y"] - self.labels[i].height() / 2))
            self.labels[i].show()

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
#        path.addEllipse(self.centreX - self.wheelIconOuterRadius, self.centreY - self.wheelIconOuterRadius, self.wheelIconOuterRadius * 2, self.wheelIconOuterRadius * 2)
#        path.addEllipse(self.centreX - self.wheelIconInnerRadius, self.centreY - self.wheelIconInnerRadius, self.wheelIconInnerRadius * 2, self.wheelIconInnerRadius * 2)
        path.addEllipse(self.cursorInitPositionPosition.x() - self.wheelIconOuterRadius, self.cursorInitPositionPosition.y() - self.wheelIconOuterRadius, self.wheelIconOuterRadius * 2, self.wheelIconOuterRadius * 2)
        path.addEllipse(self.cursorInitPositionPosition.x() - self.wheelIconInnerRadius, self.cursorInitPositionPosition.y() - self.wheelIconInnerRadius, self.wheelIconInnerRadius * 2, self.wheelIconInnerRadius * 2)
        self.painter.fillPath(path, self.wheelColor)
        
        # Split lines
        self.painter.setPen(QPen(self.lineColor, self.wheelIconLineThickness, Qt.SolidLine))
        
        for i in range(self.totalSplitSections):
            p0 = self.circleCoor(self.cursorInitPositionPosition.x(), self.cursorInitPositionPosition.y(), self.wheelIconInnerRadius, i * self.splitSectionAngle)
            p1 = self.circleCoor(self.cursorInitPositionPosition.x(), self.cursorInitPositionPosition.y(), self.wheelIconOuterRadius, i * self.splitSectionAngle)            
            self.painter.drawLine(p0["x"], p0["y"], p1["x"], p1["y"])

    def paintEvent(self, event):
        self.painter = QPainter(self)
        self.painter.setRenderHints( QPainter.HighQualityAntialiasing )
        self.drawWheel()
        self.painter.end()
                    
    def eventFilter(self, source, event):        
        #if event.type() == QtCore.QEvent.MouseButtonPress:
            #self.hide()
        
        if event.type() == QtCore.QEvent.MouseMove:
            self.w.p3("cursor X: " + str(QCursor.pos().x()) + " Y:" +  str(QCursor.pos().y()))

            for i in range(0, self.totalSplitSections):
                self.labels[i].setStyleSheet("color: red")            
            
            if (not self.cursorInitPosition):
                self.cursorInitPosition = QCursor.pos()

            distance = self.twoPointDistance(self.cursorInitPosition, QCursor.pos())

            if distance > self.wheelIconInnerRadius:
                v1 = [self.baseVector[0], self.baseVector[1]]
                v2 = [QCursor.pos().x() - self.cursorInitPosition.x(), QCursor.pos().y() - self.cursorInitPosition.y()]
                angle = self.vectorAngle(v1, v2)

                self.w.p(math.degrees(angle))

                for i in range(0, self.totalSplitSections):
                    if i * self.splitSectionAngle < angle - self.splitSectionOffAngle and angle - self.splitSectionOffAngle <=  (i + 1) * self.splitSectionAngle:
                        self.w.p2("i: " + str(i) + ", " + str(math.degrees(i * self.splitSectionAngle)) + ", " + str(math.degrees((i + 1) * self.splitSectionAngle)))
                        
                        self.labels.currentlySelectedOption.setStyleSheet(self.labelBaseColor)
                        self.labels[i].setStyleSheet(self.labelHighlightColor)
                        self.currentlySelectedOption = i
                        self.w.p2(str(i))
                        break
                        
        return super(tt2, self).eventFilter(source, event)

window = tt2(qwin)
window.cursorInitPosition = QCursor.pos()
window.initLabels()