from krita import *
from PyQt5 import *
from .HelperLib import *

class ActionsList(QObject):
    hidePieMenuSignal = pyqtSignal()

    actionsList = [
        {"name": "Ellipse Tool", "actionID": "KritaShape/KisToolEllipse", "category": "Tools", "callback": None, "resetCallback": None},
        {"name": "Freehand Brush Tool", "actionID": "KritaShape/KisToolBrush", "category": "Tools", "callback": None, "resetCallback": None},
        {"name": "Fill Tool", "actionID": "KritaFill/KisToolFill", "category": "Tools", "callback": None, "resetCallback": None},
        {"name": "Mirror View", "actionID": "mirror_canvas", "category": "Canvas", "callback": None, "resetCallback": None},
        {"name": "Eraser Mode", "actionID": "erase_action", "category": "Brush", "callback": None, "resetCallback": None},
        {"name": "Paint Layer", "actionID": "add_new_paint_layer", "category": "Layer", "callback": None, "resetCallback": None},
        {"name": "Quick Clipping Group", "actionID": "create_quick_clipping_group", "category": "Layer", "callback": None, "resetCallback": None},
        {"name": "Duplicate Layer", "actionID": "duplicatelayer", "category": "Layer", "callback": None, "resetCallback": None},
        {"name": "Delete Layer", "actionID": "remove_layer", "category": "Layer", "callback": None, "resetCallback": None},
        {"name": "Select Shapes Tool", "actionID": "InteractionTool", "category": "Tools", "callback": None, "resetCallback": None},
        {"name": "Text Tool", "actionID": "SvgTextTool", "category": "Tools", "callback": None, "resetCallback": None},
        {"name": "Edit Shapes Tool", "actionID": "PathTool", "category": "Tools", "callback": None, "resetCallback": None},
        {"name": "Calligraphy", "actionID": "KarbonCalligraphyTool", "category": "Tools", "callback": None, "resetCallback": None},
        {"name": "Line Tool", "actionID": "KritaShape/KisToolLine", "category": "Tools", "callback": None, "resetCallback": None},
        {"name": "Rectangle Tool", "actionID": "KritaShape/KisToolRectangle", "category": "Tools", "callback": None, "resetCallback": None},
        {"name": "Ellipse Tool", "actionID": "KritaShape/KisToolEllipse", "category": "Tools", "callback": None, "resetCallback": None},
        {"name": "Polygon Tool", "actionID": "KisToolPolygon", "category": "Tools", "callback": None, "resetCallback": None},
        {"name": "Polyline Tool", "actionID": "KisToolPolyline", "category": "Tools", "callback": None, "resetCallback": None},
        {"name": "Bezier Curve Tool", "actionID": "KisToolPath", "category": "Tools", "callback": None, "resetCallback": None},
        {"name": "Freehand Path Tool", "actionID": "KisToolPencil", "category": "Tools", "callback": None, "resetCallback": None},
        {"name": "Dynamic Brush Tool", "actionID": "KritaShape/KisToolDyna", "category": "Tools", "callback": None, "resetCallback": None},
        {"name": "Multibrush Tool", "actionID": "KritaShape/KisToolMultiBrush", "category": "Tools", "callback": None, "resetCallback": None},
        {"name": "Transform Tool", "actionID": "KisToolTransform", "category": "Tools", "callback": None, "resetCallback": None},
        {"name": "Move Tool", "actionID": "KritaTransform/KisToolMove", "category": "Tools", "callback": None, "resetCallback": None},
        {"name": "Crop Tool", "actionID": "KisToolCrop", "category": "Tools", "callback": None, "resetCallback": None},
        {"name": "Gradient Tool", "actionID": "KritaFill/KisToolGradient", "category": "Tools", "callback": None, "resetCallback": None},
        {"name": "Color Picker", "actionID": "KritaSelected/KisToolColorPicker", "category": "Tools", "callback": None, "resetCallback": None},
        {"name": "Colorize Mask Tool", "actionID": "KritaShape/KisToolLazyBrush", "category": "Tools", "callback": None, "resetCallback": None},
        {"name": "Smart Patch Tool", "actionID": "KritaShape/KisToolSmartPatch", "category": "Tools", "callback": None, "resetCallback": None},
        {"name": "Assistant Tool", "actionID": "KisAssistantTool", "category": "Tools", "callback": None, "resetCallback": None},
        {"name": "Measurement Tool", "actionID": "KritaShape/KisToolMeasure", "category": "Tools", "callback": None, "resetCallback": None},
        {"name": "Reference Images Tool", "actionID": "ToolReferenceImages", "category": "Tools", "callback": None, "resetCallback": None},
        {"name": "Rectangular Selection Tool", "actionID": "KisToolSelectRectangular", "category": "Tools", "callback": None, "resetCallback": None},
        {"name": "Elliptical Selection Tool", "actionID": "KisToolSelectElliptical", "category": "Tools", "callback": None, "resetCallback": None},
        {"name": "Polygonal Selection Tool", "actionID": "KisToolSelectPolygonal", "category": "Tools", "callback": None, "resetCallback": None},
        {"name": "Outline Selection Tool", "actionID": "KisToolSelectOutline", "category": "Tools", "callback": None, "resetCallback": None},
        {"name": "Contiguous Selection Tool", "actionID": "KisToolSelectContiguous", "category": "Tools", "callback": None, "resetCallback": None},
        {"name": "Similar Color Selection Tool", "actionID": "KisToolSelectSimilar", "category": "Tools", "callback": None, "resetCallback": None},
        {"name": "Bezier Curve Selection Tool", "actionID": "KisToolSelectPath", "category": "Tools", "callback": None, "resetCallback": None},
        {"name": "Magnetic Selection Tool", "actionID": "KisToolSelectMagnetic", "category": "Tools", "callback": None, "resetCallback": None},
        {"name": "Zoom Tool", "actionID": "ZoomTool", "category": "Tools", "callback": None, "resetCallback": None},
        {"name": "Pan Tool", "actionID": "PanTool", "category": "Tools", "callback": None, "resetCallback": None},
        {"name": "Transparency Mask", "actionID": "add_new_transparency_mask", "category": "Layer", "callback": None, "resetCallback": None},
        {"name": "Filter Mask", "actionID": "add_new_filter_mask", "category": "Layer", "callback": None, "resetCallback": None},
        {"name": "Colorize Mask", "actionID": "add_new_colorize_mask", "category": "Layer", "callback": None, "resetCallback": None},
        {"name": "Previous Preset", "actionID": "previous_preset", "category": "Brush", "callback": None, "resetCallback": None},
        {"name": "Color Swap", "actionID": "toggle_fg_bg", "category": "Brush", "callback": None, "resetCallback": None},
        {"name": "Preserve Alpha", "actionID": "preserve_alpha", "category": "Brush", "callback": None, "resetCallback": None},
        {"name": "Layer Visibility", "actionID": "toggle_layer_visibility", "category": "Layer", "callback": None, "resetCallback": None},
        {"name": "Undo", "actionID": "edit_undo", "category": "Misc", "callback": None, "resetCallback": None},
        {"name": "Redo", "actionID": "edit_redo", "category": "Misc", "callback": None, "resetCallback": None},
        {"name": "Deselect", "actionID": "deselect", "category": "Misc", "callback": None, "resetCallback": None},
        {"name": "Select All", "actionID": "select_all", "category": "Misc", "callback": None, "resetCallback": None},
        {"name": "Invert Selection", "actionID": "invert_selection", "category": "Misc", "callback": None, "resetCallback": None},
        {"name": "Save File", "actionID": "file_save", "category": "Misc", "callback": None, "resetCallback": None},
        {"name": "No Brush Smooth", "actionID": "set_no_brush_smoothing", "category": "Brush", "callback": None, "resetCallback": None},
        {"name": "Basic Brush Smooth", "actionID": "set_simple_brush_smoothing", "category": "Brush", "callback": None, "resetCallback": None},
        {"name": "Weighted Brush Smooth", "actionID": "set_weighted_brush_smoothing", "category": "Brush", "callback": None, "resetCallback": None},
        {"name": "Stabilizer Brush Smooth", "actionID": "set_stabilizer_brush_smoothing", "category": "Brush", "callback": None, "resetCallback": None},
        {"name": "Fill - F Color", "actionID": "fill_selection_foreground_color", "category": "Misc", "callback": None, "resetCallback": None},
        {"name": "Fill - B Color", "actionID": "fill_selection_background_color", "category": "Misc", "callback": None, "resetCallback": None},
        {"name": "Fill - Pattern", "actionID": "fill_selection_pattern", "category": "Misc", "callback": None, "resetCallback": None},
        {"name": "Select Opaque", "actionID": "selectopaque", "category": "Misc", "callback": None, "resetCallback": None},
        {"name": "Isolate Layer", "actionID": "isolate_active_layer", "category": "Layer", "callback": None, "resetCallback": None},

        {"name": "Color Selector (c)", "actionID": None, "category": "Misc", "callback": None, "resetCallback": "ColorSelector"},
        {"name": "Zoom (c)", "actionID": None, "category": "Canvas", "callback": "Zoom", "resetCallback": None},
        {"name": "Rotate Canvas (c)", "actionID": None, "category": "Canvas", "callback": "RotateCanvas", "resetCallback": "RemoveGizmo"},
        {"name": "Brush Size (c)", "actionID": None, "category": "Brush", "callback": "BrushSize", "resetCallback": "RemoveGizmo"},
        {"name": "Brush Opacity (c)", "actionID": None, "category": "Brush", "callback": "BrushOpacity", "resetCallback": "RemoveGizmo"},
        {"name": "Brush Flow (c)", "actionID": None, "category": "Brush", "callback": "BrushFlow", "resetCallback": "RemoveGizmo"},
        {"name": "Layer Opacity (c)", "actionID": None, "category": "Layer", "callback": "LayerOpacity", "resetCallback": "RemoveGizmo"},
    ]

    h = HelperLib()

    zoomStep = 1/100                # TWEAK: ZOOM action's sensitivity
    brushSizeStep = 0.2             # TWEAK: BRUSH SIZE action's sensitivity
    paintingOpacityStep = 0.01      # TWEAK: BRUSH OPACITY action's sensitivity
    paintingFlowStep = 0.01         # TWEAK: BRUSH FLOW action's sensitivity
    layerOpacityStep = 1            # TWEAK: LAYER OPACITY action's sensitivity

    """
        Don't touch baseVector and baseDPI
    """
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
        self.distancePassed = False

    def ColorSelector( self ):
        action = Krita.instance().action( "show_color_selector" )
        action.setAutoRepeat(False)
        action.trigger()
        
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

        gizmoSize = 10
        canvas = Krita.instance().activeWindow().activeView().canvas()

        if self.position == None:
            self.position = QCursor.pos()

        if self.angle == None:
             self.angle = canvas.rotation()

        if self.gizmo == None:
            self.gizmo = GizmoIcon(self.position, gizmoSize, gizmoSize, self.parent())
            self.gizmo.showAt(self.position)

        self.initDistanceTravelled = self.h.twoPointDistance(self.position, QCursor.pos())

        if self.initDistanceTravelled != None and self.initDistanceTravelled < gizmoSize:
            if self.distancePassed:
                Krita.instance().action('reset_canvas_rotation').trigger()
            return

        if not self.distancePassed:
            self.distancePassed = True

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
            self.gizmo.changeSize(view.brushSize() * zoom)
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
            self.gizmo.changeSize(view.brushSize() * zoom)
            self.gizmo.changeOpacity(view.paintingFlow() * 255)
            self.gizmo.show()

        direction = 1
        steps = 0

        if cursor.x() == self.previousPosition.x() or abs( self.previousPosition.x() - cursor.x() ) < 2:
            return

        if self.previousPosition.x() - cursor.x() > 0:
            direction = -1

        steps = int( abs( self.previousPosition.x() - cursor.x() ) )

        alpha = view.paintingFlow() + self.paintingFlowStep * steps * direction

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