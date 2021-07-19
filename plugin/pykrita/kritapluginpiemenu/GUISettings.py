from PyQt5.QtCore import pyqtSignal
from krita import *
from PyQt5 import *
from .Options import *
import os
import json
from .Debug import Logger

class GUISettings(QDialog):
  newOptionsReady = pyqtSignal()
  GUISettingsClosed = pyqtSignal()

  def __init__(self, sectionsCnt=None, parent=None):
    # super(GUISettings, self).__init__(parent)
    super().__init__(parent)

    self.GUISettingsActive = False
    
    self.setGeometry(0, 0, 300, 500)
    self.setMinimumSize(400, 500)
    self.setWindowTitle("Pie Menu GUI Settings")

    self.submenuLeftMargin = 20
    
    # Main layout, contains only QScrollArea
    self.base = QVBoxLayout()
    self.base.setContentsMargins(4, 4, 4, 4)
    self.base.setSpacing(0)
    self.scrollArea = QScrollArea()
    self.scrollArea.setWidgetResizable(True)
        
    self.settingsFormLayout = QFormLayout()
    self.settingsFormLayout.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
    self.groupBox = QGroupBox("Pie Menu GUI Settings")
    self.groupBox.setStyleSheet("QGroupBox {font-size: 16px; text-decoration: underline;}")
    self.groupBox.setLayout(self.settingsFormLayout)

    self.settingsFormLayout.addRow( self.addLine() )

    self.sectionsCnt = sectionsCnt

    self.saveButton = QPushButton("Save Settings", self)
    self.saveButton.clicked.connect( lambda: self.saveSettings() )
    self.settingsFormLayout.addRow( self.saveButton )
    
    self.scrollArea.setWidget(self.groupBox)

    self.base.addWidget(self.scrollArea)

    self.setLayout(self.base)
    
    self.options = None
    
    self.loadSettings( self.settingsFormLayout )
    self.displayOptions( self.settingsFormLayout )

  def displayOptions( self, layout ):
    self.addSpinBoxRow("gizmoSizeDefault", "Gizmo Size Default", self.options["gizmoSizeDefault"], 0, 10000, 1, layout)
    layout.addRow( self.addLine() )

    self.addSpinBoxRow("submenuPositionOffset", "Submenu Position Offset", self.options["submenuPositionOffset"], 0, 10, 0.1, layout)
    layout.addRow( self.addLine() )

    self.addSpinBoxRow("wheelInnerRadius", "Wheel Inner Radius", self.options["wheelInnerRadius"], 0, 10000, 1, layout)
    layout.addRow( self.addLine() )

    self.addSpinBoxRow("wheelOuterRadius", "Wheel Outer Radius", self.options["wheelOuterRadius"], 0, 10000, 1, layout)
    layout.addRow( self.addLine() )

    self.addSpinBoxRow("wheelLineThickness", "Wheel Line Thickness", self.options["wheelLineThickness"], 1, 10000, 1, layout)
    layout.addRow( self.addLine() )

    self.addSpinBoxRow("labelRadius", "Label Radius", self.options["labelRadius"], 0, 10000, 1, layout)
    layout.addRow( self.addLine() )

    self.addSpinBoxRow("fontSize", "Font Size", self.options["fontSize"], 0, 10000, 1, layout)
    layout.addRow( self.addLine() )

    self.addSpinBoxRow("labelWidth", "Label Width", self.options["labelWidth"], 0, 10000, 1, layout)
    layout.addRow( self.addLine() )

    self.addSpinBoxRow("labelHeight", "Label Height", self.options["labelHeight"], 0, 10000, 1, layout)
    layout.addRow( self.addLine() )

    self.addRGBARow("wheelColor", "Wheel Color", self.options["wheelColor"].red(), self.options["wheelColor"].green(), self.options["wheelColor"].blue(), self.options["wheelColor"].alpha(), 0, 255, 1, layout)
    layout.addRow( self.addLine() )

    self.addRGBARow("wheelLineColor", "Wheel Line Color", self.options["wheelLineColor"].red(), self.options["wheelLineColor"].green(), self.options["wheelLineColor"].blue(), self.options["wheelLineColor"].alpha(), 0, 255, 1, layout)
    layout.addRow( self.addLine() )

    self.addRGBARow("labelBaseColor", "Label Base Color", self.options["labelBaseColor"][0], self.options["labelBaseColor"][1], self.options["labelBaseColor"][2], self.options["labelBaseColor"][3], 0, 255, 1, layout)
    layout.addRow( self.addLine() )

    self.addRGBARow("labelActiveColor", "Label Active Color", self.options["labelActiveColor"][0], self.options["labelActiveColor"][1], self.options["labelActiveColor"][2], self.options["labelActiveColor"][3], 0, 255, 1, layout)
    layout.addRow( self.addLine() )

  def settingsPaths ( self ):
    paths = {"dirpath": "", "filepath": ""}
    
    dirName = "KritaPMPlugin"
    fileName = "pmguisettings"
    dirpath = os.path.expanduser("~/" + dirName)
    nicepath = os.path.abspath(dirpath)

    paths["dirpath"] = nicepath
    
    filepath = os.path.expanduser("~/" + dirName + "/" + fileName + ".json")
    nicepath = os.path.abspath(filepath)        

    paths["filepath"] = nicepath
    
    return paths

  def writeSettingsFile( self ):
    paths = self.settingsPaths()

    if not os.path.exists(paths["dirpath"]):
      os.mkdir(paths["dirpath"])

    # Convert colors from QColor to array so json can serialize it
    self.options["wheelColor"] = [self.options["wheelColor"].red(), self.options["wheelColor"].green(), self.options["wheelColor"].blue(), self.options["wheelColor"].alpha()]
    self.options["wheelLineColor"] = [self.options["wheelLineColor"].red(), self.options["wheelLineColor"].green(), self.options["wheelLineColor"].blue(), self.options["wheelLineColor"].alpha()]

    with open(paths["filepath"] , "w") as file:
      file.write(json.dumps(self.options))

    # Convert back to QColor for use in Krita
    self.options["wheelColor"] = QColor(self.options["wheelColor"][0], self.options["wheelColor"][1], self.options["wheelColor"][2], self.options["wheelColor"][3])
    self.options["wheelLineColor"] = QColor(self.options["wheelLineColor"][0], self.options["wheelLineColor"][1], self.options["wheelLineColor"][2], self.options["wheelLineColor"][3])

  def readSettingsFile( self ):
    paths = self.settingsPaths()

    # check if directory exists
    if not os.path.exists(paths["dirpath"]) or not os.path.exists(paths["filepath"]):
      return False
      
    with open(paths["filepath"], "r") as file:
      data = file.read()
      
    self.options = json.loads(data)
    
    return True
    
  def loadSettings( self, layout ):
    if not self.readSettingsFile():
      self.options = Options().options

    # Convert int arrays to QColor for use in PyQt
    self.options["wheelColor"] = QColor(self.options["wheelColor"][0], self.options["wheelColor"][1], self.options["wheelColor"][2], self.options["wheelColor"][3])
    self.options["wheelLineColor"] = QColor(self.options["wheelLineColor"][0], self.options["wheelLineColor"][1], self.options["wheelLineColor"][2], self.options["wheelLineColor"][3])

    # self.baseMenuSectionsCombo.setCurrentIndex( len( self.menus["menu"]) )
    
    # self.setMenuItems(self.menus, layout)

    # self.menusChanged.emit()

  def saveSettings( self ):
    # write to file
    self.writeSettingsFile()

  def setOptionsFromSettings( self ):
    parent = self.groupBox
    spinBoxes = parent.findChildren(QSpinBox)
    suffixes = ["_R", "_G", "_B", "_A"]

    for spinBox in spinBoxes:

      # Check if current spinBox is a value of RGBA
      for suffix in suffixes:
        suffixIndex = -1

        if suffix in spinBox.objectName():
          suffixIndex = suffixes.index(suffix)
          break

      # if RGBA
      if suffixIndex > -1:
        # RGBA as a QColor
        if "wheelColor" in spinBox.objectName() or "wheelLineColor" in spinBox.objectName():
          if suffixIndex == 0:
            self.options[spinBox.objectName()[:-2]].setRed( int(spinBox.value()) )
          if suffixIndex == 1:
            self.options[spinBox.objectName()[:-2]].setGreen( int(spinBox.value()) )
          if suffixIndex == 2:
            self.options[spinBox.objectName()[:-2]].setBlue( int(spinBox.value()) )
          if suffixIndex == 3:
            self.options[spinBox.objectName()[:-2]].setAlpha( int(spinBox.value()) )
        # RGBA as a python list
        else:
          self.options[spinBox.objectName()[:-2]][suffixIndex] = int(spinBox.value())
      else:
        # Other options values
        self.options[spinBox.objectName()] = int(spinBox.value())
      
    self.newOptionsReady.emit()

  def onOptionsChanged( self, val ):
    self.setOptionsFromSettings()

  def addLabel(self, label):
    label = QLabel( str(label) )
    label.setStyleSheet( "QLabel {font-size: 12px;}" )
    return label

  def addLineEdit(self, objectName):
    input = QLineEdit()
    input.setObjectName(objectName)
    input.textChanged.connect(self.onOptionsChanged)
    return input

  def addSpinBox(self, objectName, value=0, min=False, max=False, step=False):
    spinBox = QSpinBox()
    spinBox.valueChanged.connect(self.onOptionsChanged)
    spinBox.setObjectName(objectName)

    if min != False or max != False:
      spinBox.setRange(min, max)
    
    if step != False:
      spinBox.setSingleStep(step)

    spinBox.setValue(int(value))

    return spinBox

  def addLine( self ):
    line = QFrame()
    line.setFrameShape(QtWidgets.QFrame.HLine)
    line.setFrameShadow(QtWidgets.QFrame.Sunken)
    line.setLineWidth(1)
    line.setStyleSheet("QFrame {background-color: rgb(112,112,112)}")
    return line

  def addRGBARow(self, objectName, txt, r=0, g=0, b=0, a=0, min=0, max=False, step=1, layout=False):
    layout.addRow( self.addLabel(txt) )
    layout.addRow(  self.addLabel("R"), self.addSpinBox(objectName + "_R", r, min, max, step) )
    layout.addRow(  self.addLabel("G"), self.addSpinBox(objectName + "_G", g, min, max, step) )
    layout.addRow(  self.addLabel("B"), self.addSpinBox(objectName + "_B", b, min, max, step) )
    layout.addRow(  self.addLabel("A"), self.addSpinBox(objectName + "_A", a, min, max, step) )

  def addSpinBoxRow(self, objectName, txt, value=0, min=False, max=False, step=False, layout=False):
    spinBox = self.addSpinBox(objectName, value, min, max, step)

    elms = [ self.addLabel(txt), spinBox ]
    layout.addRow( elms[0], elms[1] )
    return elms

  def addEditableRow(self, objectName, txt, layout):
    # This method can be deleted
    lineEdit = self.addLineEdit(objectName)

    elms = [ self.addLabel(txt), lineEdit ]
    layout.addRow( elms[0], elms[1] )
    return elms

  def accept(self):
    self.GUISettingsClosed.emit()
    super(GUISettings, self).accept()

  def reject(self):
    self.GUISettingsClosed.emit()
    super(GUISettings, self).reject()