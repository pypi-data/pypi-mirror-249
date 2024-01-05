from . import Core


class By:
    NAME = "_name"
    CLASS = "_class"
    TAG = "_tag"


class WidgetType(Core.BufferManager):
    def __init__(self,
                 _name: str = None,
                 _class: str = "main",
                 _tag: str = "WidgetType"):
        self._name = _name
        self._class = _class
        self._tag = _tag

        self.Join = Core.EventManager(self.join)

        super().__init__()


class LayerType(WidgetType):
    def __init__(self,
                 _name: str = None,
                 _class: str = "main",
                 _tag: str = "LayerType"):
        import os
        self.widget_list = []
        self.symbol = "\n"
        self.loop = False

        self.shellClear = lambda: os.system("cls")

        self.Looping = Core.EventManager(self.looping)
        self.Closing = Core.EventManager(self.closing)

        super().__init__(_name, _class, _tag)

    def looping(self):
        """Open layer loop"""
        self.loop = True

    def closing(self):
        """Close layer loop"""
        self.loop = False

    def find(self, key: By.NAME, val):
        """
        Finding a child element in a layer widget list
        :return: class exemplar
        """
        ret = []
        for widget in self.widget_list:
            if eval(f"widget.{key} == val"):
                ret.append(widget)
        return ret
