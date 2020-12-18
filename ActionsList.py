from krita import *
from PyQt5 import *
from .HelperLib import *
from .Win import Win

win = Win()

class ActionsList(QObject):
    hidePieMenuSignal = pyqtSignal()

    actionsList = [
        {"name": "Ellipse Tool", "actionID": "KritaShape/KisToolEllipse", "callback": None, "resetCallback": None},
        {"name": "Contiguous Selection Tool", "actionID": "KisToolSelectContiguous", "callback": None, "resetCallback": None},
        {"name": "Freehand Brush Tool", "actionID": "KritaShape/KisToolBrush", "callback": None, "resetCallback": None},
        {"name": "Fill Tool", "actionID": "KritaFill/KisToolFill", "callback": None, "resetCallback": None},
        {"name": "Zoom", "actionID": None, "callback": "Zoom", "resetCallback": None},
        {"name": "Rotate Canvas", "actionID": None, "callback": "RotateCanvas", "resetCallback": "RemoveGizmo"},
        {"name": "Brush Size", "actionID": None, "callback": "BrushSize", "resetCallback": "RemoveGizmo"},
        {"name": "Brush Opacity", "actionID": None, "callback": "BrushOpacity", "resetCallback": "RemoveGizmo"},
        {"name": "Brush Flow", "actionID": None, "callback": "BrushFlow", "resetCallback": "RemoveGizmo"},
    ]

    h = HelperLib()

    zoomStep = 1/100
    brushSizeStep = 0.2
    paintingOpacityStep = 0.01
    baseVector = QPoint(1, 0)
    baseDPI = 72    # If the setzoomlevel and zoomlevel ever return same values this value might not be needed

    def __init__(self, parent=None):
        super(ActionsList, self).__init__(parent)

    def Init( self ):
        self.position = None
        self.previousPosition = None
        self.angle = None
        self.initDistanceTravelled = None
        self.initOffsetAngle = None
        self.gizmo = None
        self.hidePieMenuSignalEmitted = False

    def Zoom( self ):
        self.hidePieMenu()

        cursor = QCursor.pos()

        if self.position == None:
            self.position = cursor
        
        if self.previousPosition == None:
            self.previousPosition = self.position

        direction = 1
        steps = 0

        if cursor.y() == self.previousPosition.y() or abs( self.previousPosition.y() - cursor.y() ) < 2:
            return

        canvas = Krita.instance().activeWindow().activeView().canvas()
        res = Krita.instance().activeDocument().resolution()

        if self.previousPosition.y() - cursor.y() < 0:
            direction = -1

        steps = abs( self.previousPosition.y() - cursor.y() )

        if steps < 1:
            steps = 0

        canvas.setZoomLevel( canvas.zoomLevel() * self.baseDPI / res  + self.zoomStep * steps * direction)

        self.previousPosition = cursor

    def RotateCanvas( self ):
        self.hidePieMenu()

        canvas = Krita.instance().activeWindow().activeView().canvas()

        if self.position == None:
            self.position = QCursor.pos()

        if self.angle == None:
             self.angle = canvas.rotation()

        if self.gizmo == None:
            self.gizmo = GizmoIcon(self.position, 10, 10, self.parent())
            self.gizmo.showAt(self.position)

        self.initDistanceTravelled = self.h.twoPointDistance(self.position, QCursor.pos())

        if self.initDistanceTravelled != None and self.initDistanceTravelled < 10:
            return

        if self.initOffsetAngle == None:
            v1 = QPoint(self.baseVector.x() - self.position.x(),
                    self.baseVector.y() - self.position.y())
            v2 = QPoint(QCursor.pos().x() - self.position.x(),
                    QCursor.pos().y() - self.position.y())
                
            self.initOffsetAngle = self.h.vectorAngle(v1, v2)

        v1 = QPoint( self.baseVector.x() - self.position.x(),
                self.baseVector.y() - self.position.y() )

        v2 = QPoint( QCursor.pos().x() - self.position.x(),
                QCursor.pos().y() - self.position.y() )

        canvas.setRotation(self.angle - self.initOffsetAngle + self.h.vectorAngle(v1, v2))

    def BrushSize( self ):
        self.hidePieMenu()

        cursor = QCursor.pos()

        if self.position == None:
            self.position = cursor
        
        if self.previousPosition == None:
            self.previousPosition = self.position

        view = Krita.instance().activeWindow().activeView()
        canvas = Krita.instance().activeWindow().activeView().canvas()
        res = Krita.instance().activeDocument().resolution()
        
        zoom = canvas.zoomLevel() * self.baseDPI / res

        if self.gizmo == None:
            self.gizmo = GizmoIcon(self.position, 10, 10, self.parent())
            self.gizmo.changeSize(view.brushSize() * zoom)
            self.gizmo.show()

        direction = 1
        steps = 0

        if cursor.x() == self.previousPosition.x() or abs( self.previousPosition.x() - cursor.x() ) < 2:
            return

        if self.previousPosition.x() - cursor.x() > 0:
            direction = -1

        steps = int( abs( self.previousPosition.x() - cursor.x() ) )

        size = view.brushSize() + self.brushSizeStep * steps * direction

        view.setBrushSize( size )

        self.gizmo.changeSize( size * zoom )

        self.previousPosition = cursor

    def BrushOpacity( self ):
        global win

        self.hidePieMenu()

        cursor = QCursor.pos()

        if self.position == None:
            self.position = cursor
        
        if self.previousPosition == None:
            self.previousPosition = self.position

        view = Krita.instance().activeWindow().activeView()
        canvas = Krita.instance().activeWindow().activeView().canvas()
        res = Krita.instance().activeDocument().resolution()
        
        zoom = canvas.zoomLevel() * self.baseDPI / res

        if self.gizmo == None:
            self.gizmo = GizmoIcon(self.position, 10, 10, self.parent())
            self.gizmo.changeSize(view.brushSize() * zoom)
            self.gizmo.show()

        direction = 1
        steps = 0

        if cursor.x() == self.previousPosition.x() or abs( self.previousPosition.x() - cursor.x() ) < 2:
            return

        if self.previousPosition.x() - cursor.x() > 0:
            direction = -1

        steps = int( abs( self.previousPosition.x() - cursor.x() ) )

        alpha = view.paintingOpacity() + self.paintingOpacityStep * steps * direction

        if alpha > 1:
            alpha = 1
        elif alpha < 0:
            alpha = 0

        view.setPaintingOpacity( alpha )

        self.gizmo.changeOpacity( alpha * 255 )

        self.previousPosition = cursor

    def BrushFlow( self ):
        global win

        self.hidePieMenu()

        cursor = QCursor.pos()

        if self.position == None:
            self.position = cursor
        
        if self.previousPosition == None:
            self.previousPosition = self.position

        view = Krita.instance().activeWindow().activeView()
        canvas = Krita.instance().activeWindow().activeView().canvas()
        res = Krita.instance().activeDocument().resolution()
        
        zoom = canvas.zoomLevel() * self.baseDPI / res

        if self.gizmo == None:
            self.gizmo = GizmoIcon(self.position, 10, 10, self.parent())
            self.gizmo.changeSize(view.brushSize() * zoom)
            self.gizmo.show()

        direction = 1
        steps = 0

        if cursor.x() == self.previousPosition.x() or abs( self.previousPosition.x() - cursor.x() ) < 2:
            return

        if self.previousPosition.x() - cursor.x() > 0:
            direction = -1

        steps = int( abs( self.previousPosition.x() - cursor.x() ) )

        alpha = view.paintingFlow() + self.paintingOpacityStep * steps * direction

        if alpha > 1:
            alpha = 1
        elif alpha < 0:
            alpha = 0

        view.setPaintingFlow( alpha )

        self.gizmo.changeOpacity( alpha * 255 )

        self.previousPosition = cursor

    def RemoveGizmo( self ):
        if self.gizmo != None:
            self.gizmo.deleteLater()
            self.gizmo = None

    def hidePieMenu( self ):
        if not self.hidePieMenuSignalEmitted:
            self.hidePieMenuSignalEmitted = True
            self.hidePieMenuSignal.emit()

class Dialog(QDialog):
  def __init__(self, text, parent=None):
      super(Dialog, self).__init__(parent)
      self.setLayout(QVBoxLayout())
      self.label = QLabel(str(text))
      self.layout().addWidget(self.label)
      self.resize(200, 50)
      self.exec_()