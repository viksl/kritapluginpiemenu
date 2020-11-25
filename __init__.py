from krita import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
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
      # self.label2 = QLabel(str(text2))
      self.layout().addWidget(self.label)
      # self.layout().addWidget(self.label2)
      self.resize(200, 50)
      self.exec_()

def dotProduct(v1, v2):
  return v1[0] * v2[0] + v1[1] * v2[1]

def determinant(v1, v2):
  return v1[0] * v2[1] - v1[1] * v2[0]

def vectorAngle(v1, v2):
  return  math.degrees( math.atan2(determinant(v1, v2), dotProduct(v1, v2)) )

def twoPointDistance(v1, v2):
  return math.sqrt( math.pow(( v2.x() - v1.x() ), 2) + math.pow(( v2.y() - v1.y() ), 2)  )

class qWinFilter(QWindow):
  def __init__(self, parent=None):
    super().__init__(parent)

  def eventFilter(self, obj, e):
    if e.buttons():
      Dialog("test left button")
    if e.type() == QEvent.KeyRelease:
      Dialog("test key release")

class CustomRadialMenuExtension(Extension):
  def __init__(self,parent):
    super(CustomRadialMenuExtension, self).__init__(parent)

  def setup(self):
    pass

  def createActions(self, window):
    self.customRadialMenu = window.createAction("CustomRadialMenu", "Radial Menu")
    self.customRadialMenu.setAutoRepeat(False)
    self.customRadialMenu.setCheckable(True)

    self.MAFilter = qWinFilter()


Krita.instance().addExtension(CustomRadialMenuExtension(Krita.instance()))