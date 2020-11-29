from krita import *
# from PyQt5.QtWidgets import *
# from PyQt5.QtCore import *
from PyQt5 import *
import math

DISTANCE_BUFFER = 10                                  # THIS VALUE CAN BE CHANGED TO FIT YOUR NEEDS!
                                                      # Units: Pixels (screen not canvas pixels)
                                                      # Warning: Cannot be negative!
                                                      # How far (in pixels) you need to move your cursor for rotation to take effect (only initially).
                                                      # It makes the transition from not changin rotation to changing it a bit smoother (around 0 <- initial poin)
                                                      # In future it might also serve as a reset for canvas reset to facilitate another function related to
                                                      # canvas rotation.

TIMER_INTERVAL = 50                                   # THIS VALUE CAN BE CHANGED TO FIT YOUR NEEDS!
                                                      # Units: Miliseconds
                                                      # Warning: Cannot be negative!
                                                      # The lower the smoother experience but more cpu intensive (overall it's not a very expensive process
                                                      # so you are fine with going half way down if you feel like it)
                                                      # Don't go to much towards 0 if possible since at very low rates you can get to the moment when
                                                      # krita event loop is as fast as this timer and the rotation will thus fail

current_active_layer = None
current_active_layer_locked_original = False
angle = 0                                             # Current canvas rotation
buffer_lock = False                                   # After cursor moves out of buffer area removes the buffer condition
key_release_lock = True                               # Locks key relese event out when it's not needed to go through the whole event code
init_offset_angle = 0                                 # An angle to keep smooth transition
                                                      # (vectors: v1 = base_vector - init; v2 = cursor (immediately after leaving buffer area) - init)
cursor_init_position = None                           # Cursor position when custom rotation invokation begins
base_vector = [1, 0]                                  # Unit vector as reference to measure angle from
timer = QTimer()                                      # Custom Canvas Rotation main event loop
timer.setInterval(TIMER_INTERVAL)
timer.setSingleShot(True)
release_timer = QTimer()                              # Escape timer from timer event above (acts basically as a key release since key release is repeating
                                                      # as long as a key is down I had to go with a timer to overcome it)
release_timer.setInterval(TIMER_INTERVAL * 2)
release_timer.setSingleShot(True)
timer_lock = False                                    # Locks out unnecessary use of the timer

# Class for testing (replaces a print statement as I don't know how to print on win)
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
        
class tt2(QWidget):
  def __init__(self, parent=None):
    QWidget.__init__(self, parent)
    self.radius = 300
    self.width = self.radius * 2
    self.height = self.radius * 2
    self.centreX = self.width / 2
    self.centreY = self.height / 2
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
    self.setWindowFlags(self.windowFlags() | QtCore.Qt.Window)
    #self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
    self.setStyleSheet("background: transparent;")
    self.setWindowTitle("Widget")        
    self.setGeometry(int( QCursor.pos().x() - self.width / 2 ), int( QCursor.pos().y() - self.height / 2 ), self.width, self.height )
    self.cursorInitPosition = False
    self.labelPaintPoint = False
    self.distancePassed = False
    self.w = win()
    self.labels = [None] * self.totalSplitSections
    self.labelMaxWidth = 150
    #        self.showMaximized()

    self.show()
    Dialog(self.size())

    for i in range(len(self.labels)):
      p = self.circleCoor(self.centreX, self.centreY, self.labelRadius, i * self.splitSectionAngle + self.splitSectionAngle / 2)

      self.labels[i] = QLabel("this is a label " + str(i), self)
      self.labels[i].setFont(QFont('Times', 12))
      self.labels[i].setStyleSheet("color: red")
      self.labels[i].move(p["x"] - self.labels[i].width() / 2, p["y"] - self.labels[i].height() / 2)
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
    path.addEllipse(self.centreX - self.wheelIconOuterRadius, self.centreY - self.wheelIconOuterRadius, self.wheelIconOuterRadius * 2, self.wheelIconOuterRadius * 2)
    path.addEllipse(self.centreX - self.wheelIconInnerRadius, self.centreY - self.wheelIconInnerRadius, self.wheelIconInnerRadius * 2, self.wheelIconInnerRadius * 2)
    self.painter.fillPath(path, self.wheelColor)

    # Split lines
    self.painter.setPen(QPen(self.lineColor, self.wheelIconLineThickness, Qt.SolidLine))

    for i in range(self.totalSplitSections):
      p0 = self.circleCoor(self.centreX, self.centreY, self.wheelIconInnerRadius, i * self.splitSectionAngle)
      p1 = self.circleCoor(self.centreX, self.centreY, self.wheelIconOuterRadius, i * self.splitSectionAngle)            
      self.painter.drawLine(p0["x"], p0["y"], p1["x"], p1["y"])

  def paintEvent(self, event):
    self.painter = QPainter(self)
    self.painter.setRenderHints( QPainter.HighQualityAntialiasing )
    self.drawWheel()
    self.painter.end()
                    
  def eventFilter(self, source, event):
    if event.type() == QtCore.QEvent.MouseMove:
      self.w.p3("cursor X: " + str(QCursor.pos().x()) + " Y:" +  str(QCursor.pos().y()))

      for i in range(0, self.totalSplitSections):
        self.labels[i-1].setStyleSheet("color: red")            

      if (not self.cursorInitPosition):
        self.cursorInitPosition = QCursor.pos()

      distance = self.twoPointDistance(self.cursorInitPosition, QCursor.pos())

      if distance > 10:
        v1 = [self.baseVector[0], self.baseVector[1]]
        v2 = [QCursor.pos().x() - self.cursorInitPosition.x(), QCursor.pos().y() - self.cursorInitPosition.y()]
        angle = self.vectorAngle(v1, v2)

        self.w.p(math.degrees(angle))

        for i in range(0, self.totalSplitSections):
          if i * self.splitSectionAngle < angle - self.splitSectionOffAngle and angle - self.splitSectionOffAngle <=  (i + 1) * self.splitSectionAngle:
            self.w.p2("i: " + str(i) + ", " + str(math.degrees(i * self.splitSectionAngle)) + ", " + str(math.degrees((i + 1) * self.splitSectionAngle)))

            self.labels[i].setStyleSheet("color: green")
            self.w.p2(str(i))

            break
    return super(tt2, self).eventFilter(source, event)

class CustomRadialMenuExtension(Extension):
  def __init__(self,parent):
    super(CustomRadialMenuExtension, self).__init__(parent)

  def setup(self):
    pass

  def createActions(self, window):
    self.rm = tt(window.qwindow())
    self.customRadialMenuAction = window.createAction("CustomRadialMenu", "Radial Menu")
    self.rm.cShortcut = self.customRadialMenuAction.shortcut()

    self.customRadialMenuAction.setAutoRepeat(False)
#    self.customRadialMenuAction.triggered.connect(
#      lambda checked, win=self.rm: CRDTrigger(win))
    # qwin = Krita.instance().activeWindow().qwindow()
    # self.MAFilter = mdiAFilter()


Krita.instance().addExtension(CustomRadialMenuExtension(Krita.instance()))