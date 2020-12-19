from krita import *
from PyQt5 import *
from .HelperLib import *
from .Win import Win

win = Win()

class ActionsList(QObject):
    hidePieMenuSignal = pyqtSignal()

    actionsList = [
        {"name": "Ellipse Tool", "actionID": "KritaShape/KisToolEllipse", "callback": None, "resetCallback": None},
        {"name": "Freehand Brush Tool", "actionID": "KritaShape/KisToolBrush", "callback": None, "resetCallback": None},
        {"name": "Fill Tool", "actionID": "KritaFill/KisToolFill", "callback": None, "resetCallback": None},
        {"name": "Mirror View", "actionID": "mirror_canvas", "callback": None, "resetCallback": None},
        {"name": "Eraser Mode", "actionID": "erase_action", "callback": None, "resetCallback": None},
        {"name": "Paint Layer", "actionID": "add_new_paint_layer", "callback": None, "resetCallback": None},
        {"name": "Quick Clipping Group", "actionID": "create_quick_clipping_group", "callback": None, "resetCallback": None},
        {"name": "Duplicate Layer", "actionID": "duplicatelayer", "callback": None, "resetCallback": None},
        {"name": "Delete Layer", "actionID": "remove_layer", "callback": None, "resetCallback": None},
        {"name": "Select Shapes Tool", "actionID": "InteractionTool", "callback": None, "resetCallback": None},
        {"name": "Text Tool", "actionID": "SvgTextTool", "callback": None, "resetCallback": None},
        {"name": "Edit Shapes Tool", "actionID": "PathTool", "callback": None, "resetCallback": None},
        {"name": "Calligraphy", "actionID": "KarbonCalligraphyTool", "callback": None, "resetCallback": None},
        {"name": "Line Tool", "actionID": "KritaShape/KisToolLine", "callback": None, "resetCallback": None},
        {"name": "Rectangle Tool", "actionID": "KritaShape/KisToolRectangle", "callback": None, "resetCallback": None},
        {"name": "Ellipse Tool", "actionID": "KritaShape/KisToolEllipse", "callback": None, "resetCallback": None},
        {"name": "Polygon Tool", "actionID": "KisToolPolygon", "callback": None, "resetCallback": None},
        {"name": "Polyline Tool", "actionID": "KisToolPolyline", "callback": None, "resetCallback": None},
        {"name": "Bezier Curve Tool", "actionID": "KisToolPath", "callback": None, "resetCallback": None},
        {"name": "Freehand Path Tool", "actionID": "KisToolPencil", "callback": None, "resetCallback": None},
        {"name": "Dynamic Brush Tool", "actionID": "KritaShape/KisToolDyna", "callback": None, "resetCallback": None},
        {"name": "Multibrush Tool", "actionID": "KritaShape/KisToolMultiBrush", "callback": None, "resetCallback": None},
        {"name": "Transform Tool", "actionID": "KisToolTransform", "callback": None, "resetCallback": None},
        {"name": "Move Tool", "actionID": "KritaTransform/KisToolMove", "callback": None, "resetCallback": None},
        {"name": "Crop Tool", "actionID": "KisToolCrop", "callback": None, "resetCallback": None},
        {"name": "Gradient Tool", "actionID": "KritaFill/KisToolGradient", "callback": None, "resetCallback": None},
        {"name": "Color Picker", "actionID": "KritaSelected/KisToolColorPicker", "callback": None, "resetCallback": None},
        {"name": "Color Selector", "actionID": "show_color_selector", "callback": None, "resetCallback": None},
        {"name": "Colorize Mask Tool", "actionID": "KritaShape/KisToolLazyBrush", "callback": None, "resetCallback": None},
        {"name": "Smart Patch Tool", "actionID": "KritaShape/KisToolSmartPatch", "callback": None, "resetCallback": None},
        {"name": "Assistant Tool", "actionID": "KisAssistantTool", "callback": None, "resetCallback": None},
        {"name": "Measurement Tool", "actionID": "KritaShape/KisToolMeasure", "callback": None, "resetCallback": None},
        {"name": "Reference Images Tool", "actionID": "ToolReferenceImages", "callback": None, "resetCallback": None},
        {"name": "Rectangular Selection Tool", "actionID": "KisToolSelectRectangular", "callback": None, "resetCallback": None},
        {"name": "Elliptical Selection Tool", "actionID": "KisToolSelectElliptical", "callback": None, "resetCallback": None},
        {"name": "Polygonal Selection Tool", "actionID": "KisToolSelectPolygonal", "callback": None, "resetCallback": None},
        {"name": "Outline Selection Tool", "actionID": "KisToolSelectOutline", "callback": None, "resetCallback": None},
        {"name": "Contiguous Selection Tool", "actionID": "KisToolSelectContiguous", "callback": None, "resetCallback": None},
        {"name": "Similar Color Selection Tool", "actionID": "KisToolSelectSimilar", "callback": None, "resetCallback": None},
        {"name": "Bezier Curve Selection Tool", "actionID": "KisToolSelectPath", "callback": None, "resetCallback": None},
        {"name": "Magnetic Selection Tool", "actionID": "KisToolSelectMagnetic", "callback": None, "resetCallback": None},
        {"name": "Zoom Tool", "actionID": "ZoomTool", "callback": None, "resetCallback": None},
        {"name": "Pan Tool", "actionID": "PanTool", "callback": None, "resetCallback": None},
        {"name": "Transparency Mask", "actionID": "add_new_transparency_mask", "callback": None, "resetCallback": None},
        {"name": "Filter Mask", "actionID": "add_new_filter_mask", "callback": None, "resetCallback": None},
        {"name": "Colorize Mask", "actionID": "add_new_colorize_mask", "callback": None, "resetCallback": None},
        {"name": "Previous Preset", "actionID": "previous_preset", "callback": None, "resetCallback": None},
        {"name": "Color Swap", "actionID": "toggle_fg_bg", "callback": None, "resetCallback": None},
        {"name": "Preserve Alpha", "actionID": "preserve_alpha", "callback": None, "resetCallback": None},
        {"name": "Layer Visibility", "actionID": "toggle_layer_visibility", "callback": None, "resetCallback": None},
        {"name": "Undo", "actionID": "edit_undo", "callback": None, "resetCallback": None},
        {"name": "Redo", "actionID": "edit_redo", "callback": None, "resetCallback": None},

        {"name": "Zoom", "actionID": None, "callback": "Zoom", "resetCallback": None},
        {"name": "Rotate Canvas", "actionID": None, "callback": "RotateCanvas", "resetCallback": "RemoveGizmo"},
        {"name": "Brush Size", "actionID": None, "callback": "BrushSize", "resetCallback": "RemoveGizmo"},
        {"name": "Brush Opacity", "actionID": None, "callback": "BrushOpacity", "resetCallback": "RemoveGizmo"},
        {"name": "Brush Flow", "actionID": None, "callback": "BrushFlow", "resetCallback": "RemoveGizmo"},
        {"name": "Layer Opacity", "actionID": None, "callback": "LayerOpacity", "resetCallback": "RemoveGizmo"},
    ]

    h = HelperLib()

    zoomStep = 1/100
    brushSizeStep = 0.2
    paintingOpacityStep = 0.01
    layerOpacityStep = 1
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
            self.gizmo.changeOpacity(view.paintingOpacity() * 255)
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
            self.gizmo.changeOpacity(view.paintingFlow() * 255)
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

    def LayerOpacity( self ):
        self.hidePieMenu()

        cursor = QCursor.pos()

        if self.position == None:
            self.position = cursor
        
        if self.previousPosition == None:
            self.previousPosition = self.position

        view = Krita.instance().activeWindow().activeView()
        canvas = Krita.instance().activeWindow().activeView().canvas()
        res = Krita.instance().activeDocument().resolution()
        currentActiveLayer = Krita.instance().activeDocument().activeNode()
        
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

        alpha = currentActiveLayer.opacity() + self.layerOpacityStep * steps * direction

        if alpha > 255:
            alpha = 255
        elif alpha < 0:
            alpha = 0

        currentActiveLayer.setOpacity( alpha )
        # Next two lines needed to update the canvas, there's a better update method
        # but I can't find it and can't recall it either
        Krita.instance().action('toggle_layer_visibility').trigger()
        Krita.instance().action('toggle_layer_visibility').trigger()

        self.gizmo.changeOpacity( alpha )

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