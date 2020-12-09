from krita import *
from .PieMenuExtension import PieMenuExtension

Krita.instance().addExtension(PieMenuExtension(Krita.instance()))