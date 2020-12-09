from .krita-plugin-pie-menu import PieMenuExtension

Krita.instance().addExtension(PieMenuExtension(Krita.instance()))