from tkinter import Frame, Button, Canvas, PhotoImage, Text, Entry, END, Menu
from source.frame.setting import Setting
from source.frame.translation import Translation
from source.frame.parameter._name import Name
from source.frame.parameter._generals import General
from source.frame.parameter._child import Child
from source.frame.settings.valueConfig import valueConfig
from source.frame.settings.valueEnum import valueEnum
from source.frame.settingList import SettingList


class Parameter(Frame):
    def __init__(self, parent, frame, name, type=''):
        super().__init__(
            master=frame
        )
        self.widen = False
        self.pack(side='top', anchor='nw')

        self.par_parent = parent

        self.name = Name(self, name, self.get_parent, self.change_size)

        self._general = General(self, self.get_parent, self.name.get())

        self.translations = Translation(self._general, self.get_parent)
        
        self.child = Child(self, self.get_parent)
      
    def get_parent(self, parents: list):
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

        if name == 'enumKey':
            contains = ['valueEnum', 'valueConfig']

            for container in contains:
                if container in self.child.list:
                    if self.child.list[container].update_keys(value):
                        return

        if name == 'name':
            self.par_parent.child.rename(self.name.get(), value)
            self.name.call_set(value)

        elif name in Translation.names:
            if isinstance(value, list):
                contains = ['valueEnum', 'valueConfig']

                for container in contains:
                    if container in self.child.list:
                        if self.child.list[container].update_translation(name, value):
                            return

            self.translations.call_set(name, value)

        elif name == 'valueType':
                self._general.call_set(value)
                
                if value == "Branch":
                    self.child.show_addable()
                else:
                    self.child.hide_addable()

                if 'valueConfig' in self.child.list:
                    self.child.list['valueConfig']

        elif name not in self.child.list:
            match name:
                case 'valueConfig':
                    self.child.list[name] = valueConfig(self, self.child, name, value, self._general.type.get())
                    self.child.list[name].reload_language()

                case 'valueEnum':
                    self.child.list[name] = SettingList(self, self.child, name, value, translation=True)
                    self.child.list[name].reload_language()

                case 'enumKey':
                    self.child.list[name] = valueEnum(self, self.child, name, value)

                case _:
                    self.child.list[name] = Setting(self, self.child, name, value)
        else:
            self.child.list[name].update(value)

    def add_child(self, name):
        if name not in self.child.list:
            self.child.list[name] = Parameter(self, self.child, name)
            self.child.list[name].translations.reload_language()

    def set_warn(self, text):
        self.name.warn(text)

    def warn(self, name, value):
        if name in Translation.names:
            self.translations.color(name, '#FF0000')

        elif name == 'valueType':
            self._general.color('#FF0000')
        elif name == 'enumKey':
            if 'valueConfig' in self.child:
                self.child.list[name].set_warn(value)
            elif 'valueEnum' in self.child:
                self.child.list[name].set_warn(value)
            else:
                self.child.list[name].set_warn(value)
        else:
            self.child.list[name].set_warn(value)
