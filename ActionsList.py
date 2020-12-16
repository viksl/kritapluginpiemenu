from krita import *
from PyQt5 import *

class Dialog(QDialog):
  def __init__(self, text, parent=None):
      super(Dialog, self).__init__(parent)
      self.setLayout(QVBoxLayout())
      self.label = QLabel(str(text))
      self.layout().addWidget(self.label)
      self.resize(200, 50)
      self.exec_()

class ActionsList():
    actionsList = [
        {"name": "Ellipse Tool", "actionID": "KritaShape/KisToolEllipse", "callback": None},
        {"name": "Contiguous Selection Tool", "actionID": "KisToolSelectContiguous", "callback": None},
        {"name": "Freehand Brush Tool", "actionID": "KritaShape/KisToolBrush", "callback": None},
        {"name": "Zoom Tool", "actionID": "ZoomTool", "callback": None},
        {"name": "Fill Tool", "actionID": "KritaFill/KisToolFill", "callback": None},
        {"name": "Zoom", "actionID": None, "callback": "Zoom"}
    ]

    def Init( self ):
        self.zoomStep = 1/100
        self.position = None
        self.previousPosition = None

    def Zoom( self ):
        # TODO: check how far cursor travelled and zoom in/out more or less and compare it to the current method
        if self.position == None:
            self.position = QCursor.pos()
        
        if self.previousPosition == None:
            self.previousPosition = self.position

        direction = 1
        extraStep = 1

        if QCursor.pos().y() == self.previousPosition.y():
            return

        canvas = Krita.instance().activeWindow().activeView().canvas()

        if self.previousPosition.y() - QCursor.pos().y() < 0:
            direction = -1

        extraStep = 1 + int( canvas.zoomLevel() * 24 / 100 )
        # if canvas.zoomLevel() * 24 > 200:
        #     extraStep = 5

        # if canvas.zoomLevel() * 24 > 600:
        #     extraStep = 10

        canvas.setZoomLevel( canvas.zoomLevel() * 24 / 100  + self.zoomStep * extraStep * direction)

        self.previousPosition = QCursor().pos()