from krita import *
from PyQt5 import *
import math

class HelperLib():
  def dotProduct(self, v1, v2):
    return v1.x() * v2.x() + v1.y() * v2.y()

  def determinant(self, v1, v2):
    return v1.x() * v2.y() - v1.y() * v2.x()

  def vectorAngle(self, v1, v2):
    return  math.degrees( math.atan2(self.determinant(v1, v2), self.dotProduct(v1, v2)) )

  def twoPointDistance(self, v1, v2):
    return math.sqrt( math.pow(( v2.x() - v1.x() ), 2) + math.pow(( v2.y() - v1.y() ), 2)  )

class GizmoIcon(QWidget):
  def __init__(self, position, width, height, parent=None):
    # super(GizmoIcon, self).__init__(parent)
    QWidget.__init__(self, parent)

    self.position = position
    self.width = int(width)
    self.height = int(height)
    self.setGeometry(int(position.x() - self.width / 2), int(position.y() - self.height / 2), self.width, self.height)
    self.setWindowFlags(self.windowFlags() | QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint)
    self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
    self.setStyleSheet("background: transparent;")
    self.setWindowTitle("icon")

  def showAt(self, position):
    self.move(position.x() - self.width / 2, position.y() - self.height / 2)
    self.show()

  def changeSize(self, radius):
    self.width = radius
    self.height = radius
    self.setGeometry(int(self.position.x() - self.width / 2), int(self.position.y() - self.height / 2), self.width, self.height)
    self.update()

  def paintEvent(self, event):
    self.painter = QPainter(self)
    self.painter.eraseRect(event.rect())
    self.painter.setRenderHints( QPainter.HighQualityAntialiasing )
    self.painter.setPen( QPen(QColor(255, 255, 255, 150), 2) )
    # self.painter.setBrush( QColor(47, 47, 47, 150) )
    self.painter.setBrush( QColor(224, 5, 5, 255) )
    self.painter.drawEllipse(0, 0, self.width, self.height)
    self.painter.end()