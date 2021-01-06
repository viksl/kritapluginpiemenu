from krita import *
from PyQt5 import *
from .HelperLib import *

class ActionsList(QObject):
    hidePieMenuSignal = pyqtSignal()

    actionsList = [
        {"name": "Ellipse Tool", "actionID": "KritaShape/KisToolEllipse", "category": "Tools", "init": None, "callback": None, "resetCallback": None},
        {"name": "Freehand Brush Tool", "actionID": "KritaShape/KisToolBrush", "category": "Tools", "init": None, "callback": None, "resetCallback": None},
        {"name": "Fill Tool", "actionID": "KritaFill/KisToolFill", "category": "Tools", "init": None, "callback": None, "resetCallback": None},
        {"name": "Mirror View", "actionID": "mirror_canvas", "category": "Canvas", "init": None, "callback": None, "resetCallback": None},
        {"name": "Eraser Mode", "actionID": "erase_action", "category": "Brush", "init": None, "callback": None, "resetCallback": None},
        {"name": "Paint Layer", "actionID": "add_new_paint_layer", "category": "Layer", "init": None, "callback": None, "resetCallback": None},
        {"name": "Quick Clipping Group", "actionID": "create_quick_clipping_group", "category": "Layer", "init": None, "callback": None, "resetCallback": None},
        {"name": "Duplicate Layer", "actionID": "duplicatelayer", "category": "Layer", "init": None, "callback": None, "resetCallback": None},
        {"name": "Delete Layer", "actionID": "remove_layer", "category": "Layer", "init": None, "callback": None, "resetCallback": None},
        {"name": "Select Shapes Tool", "actionID": "InteractionTool", "category": "Tools", "init": None, "callback": None, "resetCallback": None},
        {"name": "Text Tool", "actionID": "SvgTextTool", "category": "Tools", "init": None, "callback": None, "resetCallback": None},
        {"name": "Edit Shapes Tool", "actionID": "PathTool", "category": "Tools", "init": None, "callback": None, "resetCallback": None},
        {"name": "Calligraphy", "actionID": "KarbonCalligraphyTool", "category": "Tools", "init": None, "callback": None, "resetCallback": None},
        {"name": "Line Tool", "actionID": "KritaShape/KisToolLine", "category": "Tools", "init": None, "callback": None, "resetCallback": None},
        {"name": "Rectangle Tool", "actionID": "KritaShape/KisToolRectangle", "category": "Tools", "init": None, "callback": None, "resetCallback": None},
        {"name": "Ellipse Tool", "actionID": "KritaShape/KisToolEllipse", "category": "Tools", "init": None, "callback": None, "resetCallback": None},
        {"name": "Polygon Tool", "actionID": "KisToolPolygon", "category": "Tools", "init": None, "callback": None, "resetCallback": None},
        {"name": "Polyline Tool", "actionID": "KisToolPolyline", "category": "Tools", "init": None, "callback": None, "resetCallback": None},
        {"name": "Bezier Curve Tool", "actionID": "KisToolPath", "category": "Tools", "init": None, "callback": None, "resetCallback": None},
        {"name": "Freehand Path Tool", "actionID": "KisToolPencil", "category": "Tools", "init": None, "callback": None, "resetCallback": None},
        {"name": "Dynamic Brush Tool", "actionID": "KritaShape/KisToolDyna", "category": "Tools", "init": None, "callback": None, "resetCallback": None},
        {"name": "Multibrush Tool", "actionID": "KritaShape/KisToolMultiBrush", "category": "Tools", "init": None, "callback": None, "resetCallback": None},
        {"name": "Transform Tool", "actionID": "KisToolTransform", "category": "Tools", "init": None, "callback": None, "resetCallback": None},
        {"name": "Move Tool", "actionID": "KritaTransform/KisToolMove", "category": "Tools", "init": None, "callback": None, "resetCallback": None},
        {"name": "Crop Tool", "actionID": "KisToolCrop", "category": "Tools", "init": None, "callback": None, "resetCallback": None},
        {"name": "Gradient Tool", "actionID": "KritaFill/KisToolGradient", "category": "Tools", "init": None, "callback": None, "resetCallback": None},
        {"name": "Color Picker", "actionID": "KritaSelected/KisToolColorPicker", "category": "Tools", "init": None, "callback": None, "resetCallback": None},
        {"name": "Colorize Mask Tool", "actionID": "KritaShape/KisToolLazyBrush", "category": "Tools", "init": None, "callback": None, "resetCallback": None},
        {"name": "Smart Patch Tool", "actionID": "KritaShape/KisToolSmartPatch", "category": "Tools", "init": None, "callback": None, "resetCallback": None},
        {"name": "Assistant Tool", "actionID": "KisAssistantTool", "category": "Tools", "init": None, "callback": None, "resetCallback": None},
        {"name": "Measurement Tool", "actionID": "KritaShape/KisToolMeasure", "category": "Tools", "init": None, "callback": None, "resetCallback": None},
        {"name": "Reference Images Tool", "actionID": "ToolReferenceImages", "category": "Tools", "init": None, "callback": None, "resetCallback": None},
        {"name": "Rectangular Selection Tool", "actionID": "KisToolSelectRectangular", "category": "Tools", "init": None, "callback": None, "resetCallback": None},
        {"name": "Elliptical Selection Tool", "actionID": "KisToolSelectElliptical", "category": "Tools", "init": None, "callback": None, "resetCallback": None},
        {"name": "Polygonal Selection Tool", "actionID": "KisToolSelectPolygonal", "category": "Tools", "init": None, "callback": None, "resetCallback": None},
        {"name": "Outline Selection Tool", "actionID": "KisToolSelectOutline", "category": "Tools", "init": None, "callback": None, "resetCallback": None},
        {"name": "Contiguous Selection Tool", "actionID": "KisToolSelectContiguous", "category": "Tools", "init": None, "callback": None, "resetCallback": None},
        {"name": "Similar Color Selection Tool", "actionID": "KisToolSelectSimilar", "category": "Tools", "init": None, "callback": None, "resetCallback": None},
        {"name": "Bezier Curve Selection Tool", "actionID": "KisToolSelectPath", "category": "Tools", "init": None, "callback": None, "resetCallback": None},
        {"name": "Magnetic Selection Tool", "actionID": "KisToolSelectMagnetic", "category": "Tools", "init": None, "callback": None, "resetCallback": None},
        {"name": "Zoom Tool", "actionID": "ZoomTool", "category": "Tools", "init": None, "callback": None, "resetCallback": None},
        {"name": "Pan Tool", "actionID": "PanTool", "category": "Tools", "init": None, "callback": None, "resetCallback": None},
        {"name": "Transparency Mask", "actionID": "add_new_transparency_mask", "category": "Layer", "init": None, "callback": None, "resetCallback": None},
        {"name": "Filter Mask", "actionID": "add_new_filter_mask", "category": "Layer", "init": None, "callback": None, "resetCallback": None},
        {"name": "Colorize Mask", "actionID": "add_new_colorize_mask", "category": "Layer", "init": None, "callback": None, "resetCallback": None},
        {"name": "Previous Preset", "actionID": "previous_preset", "category": "Brush", "init": None, "callback": None, "resetCallback": None},
        {"name": "Color Swap", "actionID": "toggle_fg_bg", "category": "Brush", "init": None, "callback": None, "resetCallback": None},
        {"name": "Preserve Alpha", "actionID": "preserve_alpha", "category": "Brush", "init": None, "callback": None, "resetCallback": None},
        {"name": "Layer Visibility", "actionID": "toggle_layer_visibility", "category": "Layer", "init": None, "callback": None, "resetCallback": None},
        {"name": "Undo", "actionID": "edit_undo", "category": "Miscellaneous", "init": None, "callback": None, "resetCallback": None},
        {"name": "Redo", "actionID": "edit_redo", "category": "Miscellaneous", "init": None, "callback": None, "resetCallback": None},
        {"name": "Deselect", "actionID": "deselect", "category": "Miscellaneous", "init": None, "callback": None, "resetCallback": None},
        {"name": "Select All", "actionID": "select_all", "category": "Miscellaneous", "init": None, "callback": None, "resetCallback": None},
        {"name": "Invert Selection", "actionID": "invert_selection", "category": "Miscellaneous", "init": None, "callback": None, "resetCallback": None},
        {"name": "Save File", "actionID": "file_save", "category": "Miscellaneous", "init": None, "callback": None, "resetCallback": None},
        {"name": "No Brush Smooth", "actionID": "set_no_brush_smoothing", "category": "Brush", "init": None, "callback": None, "resetCallback": None},
        {"name": "Basic Brush Smooth", "actionID": "set_simple_brush_smoothing", "category": "Brush", "init": None, "callback": None, "resetCallback": None},
        {"name": "Weighted Brush Smooth", "actionID": "set_weighted_brush_smoothing", "category": "Brush", "init": None, "callback": None, "resetCallback": None},
        {"name": "Stabilizer Brush Smooth", "actionID": "set_stabilizer_brush_smoothing", "category": "Brush", "init": None, "callback": None, "resetCallback": None},
        {"name": "Fill - F Color", "actionID": "fill_selection_foreground_color", "category": "Miscellaneous", "init": None, "callback": None, "resetCallback": None},
        {"name": "Fill - B Color", "actionID": "fill_selection_background_color", "category": "Miscellaneous", "init": None, "callback": None, "resetCallback": None},
        {"name": "Fill - Pattern", "actionID": "fill_selection_pattern", "category": "Miscellaneous", "init": None, "callback": None, "resetCallback": None},
        {"name": "Select Opaque", "actionID": "selectopaque", "category": "Layer", "init": None, "callback": None, "resetCallback": None},

        {"name": "Isolate Layer", "actionID": None, "category": "Layer", "init": None, "callback": None, "resetCallback": "IsolateLayer"},
        {"name": "Color Selector", "actionID": None, "category": "Miscellaneous", "init": None, "callback": None, "resetCallback": "ColorSelector"},
        {"name": "Confirm Transform", "actionID": None, "category": "Miscellaneous", "init": None, "callback": None, "resetCallback": "ConfirmTransform"},
        {"name": "Reset Transform", "actionID": None, "category": "Miscellaneous", "init": None, "callback": None, "resetCallback": "ResetTransform"},
        {"name": "Reset Transform (Deselect)", "actionID": None, "category": "Miscellaneous", "init": None, "callback": None, "resetCallback": "ResetTransformWithDeselect"},
        {"name": "Zoom (c)", "actionID": None, "category": "Canvas", "init": "InitZoom", "callback": "Zoom", "resetCallback": None},
        {"name": "Rotate Canvas (c)", "actionID": None, "category": "Canvas", "init": "InitCanvasRotation", "callback": "RotateCanvas", "resetCallback": None},
        {"name": "Brush Size (c)", "actionID": None, "category": "Brush", "init": "InitBrushSize", "callback": "BrushSize", "resetCallback": None},
        {"name": "Brush Opacity (c)", "actionID": None, "category": "Brush", "init": "InitBrushOpacity", "callback": "BrushOpacity", "resetCallback": None},
        {"name": "Brush Flow (c)", "actionID": None, "category": "Brush", "init": "InitBrushFlow", "callback": "BrushFlow", "resetCallback": None},
        {"name": "Layer Opacity (c)", "actionID": None, "category": "Layer", "init": "InitLayerOpacity", "callback": "LayerOpacity", "resetCallback": None},
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

        self.gizmoSizeDefault = 10
        self.maxBrushSize = int(Application.readSetting("", "maximumBrushSize", ""))

    def Init( self, gizmo=None ):
        self.position = None
        self.previousPosition = None
        self.angle = None
        self.initDistanceTravelled = None
        self.initOffsetAngle = None
        self.hidePieMenuSignalEmitted = False
        self.distancePassed = False

        if gizmo is not None:
            self.gizmo = gizmo

    def ConfirmTransform( self ):

        # Get ToolBox
        for docker in Krita.instance().dockers():
            if docker.objectName() == "ToolBox":
                break

        tools = docker.findChildren(QToolButton)

        # Get the active tool
        for tool in tools:
            if tool.isChecked():
                break

        if tool.objectName() != "KisToolTransform":
            return

        ############################################################
        # Get the transform tool options accept and cancel buttons
        ############################################################
        buttons = {"apply": None, "reset": None}

        # Get Tool Options
        for docker in Krita.instance().dockers():
            if docker.objectName() == "sharedtooldocker":
                break
                
        # Get apply or reset (or any other button I assume)
        # still no info which is which here
        # This part could be omitted, only one of the children is needed
        # to get the parent later, I'm keeping this as a 2 way
        # check since apply and reset seem to be the only ones with
        # empty objectName
        for button in docker.findChildren(QPushButton):
            if button.objectName() == "":
                break

        # Get apply and/or reset button - this way you avoid translation problems with button.text()
        for button in button.parent().buttons():
            if button.parent().buttonRole(button) == QDialogButtonBox.ApplyRole:
                buttons["apply"] = button
                break

        buttons["apply"].click()

    def ResetTransform( self ):

        # Get ToolBox
        for docker in Krita.instance().dockers():
            if docker.objectName() == "ToolBox":
                break

        tools = docker.findChildren(QToolButton)

        # Get the active tool
        for tool in tools:
            if tool.isChecked():
                break

        if tool.objectName() != "KisToolTransform":
            return

        ############################################################
        # Get the transform tool options accept and cancel buttons
        ############################################################
        buttons = {"apply": None, "reset": None}

        # Get Tool Options
        for docker in Krita.instance().dockers():
            if docker.objectName() == "sharedtooldocker":
                break
                
        # Get apply or reset (or any other button I assume)
        # still no info which is which here
        for button in docker.findChildren(QPushButton):
            if button.objectName() == "":
                break

        # Get apply and/or reset button - this way you avoid translation problems with button.text()
        for button in button.parent().buttons():
            if button.parent().buttonRole(button) == QDialogButtonBox.ResetRole:
                buttons["reset"] = button
                break

        buttons["reset"].click()

    def ResetTransformWithDeselect( self ):

        # Get ToolBox
        for docker in Krita.instance().dockers():
            if docker.objectName() == "ToolBox":
                break

        tools = docker.findChildren(QToolButton)

        # Get the active tool
        for tool in tools:
            if tool.isChecked():
                break

        if tool.objectName() != "KisToolTransform":
            return

        ############################################################
        # Get the transform tool options accept and cancel buttons
        ############################################################
        buttons = {"apply": None, "reset": None}

        # Get Tool Options
        for docker in Krita.instance().dockers():
            if docker.objectName() == "sharedtooldocker":
                break
                
        # Get apply or reset (or any other button I assume)
        # still no info which is which here
        for button in docker.findChildren(QPushButton):
            if button.objectName() == "":
                break

        # Get apply and/or reset button - this way you avoid translation problems with button.text()
        for button in button.parent().buttons():
            if button.parent().buttonRole(button) == QDialogButtonBox.ResetRole:
                buttons["reset"] = button
                break

        buttons["reset"].click()
        
        Krita.instance().action("deselect").trigger()

    def IsolateLayer( self ):
        action = Krita.instance().action( "isolate_active_layer" )
        action.setAutoRepeat(False)
        action.trigger()

    def ColorSelector( self ):
        action = Krita.instance().action( "show_color_selector" )
        action.setAutoRepeat(False)
        QTimer.singleShot(100, action.trigger)

    def InitZoom(self, gizmo):
        self.Init()
        self.hidePieMenu()

        cursor = QCursor.pos()

        if self.position == None:
            self.position = cursor
        
        if self.previousPosition == None:
            self.previousPosition = self.position

    def InitCanvasRotation(self, gizmo):
        self.gizmo = gizmo        
        self.Init()

        self.hidePieMenu()

        canvas = Krita.instance().activeWindow().activeView().canvas()

        if self.position == None:
            self.position = QCursor.pos()

        if self.angle == None:
             self.angle = canvas.rotation()

        if self.gizmo.enabled == False:
            self.gizmo.setProperties({"radius": self.gizmoSizeDefault *2, "position": self.position, "alpha": 255})

    def InitBrushSize(self, gizmo):
        self.gizmo = gizmo
        self.Init()

        self.hidePieMenu()

        cursor = QCursor.pos()

        if self.position == None:
            self.position = cursor
        
        if self.previousPosition == None:
            self.previousPosition = self.position

        view = Krita.instance().activeWindow().activeView()
        canvas = view.canvas()
        res = Krita.instance().activeDocument().resolution()
        
        zoom = canvas.zoomLevel() * self.baseDPI / res

        if self.gizmo.enabled == False:
            self.gizmo.setProperties({"radius": view.brushSize() * zoom, "position": self.position, "alpha": 255})

    def InitBrushOpacity(self, gizmo):
        self.gizmo = gizmo
        self.Init()

        self.hidePieMenu()

        cursor = QCursor.pos()

        if self.position == None:
            self.position = cursor
        
        if self.previousPosition == None:
            self.previousPosition = self.position

        view = Krita.instance().activeWindow().activeView()
        canvas = view.canvas()
        res = Krita.instance().activeDocument().resolution()
        
        zoom = canvas.zoomLevel() * self.baseDPI / res

        if self.gizmo.enabled == False:
            self.gizmo.setProperties({"radius": view.brushSize() * zoom, "position": self.position, "alpha": view.paintingOpacity() * 255})

    def InitLayerOpacity(self, gizmo):
        self.gizmo = gizmo
        self.Init()

        self.hidePieMenu()

        cursor = QCursor.pos()

        if self.position == None:
            self.position = cursor
        
        if self.previousPosition == None:
            self.previousPosition = self.position

        view = Krita.instance().activeWindow().activeView()
        canvas = view.canvas()
        res = Krita.instance().activeDocument().resolution()
        
        zoom = canvas.zoomLevel() * self.baseDPI / res
        currentActiveLayer = Krita.instance().activeDocument().activeNode()

        if self.gizmo.enabled == False:
            self.gizmo.setProperties({"radius": view.brushSize() * zoom, "position": self.position, "alpha": currentActiveLayer.opacity()})

    def InitBrushFlow(self, gizmo):
        self.gizmo = gizmo
        self.Init()

        self.hidePieMenu()

        cursor = QCursor.pos()

        if self.position == None:
            self.position = cursor
        
        if self.previousPosition == None:
            self.previousPosition = self.position

        view = Krita.instance().activeWindow().activeView()
        canvas = view.canvas()
        res = Krita.instance().activeDocument().resolution()
        
        zoom = canvas.zoomLevel() * self.baseDPI / res

        if self.gizmo.enabled == False:
            self.gizmo.setProperties({"radius": view.brushSize() * zoom, "position": self.position, "alpha": view.paintingFlow() * 255})
        
    def Zoom( self ):
        cursor = QCursor.pos()

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
        self.initDistanceTravelled = self.h.twoPointDistance(self.position, QCursor.pos())

        if self.initDistanceTravelled != None and self.initDistanceTravelled < self.gizmoSizeDefault:
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
        
        canvas = Krita.instance().activeWindow().activeView().canvas()
        canvas.setRotation(self.angle - self.initOffsetAngle + self.h.vectorAngle(v1, v2))

    def BrushSize( self ):
        direction = 1
        steps = 0
        cursor = QCursor.pos()

        if cursor.x() == self.previousPosition.x() or abs( self.previousPosition.x() - cursor.x() ) < 2:
            return

        if self.previousPosition.x() - cursor.x() > 0:
            direction = -1

        steps = int( abs( self.previousPosition.x() - cursor.x() ) )

        view = Krita.instance().activeWindow().activeView()
        canvas = view.canvas()
        res = Krita.instance().activeDocument().resolution()
        
        zoom = canvas.zoomLevel() * self.baseDPI / res

        size = view.brushSize() + self.brushSizeStep * steps * direction

        if size < 0.01:
            size = 0.01
        elif size > self.maxBrushSize:
            size = self.maxBrushSize

        view.setBrushSize( size )

        self.gizmo.setProperties({"radius": size * zoom})

        self.previousPosition = cursor

    def BrushOpacity( self ):
        cursor = QCursor.pos()
        direction = 1
        steps = 0

        if cursor.x() == self.previousPosition.x() or abs( self.previousPosition.x() - cursor.x() ) < 2:
            return

        if self.previousPosition.x() - cursor.x() > 0:
            direction = -1

        steps = int( abs( self.previousPosition.x() - cursor.x() ) )

        view = Krita.instance().activeWindow().activeView()

        alpha = view.paintingOpacity() + self.paintingOpacityStep * steps * direction

        if alpha > 1:
            alpha = 1
        elif alpha < 0:
            alpha = 0

        view.setPaintingOpacity( alpha )

        self.gizmo.setProperties({"alpha": alpha * 255})

        self.previousPosition = cursor

    def BrushFlow( self ):
        cursor = QCursor.pos()
        direction = 1
        steps = 0

        if cursor.x() == self.previousPosition.x() or abs( self.previousPosition.x() - cursor.x() ) < 2:
            return

        if self.previousPosition.x() - cursor.x() > 0:
            direction = -1

        steps = int( abs( self.previousPosition.x() - cursor.x() ) )

        view = Krita.instance().activeWindow().activeView()
        
        alpha = view.paintingFlow() + self.paintingFlowStep * steps * direction

        if alpha > 1:
            alpha = 1
        elif alpha < 0:
            alpha = 0

        view.setPaintingFlow( alpha )

        self.gizmo.setProperties({"alpha": alpha * 255})

        self.previousPosition = cursor

    def LayerOpacity( self ):
        cursor = QCursor.pos()
        direction = 1
        steps = 0

        if cursor.x() == self.previousPosition.x() or abs( self.previousPosition.x() - cursor.x() ) < 2:
            return

        if self.previousPosition.x() - cursor.x() > 0:
            direction = -1

        steps = int( abs( self.previousPosition.x() - cursor.x() ) )

        currentActiveLayer = Krita.instance().activeDocument().activeNode()

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

        self.gizmo.setProperties({"alpha": alpha})

        self.previousPosition = cursor

    def hidePieMenu( self ):
        if not self.hidePieMenuSignalEmitted:
            self.hidePieMenuSignalEmitted = True
            self.hidePieMenuSignal.emit()