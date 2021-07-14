from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIntValidator
from krita import *
from PyQt5 import *
from .Settings import CustomComboBox
from .Options import *
import os
import json
from .Debug import Logger

class GUISettings(QDialog):
  optionsChanged = pyqtSignal()
  openPieMenu = pyqtSignal()
  closePieMenu = pyqtSignal()

  def __init__(self, sectionsCnt=None, parent=None):
    # super(GUISettings, self).__init__(parent)
    super().__init__(parent)

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
    self.logger = Logger()
    self.loadSettings( self.settingsFormLayout )

    self.addSpinBoxRow("TestName", "test text int", 0, 255, 1, self.settingsFormLayout)
    self.logger.print("Test init GUI")
    self.openPieMenu.emit()


  def settingsPaths (self ):
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

    self.openPieMenu.emit()
    self.optionsChanged.emit()

  def onOptionsChanged( self, val ):
    self.logger.print("Options Changed " + str(val))

  def addLabel(self, label):
    label = QLabel( str(label) )
    label.setStyleSheet( "QLabel {font-size: 12px;}" )
    return label

  def addLineEdit(self, objectName):
    input = QLineEdit()
    input.setObjectName(objectName)
    input.textChanged.connect(self.onOptionsChanged)
    return input

  def addSpinBox(self, objectName, min, max, step):
    spinBox = QSpinBox()
    spinBox.valueChanged.connect(self.onOptionsChanged)
    spinBox.setObjectName(objectName)
    spinBox.setRange(min, max)
    spinBox.setSingleStep(step)
    self.logger.print("Inside")
    return spinBox

  def addLine( self ):
    line = QFrame()
    line.setFrameShape(QtWidgets.QFrame.HLine)
    line.setFrameShadow(QtWidgets.QFrame.Sunken)
    line.setLineWidth(1)
    line.setStyleSheet("QFrame {background-color: rgb(112,112,112)}")
    return line

  def addSpinBoxRow(self, objectName, txt, min, max, step, layout):
    spinBox = self.addSpinBox(objectName, min, max, step)

    elms = [ self.addLabel(txt), spinBox ]
    layout.addRow( elms[0], elms[1] )
    return elms

  def addEditableRow(self, objectName, txt, layout):
    lineEdit = self.addLineEdit(objectName)

    elms = [ self.addLabel(txt), lineEdit ]
    layout.addRow( elms[0], elms[1] )
    return elms

  def accept(self):
    self.closePieMenu.emit()
    super(GUISettings, self).accept()

  def reject(self):
    self.closePieMenu.emit()
    super(GUISettings, self).reject()