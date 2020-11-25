from krita import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer
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
  def __init__(self, text, text2, parent=None):
      super(Dialog, self).__init__(parent)
      self.setLayout(QVBoxLayout())
      self.label = QLabel(str(text))
      self.label2 = QLabel(str(text2))
      self.layout().addWidget(self.label)
      self.layout().addWidget(self.label2)
      self.resize(200, 50)
      self.exec_()

def dot_product(v1, v2):
  return v1[0] * v2[0] + v1[1] * v2[1]

def determinant(v1, v2):
  return v1[0] * v2[1] - v1[1] * v2[0]

def vector_angle(v1, v2):
  return  math.degrees( math.atan2(determinant(v1, v2), dot_product(v1, v2)) )

def two_point_distance(v1, v2):
  return math.sqrt( math.pow(( v2.x() - v1.x() ), 2) + math.pow(( v2.y() - v1.y() ), 2)  )

def release_timer_timeout():
  global current_active_layer
  global current_active_layer_locked_original
  global angle
  global buffer_lock
  global key_release_lock
  global init_offset_angle
  global cursor_init_position
  global base_vector
  global timer

  timer.stop()

  key_release_lock = True
  cursor_init_position = None
  buffer_lock = False
  init_offset_angle = 0
  angle = 0
  if current_active_layer != None:
    current_active_layer.setLocked(current_active_layer_locked_original)
  current_active_layer = None

# Reset everything back to default state to be ready for next rotation event
def rotate_timer_timeout():
  global current_active_layer
  global current_active_layer_locked_original
  global angle
  global buffer_lock
  global init_offset_angle
  global cursor_init_position
  global base_vector
  global timer

  if not buffer_lock:
    # Distance from initial point (cursor position trigger event was onvoked from)
    # to cursor's current position
    distance = two_point_distance(cursor_init_position, QCursor.pos())
    
    # If cursor outside buffer zone start immediately calculate initial offset angle
    # to ensure smooth transition when changing angles in followint passes
    if distance > DISTANCE_BUFFER:
      buffer_lock = True

      v1 = [base_vector[0] - cursor_init_position.x(), base_vector[1] - cursor_init_position.y()]
      v2 = [QCursor.pos().x() - cursor_init_position.x(), QCursor.pos().y() - cursor_init_position.y()]
      
      init_offset_angle = vector_angle(v1, v2)
  elif buffer_lock:
    # This handles the canvas rotation itself
    v1 = [base_vector[0] - cursor_init_position.x(), base_vector[1] - cursor_init_position.y()]
    v2 = [QCursor.pos().x() - cursor_init_position.x(), QCursor.pos().y() - cursor_init_position.y()]
    
    canvas = Krita.instance().activeWindow().activeView().canvas()
    canvas.setRotation(angle - init_offset_angle + vector_angle(v1, v2))

  timer.start()

class RadialMenuExtension(Extension):
  def __init__(self,parent):
    super(RadialMenuExtension, self).__init__(parent)

  class mdiAreaFilter(QMdiArea):
    def __init__(self, parent=None):
      super().__init__(parent)

    def eventFilter(self, obj, e):
      global release_timer
      
      if e.type() == QEvent.KeyRelease:
        if key_release_lock:
          return False

        release_timer.start()
        
      return False

  def setup(self):
    pass

  def createActions(self, window):
    self.c_canvas_rotation = window.createAction("c_canvas_rotation", "Custom Canvas Rotation")
    self.c_canvas_rotation.setAutoRepeat(False)
    self.c_canvas_rotation.setCheckable(True)

    self.MAFilter = self.mdiAreaFilter()

    @self.c_canvas_rotation.toggled.connect
    def on_toggle():
      global current_active_layer
      global current_active_layer_locked_original
      global angle
      global buffer_lock
      global key_release_lock
      global init_offset_angle
      global cursor_init_position
      global base_vector
      global timer
      global timer_lock

      canvas = Krita.instance().activeWindow().activeView().canvas()
      
      # Init custom rotation (vars, timer, active layer reference)
      key_release_lock = False
      timer_lock = False
      cursor_init_position = QCursor.pos()
      angle = canvas.rotation()
      current_active_layer = Krita.instance().activeDocument().activeNode()
      current_active_layer_locked_original = current_active_layer.locked()
      current_active_layer.setLocked(True)

      timer.start()

timer.timeout.connect(rotate_timer_timeout)
release_timer.timeout.connect(release_timer_timeout)

Krita.instance().addExtension(RadialMenuExtension(Krita.instance()))