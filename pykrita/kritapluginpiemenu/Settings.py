from krita import *
from PyQt5 import *
import os
import json

class Dialog(QDialog):
  def __init__(self, text, parent=None):
      super(Dialog, self).__init__(parent)
      self.setLayout(QVBoxLayout())
      self.label = QLabel(str(text))
      self.layout().addWidget(self.label)
      self.resize(200, 50)
      self.exec_()

class CustomComboBox (QComboBox):
  def __init__(self, parent=None):
    super(CustomComboBox, self).__init__(parent)    
    self.setStyleSheet("QComboBox:disabled"
                        "{"
                        "color: lightgreen;"
                        "}")

  def wheelEvent(self, event):
    pass

class Settings(QDialog):
  menusChanged = pyqtSignal()

  def __init__(self, actionsList, parent=None):
    super(Settings, self).__init__(parent)

    self.setGeometry(0, 0, 300, 500)
    self.setMinimumSize(400, 500)
    self.setWindowTitle("Pie Menu Settings")

    self.submenuLeftMargin = 20
    
    # Main layout, contains only QScrollArea
    self.base = QVBoxLayout()
    self.base.setContentsMargins(4, 4, 4, 4)
    self.base.setSpacing(0)
    self.scrollArea = QScrollArea()
    self.scrollArea.setWidgetResizable(True)
        
    self.settingsFormLayout = QFormLayout()
    self.settingsFormLayout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
    self.groupBox = QGroupBox("Pie Menu Settings")
    self.groupBox.setStyleSheet("QGroupBox {font-size: 16px; text-decoration: underline;}")
    self.groupBox.setLayout(self.settingsFormLayout)

    self.sectionsMaxCount = 10

    self.baseMenuSectionsCombo = self.addComboRow("Sections:", self.sectionsMaxCount, self.settingsFormLayout)[1]
    self.baseMenuSectionsCombo.currentIndexChanged.connect( lambda: self.menuAddSections(self.settingsFormLayout, False) )

    self.settingsFormLayout.addRow( self.addLine() )
    
    self.actionsList = actionsList.actionsList
    
    self.menus = {
      "menu": [],
       "submenus": {}
    }

    self.defaultMenus = {
      "menu": [
        {"name": "Select Opaque", "actionID": "selectopaque", "isSubmenu": False, "ref": None, "callback": None, "resetCallback": None},
        {"name": "Undo", "actionID": "edit_undo", "isSubmenu": False, "ref": None, "callback": None, "resetCallback": None},
        {"name": "Previous Preset", "actionID": "previous_preset", "isSubmenu": False, "ref": None, "callback": None, "resetCallback": None},
        {"name": "Outline Selection Tool", "actionID": "KisToolSelectOutline", "isSubmenu": False, "ref": None, "callback": None, "resetCallback": None}
      ],
      "submenus": {}
    }

    self.saveButton = QPushButton("Save Settings", self)
    self.saveButton.clicked.connect( lambda: self.saveSettings(self.settingsFormLayout, self.actionsList) )
    self.settingsFormLayout.addRow( self.saveButton )
    
    self.scrollArea.setWidget(self.groupBox)

    self.base.addWidget(self.scrollArea)

    self.setLayout(self.base)

    self.loadSettings( self.settingsFormLayout )

  def settingsPaths (self ):
    paths = {"dirpath": "", "filepath": ""}
    
    dirName = "KritaPMPlugin"
    fileName = "pmsettings"
    dirpath = os.path.expanduser("~/" + dirName)
    nicepath = os.path.abspath(dirpath)

    paths["dirpath"] = nicepath
    
    filepath = os.path.expanduser("~/" + dirName + "/" + fileName + ".txt")
    nicepath = os.path.abspath(filepath)        

    paths["filepath"] = nicepath
    
    return paths

  def writeSettingsFile( self ):
    paths = self.settingsPaths()

    if not os.path.exists(paths["dirpath"]):
      os.mkdir(paths["dirpath"])

    with open(paths["filepath"] , "w") as file:
      file.write(json.dumps(self.menus))

  def readSettingsFile( self ):
    paths = self.settingsPaths()

    # check if directory exists
    if not os.path.exists(paths["dirpath"]) or not os.path.exists(paths["filepath"]):
      return False
      
    with open(paths["filepath"], "r") as file:
      data = file.read()
      
    self.menus = json.loads(data)
    
    return True
    
  def loadSettings( self, layout ):
    # load file here into self.menus else go default
    if not self.readSettingsFile():
      self.menus = self.defaultMenus

    if len(self.menus["menu"]) == 0:
      self.menus = self.defaultMenus

    self.baseMenuSectionsCombo.setCurrentIndex( len( self.menus["menu"]) )
    
    self.setMenuItems(self.menus, layout)

    self.menusChanged.emit()

  def setMenuItems( self, menu, layout, isSubmenu=False, submenuRef=None ):
    start = 2 if isSubmenu else 3
    row = start
    i = 0
    ref = str(submenuRef)

    while row >= start and row <  layout.rowCount():

      widget1 = None if not hasattr(layout.itemAt( row, 0 ), "widget") else layout.itemAt( row, 0 ).widget()
      widget2 = None if not hasattr(layout.itemAt( row, 1 ), "widget") else layout.itemAt( row, 1 ).widget()
      
      if isinstance(widget1, QLabel) and isinstance(widget2, QComboBox) and not isSubmenu:
        index = widget2.findText( menu["menu"][i]["name"] )
        widget2.setCurrentIndex( index )
        ref = str(menu["menu"][i]["ref"])
        i += 1
      elif isinstance(widget1, QLabel) and isinstance(widget2, QCheckBox) and not isSubmenu:
        if menu["menu"][i - 1]["isSubmenu"]:
          widget2.setChecked(menu["menu"][i - 1]["isSubmenu"])
          layout.itemAt( row + 1, 1 ).widget().layout().itemAt(1, 1).widget().setCurrentIndex( len( menu["submenus"][ref] ) )
      elif isinstance(widget1, QLabel) and isinstance(widget2, QComboBox) and isSubmenu:
        index = widget2.findText( menu["submenus"][ref][i]["name"] )
        widget2.setCurrentIndex( index )
        i += 1
      elif  isinstance(widget2, QGroupBox):
        self.setMenuItems( menu, widget2.layout(), True, ref )
        
      row += 1
      
  def saveSettings( self, layout, actionsList ):
    settings = self.getSettings( layout )
    self.menus = self.generateMenuStructure( settings, actionsList )

    if len(self.menus["menu"]) == 0:
      self.menus = self.defaultMenus

    # write to file
    self.writeSettingsFile()

    self.menusChanged.emit()

  def generateMenuStructure( self, settings, actionsList ):
    menus = {
      "menu": [],
       "submenus": {}
    }

    # Basemenu
    for actionName in settings[0]:
      menus["menu"].append({
        "name": actionName,
        "actionID": self.GetActionID(actionName, actionsList),
        "isSubmenu": False,
        "ref": None,
        "category": self.GetCategory(actionName, actionsList),
        "callback": self.GetCallback(actionName, actionsList),
        "resetCallback": self.GetResetCallback(actionName, actionsList)
      })

    # Submenus
    for index in range( 0, len(settings[1]), 2 ):
      if len( settings[1][index] ) == 0:
        continue
      
      submenuIndex = settings[1][index + 1]

      menus["menu"][submenuIndex]["isSubmenu"] = True
      menus["menu"][submenuIndex]["ref"] = str(submenuIndex)

      menus["submenus"][str(submenuIndex)] = []
      
      for actionName in settings[1] [index]:
        menus["submenus"][str(submenuIndex)].append({
          "name": actionName,
          "actionID": self.GetActionID(actionName, actionsList),
          "isSubmenu": False,
          "ref": None,
          "category": self.GetCategory(actionName, actionsList),
          "callback": self.GetCallback(actionName, actionsList),
          "resetCallback": self.GetResetCallback(actionName, actionsList)
        })

    return menus

  def GetCategory(self, actionName, actionsList):
    for action in actionsList:
      if action["name"] == actionName:
        return action["category"]

  def GetResetCallback(self, actionName, actionsList):
    for action in actionsList:
      if action["name"] == actionName:
        return action["resetCallback"]

  def GetCallback(self, actionName, actionsList):
    for action in actionsList:
      if action["name"] == actionName:
        return action["callback"]

  def GetActionID(self, actionName, actionsList):
    for action in actionsList:
      if action["name"] == actionName:
        return action["actionID"]

  def getSettings( self, layout, isSubmenu=False ):
    menu = []
    submenus = []
    
    start = 2 if isSubmenu else 3
    submenuIndex = -1
    for row in range(start, layout.rowCount()):

      widget1 = None if not hasattr(layout.itemAt( row, 0 ), "widget") else layout.itemAt( row, 0 ).widget()
      widget2 = None if not hasattr(layout.itemAt( row, 1 ), "widget") else layout.itemAt( row, 1 ).widget()
      
      if isinstance(widget1, QLabel) and isinstance(widget2, QComboBox) and not isSubmenu:
        menu.append(widget2.currentText())
        submenuIndex += 1
      elif isinstance(widget1, QLabel) and isinstance(widget2, QComboBox) and isSubmenu:
        submenus.append(widget2.currentText())
      elif  isinstance(widget2, QGroupBox):
        submenus.append( self.getSettings( widget2.layout(), True ) )
        submenus.append( submenuIndex )

    if isSubmenu:
      return submenus
    else:
      return [menu, submenus]

  def addLine( self ):
    line = QFrame()
    line.setFrameShape(QtWidgets.QFrame.HLine)
    line.setFrameShadow(QtWidgets.QFrame.Sunken)
    line.setLineWidth(1)
    line.setStyleSheet("QFrame {background-color: rgb(112,112,112)}")
    return line

  def addSubMenu( self, val ):
    index = self.sender().sectionIndex
    pos = self.settingsFormLayout.getWidgetPosition(self.sender())
    
    if val != 2:
      self.settingsFormLayout.removeRow(pos[0] + 1)
    else:            
      subMenu = QGroupBox()
      subMenuLayout = QFormLayout()
      subMenuLayout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
      
      subMenuLayout.addRow(self.addLabel("Submenu " + str( index )))
      self.baseMenuSectionsCombo = self.addComboRow("Sections:", self.sectionsMaxCount, subMenuLayout)[1]
      self.baseMenuSectionsCombo.currentIndexChanged.connect( lambda: self.menuAddSections(subMenuLayout, True) )

      subMenuLayout.addRow( self.addLine() )            
      subMenu.setLayout( subMenuLayout )
    
      self.settingsFormLayout.insertRow(pos[0] + 1, subMenu)

  def menuAddSections( self, layout, isSubMenu=False ):
    row = 1 if isSubMenu else 0
    
    sectionsCountTxt = layout.itemAt(row, QFormLayout.FieldRole).widget().currentText()

    sectionsCount = int( sectionsCountTxt )

    if layout.rowCount() > 3:
      for i in range( layout.rowCount() - 1, 2, -1 ):
        layout.removeRow(i)

    for i in range( sectionsCount ):
      comboRow = self.addComboRow( "Action " + str( i ) + ":", self.actionsList, layout )

      if not isSubMenu:
        checkBoxRow = self.addCheckBoxRow( "Sub Menu:", layout )
        checkBoxRow[1].stateChanged.connect(self.addSubMenu)
        checkBoxRow[1].sectionIndex = i

        layout.addRow( self.addLine() )

  def addCheckBoxRow(self, txt, layout):
    elms = [ self.addLabel(txt), QCheckBox() ]
    layout.addRow( elms[0], elms[1] )
    return elms

  def addLabel(self, label):
    label = QLabel( str(label) )
    label.setStyleSheet( "QLabel {font-size: 12px;}" )
    return label

  def addComboBox(self, actionsList):
    comboBox = CustomComboBox()
    
    # to remove wheelEvent so scrolling works on the scrollarea but not on individual buttons
    comboBox.setFocusPolicy(Qt.StrongFocus)
    actions = []
    categories = {}

    if isinstance(actionsList, int) or isinstance(actionsList, str):
      for i in range(self.sectionsMaxCount):
        actions.append(str(i))
    else:
      # Form the list of categories
      for action in actionsList:
        if (action["category"] not in categories):
          categories[str(action["category"])] = []

        categories[str(action["category"])].append(action["name"])

      # Alphabetic sort
      for category in categories:
        categories[category] = sorted(categories[category])

      for category, actionList in sorted(categories.items()):
          if category not in actions:
            actions.append(str(category))

          for action in actionList:
            actions.append(str(action))

    comboBox.addItems(actions)

    if bool(categories):
      index = 0

      for category, actionList in sorted(categories.items()):
        comboBox.model().item(index).setEnabled(False)

        font = QFont()
        font.setBold(True)

        comboBox.model().item(index).setFont(font)

        index += 1 + len(actionList)

      comboBox.setCurrentIndex(1)

    return comboBox

  def addComboRow(self, txt, actionsList, layout):
    elms = [ self.addLabel(txt), self.addComboBox(actionsList) ]
    layout.addRow( elms[0], elms[1] )
    return elms

  def accept(self):
    super(Settings, self).accept()

  def reject(self):
    super(Settings, self).reject()
