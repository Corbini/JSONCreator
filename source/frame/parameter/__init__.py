from tkinter import Frame, Button, Canvas, PhotoImage, Text, Entry, END
from source.frame.setting import Setting


class Parameter(Frame):

    from ._name import create_name, change_name, configure_name, update_name
    from ._generals import create_generals, show_generals, hide_generals

    call = lambda self, parents, name, value: print(parents, name, value)

    def __init__(self, parent, frame, name, type='untype'):
        super().__init__(
            master=frame
        )
        self.pack(side='top', anchor='nw')

        self.par_parent = parent

        self.create_name(name)
        self.create_generals(type)

        self.settings_view = Frame(self)
        self.settings_list = dict()

        self.widen = False

    def get_parent(self, parents: list):
        if self.par_parent is not None:
            self.par_parent.get_parent(parents)
            parents.append(self.name_button.cget('text'))

    def change_size(self):
        if self.widen is False:

            self.settings_view.grid(row=1, column=1, sticky='nw')
            self.show_generals()

            self.widen = True

        else:
            self.settings_view.grid_forget()
            self.hide_generals()

            self.widen = False

    def set_type(self, value):
        self.general_types.delete(0, END)
        self.general_types.insert(0, value)

    def update_setting(self, name, value):
        
        if name == "name":
            self.update_name(name)
            return

        if name == "langPl":
            self.general_pl.insert(0, value)
            return

        if name == "langEn":
            self.general_en.insert(0, value)
            return

        if name == "valueType":
            self.set_type(value)
            return

        if name not in self.settings_list:
            self.settings_list[name] = Setting(self, self.settings_view, name, value)
        else:
            self.settings_list[name].update(value)

    def add_child(self, name):
        if name in self.settings_list:
            return

        self.settings_list[name] = Parameter(self, self.settings_view, name)
