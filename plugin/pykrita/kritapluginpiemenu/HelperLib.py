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

class Gizmo(QObject):
  gizmoUpdatedSignal = pyqtSignal()

  def __init__(self, position=None, width=None, height=None, alpha=255, parent=None):
    super().__init__(parent)

    self.position = position
    self.radius = None
    self.width = int(width) if width != None else width
    self.height = int(height) if height != None else height
    self.alpha = alpha
    self.enabled = False

  def setProperties(self, settings):
    for key, value in settings.items():
      if hasattr(self, key):
        if key == "radius":
          setattr(self, "width", value)
          setattr(self, "height", value)
        else:
          setattr(self, key, value)

    self.enabled = True

    self.gizmoUpdatedSignal.emit()