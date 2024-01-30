from tkinter import Frame, Button, Canvas, PhotoImage, Text, Entry
from source.frame.setting import Setting


class Parameter(Frame):

    from ._name import create_name, change_name, configure_name, update_name
    from ._generals import create_generals

    def __init__(self, parent, frame, name):
        super().__init__(
            master=frame
        )
        self.pack(side='top', anchor='nw')
        self.pack_propagate(True)

        self.par_parent = parent

        self.create_name(name)
        self.create_generals()

        self.settings_view = Frame(self)

        self.settings_view.propagate(True)
        self.settings_list = dict()
        self.type = "int"

        self.settings_view.grid(row=1, column=1, sticky='nw')
        self.widen = False

    def change_size(self):
        if self.widen is False:

            self.settings_view.update()
            height = self.settings_view.winfo_height() + 30
            width = self.settings_view.winfo_width() + 220

            if height < 190:
                height = 190

            self.configure(
                height=height,
                width=1000
            )

            self.widen = True

        else:
            # self.settings_view.place_forget()

            self.general

            self.widen = False

    def set_type(self):
        self.type = "new_name"
        self.settings_list = dict()

    def update_setting(self, name, value):
        
        if name == "name":
            self.update_name(name)
            return

        if name == "langPl":
            self.entry_2_t.insert(0, value)
            return

        if name == "langEn":
            self.entry_1_t.insert(0, value)
            return

        if name == "valueType":
            return

        if name not in self.settings_list:
            print("Create setting")
            self.settings_list[name] = Setting(self, self.settings_view, name, value)
        else:
            self.settings_list[name].update(value)

    def add_child(self, name):
        if name in self.settings_list:
            return

        print("Create parameter", name)
        self.settings_list[name] = Parameter(self, self.settings_view, name)
