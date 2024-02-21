from tkinter import Frame, Button, Canvas, PhotoImage, Text, Entry, END
from source.frame.setting import Setting
from source.frame.translation import Translation
from source.frame.parameter._name import Name
from source.frame.parameter._generals import General
from source.frame.parameter._child import Child
from source.frame.settings.valueConfig import valueConfig


class Parameter(Frame):
    def __init__(self, parent, frame, name, type=''):
        super().__init__(
            master=frame
        )
        self.widen = False
        self.pack(side='top', anchor='nw')

        self.par_parent = parent

        self.name = Name(self, name, self.get_parent, self.change_size)

        self._general = General(self, self.get_parent, self.name.get)

        self.translations = Translation(self._general, self.get_parent)
        
        self.child = Child(self, self.get_parent)

    def get_parent(self, parents = list()):
        parent = self.par_parent
        
        parents.insert(0, self.name.get())
        while parent is not None:
            parents.insert(0, parent.name.get())
            parent = parent.par_parent

        return parents

    def change_size(self):
        if self.widen is False:

            self.child.show()
            self._general.show()

            self.widen = True

        else:
            self.child.hide()
            self._general.hide()

            self.widen = False

    def update_setting(self, name, value):
        if name == 'name':
            self.par_parent.child.rename(self.name.get(), value)
            self.name.call_set(value)

        elif name in Translation.names:
            self.translations.call_set(name, value)

        elif name == 'valueType':
                self._general.call_set(value)
                
                if value == "Branch":
                    self.child.show_addable()
                else:
                    self.child.hide_addable()

        elif name not in self.child.list:
            if name == 'valueConfig':
                self.child.list[name] = valueConfig(self, self.child, name, value)
            else:
                self.child.list[name] = Setting(self, self.child, name, value)
        else:
            self.child.list[name].update(value)

    def add_child(self, name):
        if name not in self.child.list:
            self.child.list[name] = Parameter(self, self.child, name)
            self.child.list[name].translations.reload_language()
 