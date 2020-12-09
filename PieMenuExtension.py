class PieMenuExtension(Extension):
  def __init__(self,parent):
    super(PieMenuExtension, self).__init__(parent)
    dialog = Dialog("test")
  def setup(self):
    pass

  def createActions(self, window):
    self.PMAction = window.createAction("pieMenu", "Pie Menu")